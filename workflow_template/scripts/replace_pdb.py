#!/usr/bin/env python3

"""
This script replaces a PDB file in a HADDOCK param file.

Users need to provide a HADDOCK-compliant, JSON-formatted parameter file,
a PDB file to insert in the aforementioned parameter file and the index of
the PDB file they want to replace.

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
        '-pdb',
        '--pdb_file',
        nargs='?',
        required=True,
        help='Path to the PDB file'
    )
    parser.add_argument(
        '-i',
        '--index',
        nargs='?',
        type=int,
        required=True,
        help='Which PDB to replace? 1-indexed'
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
            # Since it's not JSON it must be PDB
            # Even though it shouldn't be an issue follow best practice
            # and wrap this in with to do it line-by-line
            for line in in_file:
                lines.append(line)
            loaded_file = ''.join(lines)
    return loaded_file


def replace_pdb(param_file, pdb_file, index):
    """Replace the pdb file in param_file with index index with pdb_file."""
    param_file['partners']["{:d}".format(index)]['raw_pdb'] = pdb_file
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
    pdb_file = load_file_to_memory(args.pdb_file)

    param_file = replace_pdb(param_file, pdb_file, args.index)
    write_param_file(param_file)

if __name__ == '__main__':
    main()
