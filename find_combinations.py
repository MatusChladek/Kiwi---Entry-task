import pandas as pd
from datetime import datetime
import numpy as np

#%reload_ext autoreload
#%autoreload 2
from utils import *

def get_flights(df,bags):
    df.departure = pd.to_datetime(df.departure,format='%Y-%m-%dT%H:%M:%S')
    df.arrival = pd.to_datetime(df.arrival,format='%Y-%m-%dT%H:%M:%S')
    locs = df.source.unique()
    output = {}

    for start in locs:
        flights = []

        # create list of all flights from start destination
        # consider inices to not be flight_number since there
        # can be repeating flight_numbers in different days
        df_start = df.loc[df.source == start,:]
        df_start = df_start.loc[df_start.bags_allowed >= bags,:]

        for item in df_start.index:
            flights.append([item])

        flights = np.array(flights)

        # longest trips from start destination for each flight
        new = create_flights(df,flights,bags)

        # create all valid subsets of longest trips
        subsets = get_subsets(new)

        # delete those trips with repeating locations (exept for start/end)
        indexes = del_repeats(df,subsets,1)
        uniques = [subsets[i] for i in indexes]

        # delete repeating trips
        uniques_set = set(tuple(x) for x in uniques)
        uniques = [list(x) for x in uniques_set]

        # add price to the end of each trip
        final = add_price(df,uniques,bags)

        # map IDs to df rows for postproccessing
        # though I think that storing just ID is best way for further processing
        final = map_index(df,final)

        output[start] = final
    return output

# 1) in case we want to do it directly from file
# df = pd.read_csv('data1.csv',parse_dates=True)

# 2) read console
import csv
import sys

f = sys.stdin.read().splitlines()
lines = csv.reader(f)
lines = list(lines)
column_names = lines[0]
rows = lines[1:]
df = pd.DataFrame(columns=column_names)
for i in range(len(rows)):
    df.loc[i] = rows[i]
df.price = df.price.astype(int)
df.bags_allowed = df.bags_allowed.astype(int)
df.bags_price = df.bags_price.astype(int)



# print all combinations
# of flights for passengers with no bags, one bag or two bags
bags_0 = get_flights(df,0)
print("All routes for passengers without a bag: ",bags_0)
bags_1 = get_flights(df,1)
print("All routes for passengers with one bag: ",bags_1)
bags_2 = get_flights(df,2)
print("All routes for passengers with two bags: ", bags_2)

# Output is dictionary with locations and nested lists where
# price is always last item
