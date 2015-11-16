#!/usr/bin/env python

""" Download files.
"""

import argparse
import csv
from subprocess import check_call
import multiprocessing

def download_single_file(entry):
    output_file = entry[0];
    link = entry[1];
    command = "wget -q --tries=600 --waitretry 600 -O {} {}".format(
            output_file, link);
    check_call(command.split());

def parse_args():
    parser = argparse.ArgumentParser(description=__doc__);
    parser.add_argument("summary", help="summary file");
    return parser.parse_args();

def main():
    args = parse_args();
    summary_file = args.summary;
    pool = multiprocessing.Pool(multiprocessing.cpu_count());
    with open(summary_file, 'r') as fin:
        csv_reader = csv.reader(fin);
        header = csv_reader.next();
        header = [str(item).strip() for item in header];
        link_idx = header.index("link");
        file_id_idx = header.index("file_id");
        file_idx = header.index("file");

        entries = [(row[file_idx], row[link_idx]) for row in csv_reader];

    pool.map(download_single_file, entries);

if __name__ == "__main__":
    main();
