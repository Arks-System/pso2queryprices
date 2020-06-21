#!/usr/bin/python3

import argparse
import logging
import requests

ENDPOINT="http://db.kakia.org/item/search"
logformat="%(asctime)s %(levelname)s - %(message)s"

def main(args):
    print(args.items)

    for e in args.items:
        item = query(e)
        logging.debug(item)
        print(f"{item['EnName']} ({item['JpName']}):")

        for price in item['PriceInfo']:
            ship = "{:02d}".format(int(price['Ship']))
            meseta = "{:,}".format(price['Price']).replace(",", " ").rjust(16)
            print(f"  Ship {ship}: {meseta} (last updated: {price['LastUpdated']})")


def query(item):
    params = {
        "name": item,
    }
    r = requests.get(ENDPOINT, params=params)

    if (r.status_code != 200):
        logging.warn(f"{r.status_code}")

    data = r.json()[0]

    data["PriceInfo"] = sorted(data["PriceInfo"], key=lambda  k: k["Ship"])

    return (data)

if (__name__ == '__main__'):
    PARSER = argparse.ArgumentParser(description='Query PSO2JP prices')
    PARSER.add_argument('items', action="store", nargs="*", help="List of items to query prices")
    PARSER.add_argument('-v', action='store_true', help='Verbose', default=False, required=False)

    args = PARSER.parse_args()
    if (args.v):
        logging.basicConfig(format=logformat, level = logging.INFO)
    else:
        logging.basicConfig(format=logformat, level = logging.ERROR)

    main(args)
