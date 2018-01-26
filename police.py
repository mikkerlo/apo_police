#!/usr/local/bin/python3
import mystem
import utils
import logging
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(description="This program calling apo police for your list")
    parser.add_argument('filename', help='Filename for apo police')
    parser.add_argument('-v', '--verbosity', help='increase output verbosity', action='count')
    cli_args = parser.parse_args()
    return cli_args


def main():
    cli_args = parse_arguments()
    filename = cli_args.filename
    verbosity = cli_args.verbosity

    if verbosity == 0:
        utils.setup_logging(logging.ERROR)
    elif verbosity == 1:
        utils.setup_logging(logging.INFO)
    elif verbosity == 2:
        utils.setup_logging(logging.DEBUG)

    temp_data = utils.read_from_file(filename)
    names = mystem.process_names(temp_data)
    print(*sorted(names), sep='\n')


if __name__ == '__main__':
    main()
