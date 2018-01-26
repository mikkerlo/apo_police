import os
import subprocess
import json
import logging


def read_from_file(filename):
    with open(filename) as fin:
        return fin.read()


def write_in_file(filename, data):
    with open(filename, 'w') as fout:
        fout.write(data)


def get_output_from_program(*args):
    subprocess.run(args=args)


def iload_json(buff, decoder=None, _w=json.decoder.WHITESPACE.match):
    """Generate a sequence of top-level JSON values declared in the
    buffer."""
    decoder = decoder or json._default_decoder
    idx = _w(buff, 0).end()
    end = len(buff)

    try:
        while idx != end:
            (val, idx) = decoder.raw_decode(buff, idx=idx)
            yield val
            idx = _w(buff, idx).end()
    except ValueError as exc:
        raise ValueError('%s (%r at position %d).' % (exc, buff[idx:], idx))


def setup_logging(level):
    logging.basicConfig(level=level)