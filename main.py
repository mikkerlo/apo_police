#!/usr/local/bin/python3
import mystem
import utils
import logging


def main():
    logging.basicConfig(level=logging.INFO)
    temp_data = utils.read_from_file('kek')
    names = mystem.process_names(temp_data)
    print(*sorted(names), sep='\n')


if __name__ == '__main__':
    main()
