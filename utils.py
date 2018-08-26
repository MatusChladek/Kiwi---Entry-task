def create_flights(df,flights,bags):
    output = []
    count_check = 0

    df1 = df.loc[df.bags_allowed >= bags,:]
    # set proper unique identifier here brah
    #df1 = df1.set_index('flight_number')

    for counter,route in enumerate(flights):
        #print(route)
        pls = df1.loc[route[-1],:]
        # filter just rows with correct source
        temp_df = df1.loc[df1.source == pls.destination,:]
        # filter just time wise available fligths
        temp_df['wait'] = (temp_df.departure - pls.arrival)/pd.Timedelta('1h')
        temp_df = temp_df.query('1<=wait<=4')

        if len(temp_df)!=0:
            #checking if there are any new flights at all
            count_check += 1

            for item in temp_df.index:
                new_route = np.append(route,item)
                output.append(new_route)
        else:
            output.append(route)
    #print(count_check)

    if count_check != 0 :
        output = create_flights(df,output,bags)

    return output

# create all subsets with initial start
def get_subsets(route_list):
    output = []

    for route in route_list:
        #print(route)
        output.append(route)
        for i in range(1,len(route)):
            output.append(route[:-i])
        #print(b)
    return output

# delete routes with repeating locs
def del_repeats(df,routes,bags):
    output = []
    for route in routes:

        temp = []
        df1 = df.loc[df.bags_allowed >= bags,:]
        # set proper unique identifier here brah
        #df1 = df1.set_index('flight_number')

        # create source location
        temp.append(df1.loc[route[0],:].source)
        # append destinations to source etc
        for item in route:
            temp.append(df1.loc[item,:].destination)

        output.append(temp)

    #print(output)

    # only those where all are unique or all unique exept for start & end
    indexer = [counter for counter,i in enumerate(output) if (len(set(i)) == len(i)) or ((i[0] == i[-1]) and (len(set(i))+1 == len(i)))]
    output = [i for _,i in enumerate(output) if (len(set(i)) == len(i)) or ((i[0] == i[-1]) and (len(set(i))+1 == len(i)))]

    #print('skap')
    #print(indexer)
    #print(output)
    return indexer

# compute price for trips
def add_price(df,routes,bags):
    output = []
    #df = df.set_index('flight_number')

    for route in routes:
        price = np.sum(df.loc[route,:].price + df.loc[route,:].bag_price*bags)
        output.append(np.append(route,price))
    return output

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

    for route in routes:
        temp = []
        for item in route[:-1]:
            temp.append(df.loc[item,:])
        temp.append(route[-1])
        output.append(temp)

    return output
