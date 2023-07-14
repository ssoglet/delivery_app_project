import time
import argparse
from helpers.connection import conn
from geopy.distance import geodesic as GD
from datetime import datetime, timedelta

def main(args):
    try:
        cur = conn.cursor()

        #Information option
        #Print information of the entered ID store
        if args.option == "info":
            print("***Information of Store***")
            sql = "SELECT * FROM store WHERE id=%(id)s;"
            cur.execute(sql, {"id": args.id})
            rows = cur.fetchall()
            for row in rows:
                print("ID:", row[0])
                print("Address:", row[1])
                print("Name:", row[2])
                print("Latitude:", row[3])
                print("Longitude:", row[4])
                print("Phone Number:", row[5])
                print("Schedules:", row[6])
                print("Seller ID:", row[7])

        #Menu option
        elif args.option == "menu":
            #Print menu of the entered ID store
            if args.property[0] == "--list":
                sql = "SELECT * FROM menu WHERE sid=%(id)s;"
                cur.execute(sql, {"id": args.id})
                rows = cur.fetchall()
                for row in rows:
                    print(row)

            #Add menu to the entered ID store
            elif args.property[0] == "--add":
                sql1 = "SELECT count(*) FROM menu;"
                cur.execute(sql1)
                rows = cur.fetchall()
                for row in rows:
                    menu_id = row[0]+1
                sql2 = "INSERT INTO menu VALUES ('" + str(menu_id) + "', '" + str(args.property[1]) + "', %(id)s);"
                cur.execute(sql2, {"id": args.id})
                conn.commit()

        #Order option
        elif args.option == "order":
            #Print information of the entered ID store
            if args.property[0] == "--list" and len(args.property) == 1:
                print("***Information of Store***")
                sql = "SELECT * FROM public.order WHERE sid=%(id)s;"
                cur.execute(sql, {"id": args.id})
                rows = cur.fetchall()
                for row in rows:
                    print("Order ID:", row[0])
                    print("Customer ID:", row[1])
                    print("Store ID:", row[2])
                    print("Menu ID:", row[3])
                    print("Menu number:", row[4])
                    print("Order Time:", row[5])
                    print("Delivery Time:", row[6])
                    print("Payment ID:", row[7])
                    print("Delivering Status:", row[8])
                    print("Delivery ID:", row[9])

            #Search with delivery status filter and print order ID
            elif args.property[0] == "--list" and len(args.property) == 2:
                if args.property[1] == "0":
                    print("***PENDING***")
                    sql = "SELECT * FROM public.order WHERE sid=%(id)s AND deliv_st='0'"
                    cur.execute(sql, {"id": args.id})
                    rows = cur.fetchall()
                    for row in rows:
                        print("Order ID:", row[0])
                elif args.property[1] == "1" or args.property[1] == "delivering":
                    print("***DELIVERING***")
                    sql = "SELECT * FROM public.order WHERE sid=%(id)s AND deliv_st='1'"
                    cur.execute(sql, {"id": args.id})
                    rows = cur.fetchall()
                    for row in rows:
                        print("Order ID:", row[0])
                elif args.property[1] == "2" or args.property[1] == "delivered":
                    print("***DELIVERED***")
                    sql = "SELECT * FROM public.order WHERE sid=%(id)s AND deliv_st='2'"
                    cur.execute(sql, {"id": args.id})
                    rows = cur.fetchall()
                    for row in rows:
                        print("Order ID:", row[0])

            #Update delivery status into deliverying and match the nearest delivery man
            elif args.property[0] == "--update" and len(args.property) == 3:
                #Update order information
                sql1 = "UPDATE public.order SET deliv_st='" + str(args.property[2]) + "' WHERE order_id='" + str(args.property[1]) + "' AND sid=%(id)s;"
                cur.execute(sql1, {"id": args.id})
                conn.commit()
                #Count number of total delivery man
                sql2 = "SELECT count(*) FROM delivery;"
                cur.execute(sql2)
                rows = cur.fetchall()
                for row in rows:
                    deliveries = row[0]
                min = float(10000000)
                #Set departure location
                sql3 = "SELECT * FROM store WHERE id=%(id)s;"
                cur.execute(sql3, {"id": args.id})
                rows = cur.fetchall()
                for row in rows:
                    departure = (row[3], row[4])
                #Set arrival location and find delivery man with minimum distance
                for i in range(deliveries+1):
                    sql4 = "SELECT * FROM delivery WHERE id=%(id)s;"
                    cur.execute(sql4, {"id": i})
                    rows = cur.fetchall()
                    for row in rows:
                        arrival = (row[6], row[7])
                        distance = GD(departure, arrival).km
                        if distance < min and row[8] < 5:
                            min = distance
                            sql5 = "UPDATE public.order SET delivery='" + str(row[0]) + "';"
                            cur.execute(sql5)
                conn.commit()

        #Statistics option
        #Print the number of orders during the entered period
        elif args.option == "stat":
            print("***Number of orders***")
            for i in range(int(args.property[1])):
                count = 0
                sql1 = "SELECT TO_CHAR(order_time, 'YYYY/MM/DD') FROM public.order WHERE sid=%(id)s;"
                cur.execute(sql1, {"id": args.id})
                rows = cur.fetchall()
                for row in rows:
                    date = row[0]
                    if date == args.property[0]:
                        count += 1
                print("Date:", args.property[0])
                print("Orders:", count)
                args.property[0] = datetime.strptime(args.property[0], '%Y/%m/%d')
                args.property[0] += timedelta(days=1)
                args.property[0] = args.property[0].strftime('%Y/%m/%d')

        #Search option
        #Search the customer who ordered all menus of the entered store
        elif args.option == "search" and args.property[0] == "--customer":
            print("***Customer who ordered all menus***")
            #Counting the number of menus of the store
            sql1 = "SELECT count(*) FROM menu WHERE sid=%(id)s;"
            cur.execute(sql1, {"id": args.id})
            rows = cur.fetchall()
            for row in rows:
                total_menu = row[0]
            #Counting the total number of customers
            sql2 = "SELECT count(*) FROM customer;"
            cur.execute(sql2)
            rows = cur.fetchall()
            for row in rows:
                total_customer = row[0]
            #Find the customer whose number of order matches with the number of menus
            for i in range(total_customer):
                sql3 = "SELECT count(*) FROM public.order WHERE sid=%(id)s AND cid='" + str(i) + "';"
                cur.execute(sql3, {"id": args.id})
                rows = cur.fetchall()
                for row in rows:
                    total_order = row[0]
                if total_menu == total_order:
                    print("Customer ID:", i)

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
