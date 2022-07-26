
#what imports do I need?
import psycopg2

conn = psycopg2.connect(dsn)
curr = conn.cursor()
cur.execute(sql, (value1,value2))

def get_urm_degs_top_insts():
    """Query data from unified table to determine top institutions based on request restrictions"""
    conn = None
    try:
        #What do we need to modify here to have the config be what's coming from Ethan?
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.exectute("SELECT * from")

