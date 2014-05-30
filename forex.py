#!/usr/bin/env python3
"""
forex.py

Commandline tool for converting between currencies using data
from openexchangerates.org.

Requires an API key for openexchangerates.org which should be
provided as the environment variable OER_APP_ID.
"""
import argparse
import urllib.request
import urllib.error
import urllib.parse
from decimal import Decimal
from datetime import date, timedelta, datetime
import os
try:
    import simplejson as json
except ImportError:
    import json

URL_LATEST = 'http://openexchangerates.org/api/latest.json'
URL_HISTORICAL = 'http://openexchangerates.org/api/historical/{0}.json'

def main():
    parser = argparse.ArgumentParser(description="""Convert between two
                                        currencies using data from
                                        openexchangerates.org""",
                                    epilog="""Requires an API key for
                                        openexchangerates.org which should be
                                        provided as the environment variable
                                        OER_APP_ID.""")
    parser.add_argument('amount',
                        type=str,
                        help="Amount to convert")
    parser.add_argument('base_curr',
                        type=str,
                        help="3-letter base currency to convert from e.g. GBP")
    parser.add_argument('new_curr',
                        type=str,
                        help="3-letter currency to convert to e.g. USD")
    parser.add_argument('-d',
                        '--date',
                        type=is_date,
                        help="Date to use for historical rates (YYYY-MM-DD)")

    args = parser.parse_args()
    if args is not None:
        try:
            request_data = {'app_id': os.environ['OER_APP_ID']}
        except KeyError:
            parser.error("Environment variable OER_APP_ID is not set.")
        if args.date is not None:
            # Get historical data
            url = URL_HISTORICAL.format(args.date.isoformat())
        else:
            url = URL_LATEST
        try:
            forex_data = get_json(url, request_data)
        except Exception as e:
            parser.error(e)
        base_curr = args.base_curr.upper()
        new_curr = args.new_curr.upper()
        try:
            conv_rate = forex_data['rates'][new_curr] \
                        * Decimal(1) / forex_data['rates'][base_curr]
        except KeyError as e:
            parser.error("Invalid currency: {0}".format(e))
        result = Decimal(args.amount) * conv_rate
        print("{0:.3f} {1}".format(result, new_curr))
    else:
        parser.error("No arguments supplied.")

def is_date(input_date):
    """Checks whether the input date is a valid date."""
    try:
        day = datetime.strptime(input_date, '%Y-%m-%d').date()
    except ValueError:
        raise argparse.ArgumentTypeError(
            "Invalid date – must be in format YYYY-MM-DD"
            )
    return day

def get_json(url, data):
    """Gets JSON from URL, authenticating with data. Returns dictionary"""
    data = urllib.parse.urlencode(data)
    try:
        html = urllib.request.urlopen('{0}?{1}'.format(url, data))
    except urllib.error.URLError as e:
        raise Exception("{0} for {1}".format(e, url))
    except urllib.error.HTTPError as e:
        raise Exception("{0} for {1}".format(e, url))
    raw_json = html.read().decode('utf-8')
    forex_json = json.loads(raw_json, use_decimal=True)
    return forex_json

if __name__ == "__main__":
    main()
