#!/usr/local/bin/python3
import mystem
import utils
import logging
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(description="This program calling apo police for your list")
    parser.add_argument('filename', help='filename for apo police')
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

    logging.info('Whop-Whop')
    logging.info('This is apo police siren!')
    logging.info('Our team surrounds your list')
    temp_data = utils.read_from_file(filename)
    logging.info('Environment completed successfully')
    logging.info('Estimate a situation')
    names = mystem.process_names(temp_data)
    logging.info('Today, without penalty, continue to be careful')
    print(*sorted(names), sep='\n')


if __name__ == '__main__':
    main()
