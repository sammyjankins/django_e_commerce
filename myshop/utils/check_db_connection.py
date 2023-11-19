import os
from time import sleep

import psycopg2


def postgres_test():
    try:
        conn = psycopg2.connect(f"dbname={os.environ.get('DB_NAME')} "
                                f"user={os.environ.get('DB_USER')} "
                                f"host={os.environ.get('DB_HOST')} "
                                f"password={os.environ.get('DB_PASSWORD')} "
                                f"connect_timeout=1 ")
        conn.close()
        return True
    except:
        return False


while not postgres_test():
    sleep(3)
    continue
else:
    print('### DB IS UP ###')
