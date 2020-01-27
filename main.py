#!/usr/bin/env python3
"""
Entrypoint for the pay calculator service 
"""

import argparse
import daemon
from cal_setup import get_calendar_service


def main(args):
    """ Main entry point of the app """
    cal_service = get_calendar_service()

    daemon.main(cal_service, args.id, args.rate)


if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()

    # Required positional argument
    parser.add_argument("id", help="The ID of the calendar to manipulate")
    parser.add_argument("rate", type=float, help="Hourly pay rate")

    args = parser.parse_args()
    main(args)

