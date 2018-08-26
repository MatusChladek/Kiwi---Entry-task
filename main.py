import pandas as pd
from datetime import datetime
import numpy as np

%reload_ext autoreload
%autoreload 2
from utils import *

def get_flights(df,bags):
    df.departure = pd.to_datetime(df.departure,format='%Y-%m-%dT%H:%M:%S')
    df.arrival = pd.to_datetime(df.arrival,format='%Y-%m-%dT%H:%M:%S')
    locs = df.source.unique()
    output = {}

    for start in locs:
        #print(start)
        flights = []

        # create list of all flights from start destination
        # consider flight_number to be unique index temporarily
        df_start = df.loc[df.source == start,:]
        #print(df_start)
        df_start = df_start.loc[df_start.bags_allowed >= bags,:]
        for item in df_start.index:
            flights.append([item])

        flights = np.array(flights)
        #print(flights)

        # longest trips from start destination for each flight
        new = create_flights(df,flights,bags)
        #print(new)

        # create subsets of longest trips
        subsets = get_subsets(new)
        #print(subsets)

        # delete those with repeating locations
        indexes = del_repeats(df,subsets,1)
        uniques = [subsets[i] for i in indexes]
        uniques_set = set(tuple(x) for x in uniques)
        uniques = [list(x) for x in uniques_set]
        uniques
        #print(uniques)

        # add price to the end of each trip
        final = add_price(df,uniques,bags)

        # map it to create proper trip (I think that storing just ID is best way for further processing)
        final = map_index(df,final)

        output[start] = final
    return output

# in case we want to do it directly from file
#df = pd.read_csv('data1.csv',parse_dates=True)

# read console
import csv
import sys

f = sys.stdin.read().splitlines()
lines = csv.reader(f, delimiter=';')
lines = list(lines)
column_names = lines[0]
rows = lines[1:]
df = pd.DataFrame(columns=column_names)
for i in range(len(rows)):
    df.loc[i] = rows[i]

print(df)



bags_0 = get_flights(df,0)
print("All routes for passengers without a bag: ",bags_0)
bags_1 = get_flights(df,1)
print("All routes for passengers with one bag: ",bags_1)
bags_2 = get_flights(df,2)
print("All routes for passengers with two bags: ",bags_2)
