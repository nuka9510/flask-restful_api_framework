import mysql.connector, decimal, datetime
from mysql.connector import errorcode
from application import config

class Model():
    def __init__(self):
        '''
        method

        execute(sql: str[, *data: str|int|...])

        fetchall()
        
        fetchone()
        
        close()
        '''
        self.__connect()

    def __connect(self):
        try:
            self.con = mysql.connector.connect(**config['DATABASE'])
            self.cur = self.con.cursor()
        except mysql.connector.Error as err:
            return err

    def __json_convert(self, value):
        if isinstance(value, datetime.date):
            return value.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(value, decimal.Decimal):
            return str(value)
        else:
            return value

    def execute(self, sql, *data):
        '''
        execute(sql: str[, *data: str|int|...])

        sql문을 실행시킨다.
        '''
        if not self.con.is_connected():
            self.__connect()
        
        if not data:
            self.cur.execute(sql)
        else:
            self.cur.execute(sql, data)

    def fetchall(self):
        '''
        fetchall()

        select된 모든 row를 불러온다.
        '''
        column_names = self.cur.column_names
        result = list()

        for val in iter(self.cur.fetchall()):
            row = list()
            for i in val:
                row.append(self.__json_convert(i))

            result.append(dict(zip(column_names, row)))

        return result

    def fetchone(self):
        '''
        fetchone()
        
        select된 row중 가장 첫 번째 row를 불러온다.
        '''
        column_names = self.cur.column_names
        row = list()

        for val in self.cur.fetchone():
            row.append(self.__json_convert(val))

        return dict(zip(column_names, row))
    
    def insert_id(self):
        '''
        insert_id()
        '''
        return self.cur.lastrowid

    def close(self):
        '''
        close()

        db connection을 끊는다.
        '''
        self.cur.close()
        self.con.close()