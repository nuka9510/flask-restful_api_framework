import mysql.connector, decimal, datetime
from mysql.connector import errorcode
from application.config import database

class Model():
    def __init__(self):
        try:
            self.con = mysql.connector.connect(**database.db)
            self.cur = self.con.cursor()
        except mysql.connector.Error as err:
            return err

    def connect(self):
        try:
            self.con = mysql.connector.connect(**database.db)
            self.cur = self.con.cursor()
        except mysql.connector.Error as err:
            return err


    def execute(self, sql, *data):
        if not self.con.is_connected():
            self.connect()
        
        self.cur.execute(sql, *data)

    def fetchall(self):
        column_names = self.cur.column_names
        result = list()
        for val in iter(self.cur.fetchall()):
            row = list()
            for i in val:
                row.append(self.json_serialize(i))

            result.append(dict(zip(column_names, row)))

        return result

    def fetchone(self):
        column_names = self.cur.column_names
        row = list()
        for val in self.cur.fetchone():
            row.append(self.json_serialize(val))
        return dict(zip(column_names, row))

    def close(self):
        self.cur.close()
        self.con.close()

    def json_serialize(self, value):
        if isinstance(value, datetime.date):
            return value.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(value, decimal.Decimal):
            return str(value)
        else:
            return value