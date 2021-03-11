#!/usr/bin/env python3

"""
This script replaces a tbl file in a HADDOCK param file.

Users need to provide a HADDOCK-compliant, JSON-formatted parameter file,
a tbl file to insert in the aforementioned parameter file and the type of
tbl file they want to replace, one of ambig, unambig, hbond and dihedral.

Will produce a param file in the current directory non-destructively.
"""

__version__ = '0.1.0'
__author__ = 'Panagiotis Koukos'

import json
import argparse
from os import path, listdir


def _check_input():
    """Parse and sanity-check the command line arguments."""
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        '-param',
        '--parameter_file',
        nargs='?',
        required=True,
        help='Path to the parameter file'
    )
    parser.add_argument(
        '-tbl',
        '--tbl_file',
        nargs='?',
        required=True,
        help='Path to the tbl file'
    )
    parser.add_argument(
        '-type',
        '--tbl_type',
        nargs='?',
        choices=['ambig', 'unambig', 'hbond', 'dihedral'],
        required=True,
        help=(
            'Which tbl to replace? Only allows ambig, '
            'unambig, hbond and dihedral'
        )
    )

    args = parser.parse_args()
    return args


def load_file_to_memory(input_file):
    """Read a provided file into memory."""
    ftype = path.splitext(input_file)[-1]
    with open(input_file) as in_file:
        if ftype.lower() == '.json':
            loaded_file = json.load(in_file)
        else:
            lines = []
            # Since it's not JSON it must be tbl
            # Even though it shouldn't be an issue follow best practice
            # and wrap this in with to do it line-by-line
            for line in in_file:
                lines.append(line)
            loaded_file = ''.join(lines)

            # Set it to None if nothing was read so that the json field
            # in turn is set to null
            if len(loaded_file) == 0:
                loaded_file = None
    return loaded_file


def replace_tbl(param_file, tbl_file, tbl_type):
    """Replace the tbl_type tbl file in param_file with tbl_file."""
    # Poor man's switch-case
    tbl_field = {
        'ambig': 'tblfile',
        'hbond': 'hbondfile',
        'unambig': 'unambigtblfile',
        'dihedral': 'dihedralfile'
    }

    param_file[tbl_field[tbl_type]] = tbl_file
    return param_file


def write_param_file(param_file):
    """Write the modified param file to disk."""
    files_present = listdir('.')
    param_file_present = any([_ == 'job_params.json' for _ in files_present])
    if param_file_present is False:
        fname = 'job_params.json'
    else:
        # job_params.json exists. Start going through the list of files
        # named job_params_X.json where X is int until you find one that
        # does not exist
        i = 1
        while "job_params_{:d}.json".format(i) in files_present:
            i += 1
        fname = "job_params_{:d}.json".format(i)

    with open(fname, 'w') as out_file:
        print(
            json.dumps(
                param_file,
                indent=4,
                sort_keys=True
            ),
            file=out_file
        )


def main():
    args = _check_input()
    param_file = load_file_to_memory(args.parameter_file)
    tbl_file = load_file_to_memory(args.tbl_file)

    param_file = replace_tbl(param_file, tbl_file, args.tbl_type)
    write_param_file(param_file)

if __name__ == '__main__':
    main()
