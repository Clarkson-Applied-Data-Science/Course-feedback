
from pathlib import Path
import pymysql
import datetime
from models.baseObject import baseObject
import hashlib

class course(baseObject):
    def __init__(self):
        self.setup()   
    def verify_new(self):
        self.errors = []
        #
        if len(self.data[0]['courseName']) <=2:
            self.errors.append('Name must be greater than two character.')
        c = course()
        c.getByField('courseName',self.data[0]['courseName'])
        if len(c.data) > 0:
            self.errors.append(f"This course already exist ({self.data[0]['courseName']})")
        
        if len(self.errors) == 0:
            return True
        else:
            return False
    def verify_update(self):
        self.errors = []
        #
        if len(self.data[0]['courseName']) <=2:
            self.errors.append('Name must be greater than two character.')
        c = course()
        c.getByField('courseName',self.data[0]['courseName'])
        if len(c.data) > 0 and c.data[0][c.pk] != self.data[0][self.pk]:
            self.errors.append(f"This course already exist ({self.data[0]['courseName']})")
        #
        if len(self.errors) == 0:
            return True
        else:
            return False
    def getNotIn(self, fieldname, values): 
        self.data = []
        if not values:   
            return self.getAll()
        placeholders = ','.join(['%s'] * len(values))
        sql = f"SELECT * FROM `{self.tn}` WHERE `{fieldname}` NOT IN ({placeholders});"
        self.cur.execute(sql, values)

        for row in self.cur:
            self.data.append(row)
   