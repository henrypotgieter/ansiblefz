import os
import mysql.connector as mysql
from dotenv import load_dotenv


class Sqlconn(object):
    def __init__(self):
        load_dotenv(".env")
        self.HOST = os.getenv("MYSQL_HOST")
        self.DB = os.getenv("MYSQL_DB")
        self.USER = os.getenv("MYSQL_USER")
        self.PASS = os.getenv("MYSQL_PASS")

    def sql_read(self, query):
        self.db_conn = mysql.connect(
            host=self.HOST, database=self.DB, user=self.USER, password=self.PASS
        )
        self.c = self.db_conn.cursor()
        self.c.execute(query)
        data = self.c.fetchall()
        self.db_conn.close()
        return data

    def sql_write(self, query):
        self.db_conn = mysql.connect(
            host=self.HOST, database=self.DB, user=self.USER, password=self.PASS
        )
        self.c = self.db_conn.cursor()
        data = self.c.execute(query)
        self.db_conn.commit()
        self.db_conn.close()
        return data

    def categories(self):
        tuples = self.sql_read("SELECT host_category FROM category")

        categories = []
        for category in tuples:
            categories.append(category[0])
        return categories

    def directory(self, host_category):
        tuples = self.sql_read(
            "SELECT playbook_dir FROM category WHERE host_category = '"
            + host_category
            + "'"
        )
        return tuples[0][0]

    def playbooks(self, host_category):
        tuples = self.sql_read(
            "SELECT scriptname FROM scripts WHERE host_category = '"
            + host_category
            + "' and active = 1"
        )

        scriptnames = []
        for script in tuples:
            scriptnames.append(script[0])
        return scriptnames

    def filedata(self, scriptname):
        tuples = self.sql_read(
            "SELECT filename FROM scripts WHERE scriptname = '" + scriptname + "'"
        )
        return list(tuples[0])

    def category_desc(self, category_name):
        tuples = self.sql_read(
            "SELECT description FROM category WHERE host_category ='"
            + category_name
            + "'"
        )
        return tuples[0][0]

    def script_desc(self, category_name, script_name):
        tuples = self.sql_read(
            "SELECT description FROM scripts WHERE host_category ='"
            + category_name
            + "' AND scriptname = "
            + script_name
        )
        return tuples[0][0]
