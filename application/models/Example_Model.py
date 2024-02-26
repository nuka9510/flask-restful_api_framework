from system import Model
from system.core.database import db
from sqlalchemy import text

# class Example_Model(Model):
#     def example(self):
#         sql = '''[QUERY]'''

#         self.execute(sql)
#         res = self.fetchall()
#         self.close()
#         return res

class Example_Model():
    def example(self):
        sql = text('''[QUERY]''')

        res = db.session.execute(sql).fetchall()
        return res