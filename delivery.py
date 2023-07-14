import time
import argparse
from helpers.connection import conn

def main(args):
    try:
        cur = conn.cursor()

        #Status option
        #Print the delivering orders of entered delivery man
        if args.option == "status" and len(args.property) == 0:
            print("***Delivering Orders***")
            sql = "SELECT * FROM public.order WHERE delivery=%(id)s;"
            cur.execute(sql, {"id": args.id})
            rows = cur.fetchall()
            for row in rows:
                if "1" in row[8]:
                    print("Order ID:", row[0])

        #Change delivery status of entered number into delivered
        elif args.option == "status" and args.property[0] == "-e":
            sql = "UPDATE public.order SET deliv_st=2 WHERE delivery=%s AND order_id=%s;"
            cur.execute(sql, (args.id, args.property[1]))
            conn.commit()

        #Print all orders of entered delivery man
        elif args.option == "status" and args.property[0] == "-a":
            print("***All Orders***")
            sql = "SELECT * FROM public.order WHERE delivery=%(id)s;"
            cur.execute(sql, {"id": args.id})
            rows = cur.fetchall()
            for row in rows:
                print("Order ID:", row[0])
                if "0" in row[8]:
                    print("Delivery Status: Order")
                elif "1" in row[8]:
                    print("Delivery Status: Delivering")
                elif "2" in row[8]:
                    print("Delivery Status: Delivered")

    except Exception as err:
        print(err)
    pass

if __name__ == "__main__":
    start = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument("id", help="ID of Seller")
    parser.add_argument("option", help="Options of Seller")
    parser.add_argument("property", nargs=argparse.REMAINDER, help="Properties")
    args = parser.parse_args()
    main(args)