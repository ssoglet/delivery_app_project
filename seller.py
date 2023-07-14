import time
import argparse
from helpers.connection import conn

def main(args):
    try:
        cur = conn.cursor()

        #Print information of the entered ID seller
        if args.option == "info":
            print("***Information of Seller***")
            sql = "SELECT * FROM seller WHERE id=%(id)s;"
            cur.execute(sql, {"id": args.id})
            rows = cur.fetchall()
            for row in rows:
                print("ID:", row[0])
                print("Name:", row[1])
                print("Phone Number:", row[2])
                print("Local:", row[3])
                print("Email:", row[4])

        #Update seller information into the entered information
        elif args.option == "update":
            if args.property[0] == "name":
                # sql = "UPDATE seller SET name=%(name)s WHERE id=%(id)s;"
                sql = "UPDATE seller SET name='" + str(args.property[1]) + "'WHERE id=%(id)s;"
                # cur.execute(sql, ({"name": args.property[1]}, {"id": args.id}))
                cur.execute(sql, {"id": args.id})
            elif args.property[0] == "phone":
                sql = "UPDATE seller SET phone='" + str(args.property[1]) + "'WHERE id=%(id)s;"
                cur.execute(sql, {"id": args.id})
            elif args.property[0] == "local":
                sql = "UPDATE seller SET local='" + str(args.property[1]) + "'WHERE id=%(id)s;"
                cur.execute(sql, {"id": args.id})
            elif args.property[0] == "email" or args.property[0] == "domain":
                sql = "UPDATE seller SET domain='" + str(args.property[1]) + "'WHERE id=%(id)s;"
                cur.execute(sql, {"id": args.id})
            elif args.property[0] == "passwd" or args.property[0] == "password":
                sql = "UPDATE seller SET passwd='" + str(args.property[1]) + "'WHERE id=%(id)s;"
                cur.execute(sql, {"id": args.id})
            conn.commit()

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
