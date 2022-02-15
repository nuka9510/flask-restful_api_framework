from system import Model

class Example_Model():
    def __init__(self):
        self.db = Model()

    def example(self):
        sql = '''[QUERY]'''
        self.db.execute(sql)
        res = self.db.fetchall()
        self.db.close()
        return res