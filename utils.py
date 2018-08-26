def create_flights(df,flights,bags):
    output = []
    count_check = 0
    df1 = df.loc[df.bags_allowed >= bags,:]

    for counter,route in enumerate(flights):
        # take just last flight
        pls = df1.loc[route[-1],:]

        # filter just rows with correct source
        temp_df = df1.loc[df1.source == pls.destination,:]

        # filter just time wise available fligths
        # using more/less or equal based on my understanding
        # above actually makes difference
        temp_df['wait'] = (temp_df.departure - pls.arrival)/pd.Timedelta('1h')
        temp_df = temp_df.query('1<=wait<=4')

        if len(temp_df) != 0:
            #checking if there are any new flights at all
            count_check += 1
            for item in temp_df.index:
                new_route = np.append(route,item)
                output.append(new_route)
        else:
            output.append(route)
    #print(count_check)

    # do until no new flights were found for all current trips
    if count_check != 0 :
        output = create_flights(df,output,bags)

    return output

#####################################################################

# create all subsets of longest trips starting with initial start
def get_subsets(route_list):
    output = []

    for route in route_list:
        output.append(route)
        for i in range(1,len(route)):
            output.append(route[:-i])
    return output

#######################################################################
# delete trips with repeating locs
# default start end location doesn't have to be same
# possible to force equal start & end location
def del_repeats(df,routes,bags,start_end_equal = False):
    output = []
    for route in routes:
        temp = []
        df1 = df.loc[df.bags_allowed >= bags,:]

        # create source location
        temp.append(df1.loc[route[0],:].source)

        # append destinations to source etc
        for item in route:
            temp.append(df1.loc[item,:].destination)

        output.append(temp)


    # only those where all are unique or all unique except for start & end
    if start_end_equal:
        indexer = [counter for counter,i in enumerate(output) if ((i[0] == i[-1]) and (len(set(i))+1 == len(i)))]
        output = [i for _,i in enumerate(output) if ((i[0] == i[-1]) and (len(set(i))+1 == len(i)))]
    else:
        indexer = [counter for counter,i in enumerate(output) if (len(set(i)) == len(i)) or ((i[0] == i[-1]) and (len(set(i))+1 == len(i)))]
        output = [i for _,i in enumerate(output) if (len(set(i)) == len(i)) or ((i[0] == i[-1]) and (len(set(i))+1 == len(i)))]

    return indexer

############################################################################
# compute price for trips
def add_price(df,routes,bags):
    output = []

    for route in routes:
        price = np.sum(df.loc[route,:].price + df.loc[route,:].bag_price*bags)
        output.append(np.append(route,price))
    return output


###########################################################################
# map indices on rows for postprocessing
# possible to create loc only + price outputs
def map_index(df,routes,locs_only=False):
    output = []

    if locs_only:
        for route in routes:
            temp = []
            # create source location
            temp.append(df.loc[route[0],:].source)
            # append destinations to source etc
            for item in route[:-1]:
                temp.append(df.loc[item,:].destination)
            temp.append(route[-1])
            output.append(temp)

    else:
        for route in routes:
            temp = []
            for item in route[:-1]:
                temp.append(df.loc[item,:])
            temp.append(route[-1])
            output.append(temp)

    return output
