import sys
import subprocess
import os
from io import StringIO
from typing import List
import pandas as pd

VERBOSE = True


def mdb_to_pandas(database_path: os.PathLike, tables_of_interest: List[bytes] = []):

    if len(tables_of_interest) > 0:
        tables = tables_of_interest
    else:
        # read out all table names and use them
        table_names = subprocess.Popen(["mdb-tables", "-1", database_path],
                                       stdout=subprocess.PIPE).communicate()[0]
        tables = table_names.splitlines()
        sys.stdout.flush()

    # Dump each table as a stringio using "mdb-export",
    out_tables = {}
    for rtable in tables:
        table = rtable.decode()
        if VERBOSE:
            print('running table:', table)
        if table != '':
            if VERBOSE:
                print("Dumping " + table)
            contents = subprocess.Popen(["mdb-export", database_path, table],
                                        stdout=subprocess.PIPE).communicate()[0]
            temp_io = StringIO(contents.decode())
            print(table, temp_io)
            out_tables[table] = pd.read_csv(temp_io)
    return out_tables
