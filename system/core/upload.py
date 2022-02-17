import mysql.connector, decimal, datetime
from mysql.connector import errorcode
from application import db

class Model():
    def __init__(self):
        self.connect()

    def connect(self):
        try:
            self.con = mysql.connector.connect(**db)
            self.cur = self.con.cursor()
        except mysql.connector.Error as err:
            return err

    def execute(self, sql, *data):
        if not self.con.is_connected():
            self.connect()
        
        if not data:
            self.cur.execute(sql)
        else:
            self.cur.execute(sql, data)

    def fetchall(self):
        column_names = self.cur.column_names
        result = list()

        for val in iter(self.cur.fetchall()):
            row = list()
            for i in val:
                row.append(self.json_convert(i))

            result.append(dict(zip(column_names, row)))

        return result

    def fetchone(self):
        column_names = self.cur.column_names
        row = list()

        for val in self.cur.fetchone():
            row.append(self.json_convert(val))

        return dict(zip(column_names, row))

    def close(self):
        self.cur.close()
        self.con.close()

    def json_convert(self, value):
        if isinstance(value, datetime.date):
            return value.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(value, decimal.Decimal):
            return str(value)
        else:
            return value