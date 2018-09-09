import psycopg2
from psycopg2.extras import RealDictCursor
import https_req

# SELECT * FROM [leproject-186622:breachcomp.anti_public]
# WHERE email LIKE 'blabla@gmail.com' in BigQuery

pg_config = {
    'host': '35.234.120.106',
    'database': 'pythonweekend',
    'user': 'shareduser',
    'password': 'NeverEverSharePasswordsInProductionEnvironement'
}

conn = psycopg2.connect(**pg_config)

cur = conn.cursor()

# check all available tables
cur.execute("select relname from pg_class where relkind='r' and relname !~ '^(pg_|sql_)';")
lst = cur.fetchall()
print(lst)

# 
for item in lst:
    item = str(item)
    item = item.replace("'","")
    item = item.replace(")","")
    item = item.replace("(","")
    item = item.replace(",","")
    cur.execute(f'SELECT * FROM {item}')
    all = cur.fetchall()
    #if all != []:
    #    print(item)


# Insert data into the table
sql_insert = """
    INSERT INTO matus_connections (src_id, dst_id, dep, arr, price)
    VALUES (%(src_id)s,
            %(dst_id)s,
		    %(dep)s,
            %(arr)s,
            %(price)s);
"""

src = 'Barcelona'
dst = 'Madrid'
date_from = '09-09-2018'

# load play results for random 
results = https_req.return_route(src,dst,date_from)
for value in results:
    #value = {‘src_id’: 91342, ‘dep’: datetime_object, ‘price’: 133.7, ‘dep’: datetime_object}
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(sql_insert, value)  # psycopg2 prepared statement syntax
        conn.commit()  # important, otherwise your data won’t be inserted!


    # departure_time & arrival_time should be datetime object, psycopg2 will format them for you

#Lighting talk notes

# DataDog - for alarming, ping metrics etc (has free tier) and speeds up debugging
# datadog/github
# track fnc timings
###########################
# Sentry -  something like debug mode in flask
# monitor errors
###########################
# Black -  for code formatting
###########################
# Coala