from system import Model

class Example_Model(Model):
    def example(self):
        sql = '''[QUERY]'''
        self.execute(sql)
        res = self.fetchall()
        self.close()
        return res