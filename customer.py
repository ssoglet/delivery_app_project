import time
import argparse
from helpers.connection import conn
import json
from geopy.distance import geodesic as GD
import operator

def main(args):
    try:
        cur = conn.cursor()

        #Information option
        if args.option == "info":
            #Print information of the entered customer
            if len(args.property) == 0:
                print("***Information of Customer***")
                sql = "SELECT * FROM customer WHERE id=%(id)s;"
                cur.execute(sql, {"id": args.id})
                rows = cur.fetchall()
                for row in rows:
                    print("ID:", row[0])
                    print("Name:", row[1])
                    print("Phone Number:", row[2])
                    print("Local:", row[3])
                    print("Email:", row[4])
                    print("Payments:", row[6])
                    print("Latitude:", row[7])
                    print("Longitude:", row[8])
            #Print address of the entered customer
            elif len(args.property) == 1 and args.property[0] == "address":
                print("***Address of Customer***")
                sql = "SELECT * FROM customer WHERE id=%(id)s;"
                cur.execute(sql, {"id": args.id})
                rows = cur.fetchall()
                for row in rows:
                    for i in range(len(row[9])):
                        print("Address", i+1, ":", str(row[9][i]))

        #Update option
        elif args.option == "update" and args.property[0] == "address":
            #Add new address
            if args.property[1] == "--c" or args.property[1] == "--create":
                sql = "UPDATE customer SET address=array_append(address,'" + args.property[2] + "') WHERE id=%(id)s;"
                cur.execute(sql, {"id": args.id})
                conn.commit()
            #Change the address of entered number into entered value
            elif args.property[1] == "--e" or args.property[1] == "--edit":
                sql = "UPDATE customer SET address['" + args.property[2] + "'] = '" + args.property[3] + "' WHERE id=%(id)s;"
                cur.execute(sql, {"id": args.id})
                conn.commit()
            #Delete the address of entered number
            elif args.property[1] == "--r" or args.property[1] == "--remove":
                sql = "UPDATE customer SET address['" + args.property[2] + "'] = NULL WHERE id=%(id)s;"
                cur.execute(sql, {"id": args.id})
                conn.commit()

        #Pay option
        elif args.option == "pay":
            #Print the information of payments of entered customer
            if len(args.property) == 0:
                print("***Information of Payments***")
                sql = "SELECT * FROM customer WHERE id=%(id)s;"
                cur.execute(sql, {"id": args.id})
                rows = cur.fetchall()
                for row in rows:
                    pay_num = len(row[6])
                    for i in range(pay_num):
                        print("Payment", i+1, ":", row[6][i])
            #Add entered card payment
            elif len(args.property) == 2 and args.property[0] == "--add-card":
                sql1 = "SELECT JSONB_ARRAY_ELEMENTS(payments) FROM customer WHERE id=%(id)s;"
                cur.execute(sql1, {"id": args.id})
                rows = cur.fetchall()
                list = []
                for row in rows:
                    list.append(row[0])
                list.append({'data': {'card_num': args.property[1]}, 'type': 'card'})
                lists = json.dumps(list)
                sql2 = "UPDATE customer SET payments = '" + lists + "'WHERE id=%(id)s;"
                cur.execute(sql2, {"id": args.id})
                conn.commit()
            #Add entered account payment
            elif len(args.property) == 3 and args.property[0] == "--add-account":
                sql1 = "SELECT JSONB_ARRAY_ELEMENTS(payments) FROM customer WHERE id=%(id)s;"
                cur.execute(sql1, {"id": args.id})
                rows = cur.fetchall()
                list = []
                for row in rows:
                    list.append(row[0])
                list.append({'data': {'bid': args.property[1], 'acc_num': args.property[2]}, 'type': 'account'})
                lists = json.dumps(list)
                sql2 = "UPDATE customer SET payments = '" + lists + "'WHERE id=%(id)s;"
                cur.execute(sql2, {"id": args.id})
                conn.commit()
            #Delete payment of entered number
            elif len(args.property) == 2 and args.property[0] == "-r" or args.property[0] == "--remove":
                args.property[1] = str(int(args.property[1]) - 1)
                sql = "UPDATE customer SET payments['" + args.property[1] + "'] = NULL WHERE id=%(id)s;"
                cur.execute(sql, {"id": args.id})
                conn.commit()

        #Search option
        elif args.option == "search" and args.property[0] == "-a" and args.property[1] == "-o" and args.property[3] == "-l":
            #Print entered number of stores in ascending order of name
            if args.property[2] == "0":
                print("***Stores in Ascending Order of Name***")
                sql = "SELECT sname FROM store ORDER BY sname LIMIT'" + args.property[4] + "';"
                cur.execute(sql)
                rows = cur.fetchall()
                i = 1
                for row in rows:
                    print("* Store", i, "*")
                    print("Store Name:", row[0])
                    i += 1
            #Print entered number of stores in ascending oroder of address
            elif args.property[2] == "1":
                print("***Stores in Ascending Order of Address***")
                sql = "SELECT address, sname FROM store ORDER BY address LIMIT'" + args.property[4] + "';"
                cur.execute(sql)
                rows = cur.fetchall()
                i = 1
                for row in rows:
                    print("* Store", i, "*")
                    print("Store Address:", row[0])
                    print("Store Name:", row[1])
                    i += 1
            #Print entered number of nearest stores from the customer
            elif args.property[2] == "2":
                #Count number of total stores
                print("***Nearest Stores***")
                sql1 = "SELECT count(*) FROM store;"
                cur.execute(sql1)
                rows = cur.fetchall()
                for row in rows:
                    stores = row[0]
                #Set customer location as departure
                sql2 = "SELECT * FROM customer WHERE id=%(id)s;"
                cur.execute(sql2, {"id": args.id})
                rows = cur.fetchall()
                for row in rows:
                    departure = (row[7], row[8])
                #Set store location as arrival and find nearest stores
                distance_list = []
                for i in range(stores+1):
                    sql3 = "SELECT * FROM store WHERE id=%(id)s;"
                    cur.execute(sql3, {"id": i})
                    rows = cur.fetchall()
                    for row in rows:
                        arrival = (row[3], row[4])
                        distance = GD(departure, arrival).km
                        distances = (i, distance)
                        distance_list.append(distances)
                #Sort the stores in order of proximity
                distance_dict = dict(distance_list)
                sorted_distance = sorted(distance_dict.items(), key=operator.itemgetter(1))
                near_stores = []
                for i in range(stores):
                    near_stores.append(sorted_distance[i][0])
                #Print entered number of nearest stores
                for i in range(int(args.property[4])):
                    print("* Store", i, "*")
                    print("Store ID:", near_stores[i])
                    sql4 = "SELECT * FROM store WHERE id=%(id)s;"
                    cur.execute(sql4, {"id": near_stores[i]})
                    rows = cur.fetchall()
                    for row in rows:
                        print("Store Name:", row[2])

        #Select option
        #Print menus of stores of entered number
        elif args.option == "select":
            sql = "SELECT * FROM menu WHERE sid=%(id)s;"
            cur.execute(sql, {"id": args.property[0]})
            rows = cur.fetchall()
            for row in rows:
                print(row)

        #List option
        elif args.option == "list":
            #Print total orders of the customer of entered number
            if len(args.property) == 0:
                print("***Order of the Customer***")
                sql = "SELECT * FROM public.order WHERE cid=%(id)s;"
                cur.execute(sql, {"id": args.id})
                rows = cur.fetchall()
                for row in rows:
                    print("Order ID:", row[0])
            #Print delivering orders of the customer of entered number
            elif len(args.property) == 1 and args.property[0] == "-w" or args.property[0] == "--waiting":
                print("***Delivering Order of the Customer***")
                sql = f"SELECT * FROM public.order WHERE cid=%(id)s and deliv_st='" + str(1)+ "';"
                cur.execute(sql, {"id": args.id})
                rows = cur.fetchall()
                for row in rows:
                    print("Order ID:", row[0])

    except Exception as err:
        print(err)
    pass

if __name__ == "__main__":
    start = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument("id", help="ID of Store")
    parser.add_argument("option", help="Options of Store")
    parser.add_argument("property", nargs=argparse.REMAINDER, help="Properties")
    args = parser.parse_args()
    main(args)
