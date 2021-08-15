import sqlite3
from sqlite3 import Error
import os


class DBLite(object):
    DB_FILE_NAME = ''
    CONN = None
    CURSOR = None
    MEDIA_TABLE = 'media'

    def set_db_file_name(self, db_file_name):
        self.DB_FILE_NAME = db_file_name

    def dict_factory(self, cursor, row):
        # https://stackoverflow.com/a/3300514
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def __init__(self, db_file, clear_tables=False, use_dict=False):
        try:
            if os.path.exists(db_file):
                self.connect(db_file, use_dict)
            else:
                try:
                    self.connect(db_file)
                    self.create_base_tables()
                except Error as e:
                    print("ERR: {} ".format(e))
                    clear_tables = False

            if clear_tables:
                self.truncate_table()

        except Error as e:
            print(f"SQLITE ERR:{e}")

    def fetch_all(self, qry):
        self.CURSOR.execute(qry)
        return self.CURSOR.fetchall()

    def connect(self, db_file, use_dict):
        """ create a database connection to a SQLite database """
        conn = None
        try:
            self.CONN = sqlite3.connect(db_file)
            if use_dict:
                self.CONN.row_factory = self.dict_factory
            self.CURSOR = self.CONN.cursor()
            print(sqlite3.version)
        except Error as e:
            print(e)

    def close_conn(self):
        if self.CONN:
            self.CONN.close()

    def fetch_all(self, qry: str):
        self.CURSOR.execute(qry)
        return self.CURSOR.fetchall()

    def insert_many_into(self, rows: list):
        """

        :param rows: [(UID,kind,file_ext,file_name,src,notes,within_fcp,proxy_file)]
        :return:
        """

        self.CONN.executemany('INSERT INTO {} VALUES (?,?,?,?,?,?,?,?,?)'.format(self.MEDIA_TABLE), rows)
        self.CONN.commit()

    def truncate_table(self):
        qry = "DELETE FROM {}".format(self.MEDIA_TABLE)
        self.CONN.execute(qry)
        self.CONN.commit()

    def create_base_tables(self):
        # Create table
        # uid,kind,file_ext,file_name,src_path
        create_stmt = [
            "CREATE TABLE {}".format(self.MEDIA_TABLE),
            "(id INTEGER PRIMARY KEY AUTOINCREMENT,",
            "uid VARCHAR(60),",
            "kind VARCHAR(10),",
            "file_ext VARCHAR(5),",
            "file_name VARCHAR(50),",
            "src_path TEXT,",
            "notes TEXT,",
            "within_fcp INTEGER,",
            "proxy_file INTEGER",
            ")",
        ]
        # self.CONN.execute('''CREATE TABLE media
        #              (date text, trans text, symbol text, qty real, price real)''')

        self.CONN.execute(" ".join(create_stmt))
        self.CONN.commit()
