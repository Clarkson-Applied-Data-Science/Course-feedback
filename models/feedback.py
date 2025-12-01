
from pathlib import Path
import pymysql
import datetime
from models.baseObject import baseObject
import hashlib

class feedback(baseObject):
    def __init__(self):
        self.setup()   
    def verify_new(self):
        self.errors = []
        
        f = feedback() 
        f.getByFields({"uuid": self.data[0]['uuid'], "courseID": self.data[0]['courseID']}, op="AND")

        if len(f.data) > 0:
            self.errors.append(f"You alread gave a feedback for this course.")
        
        if len(self.errors) == 0:
            return True
        else:
            return False
    def verify_update(self):
        self.errors = []
        f = feedback() 
        f.getByFields({"uuid": self.data[0]['uuid'], "courseID": self.data[0]['courseID']}, op="AND")

        if len(f.data) > 0:
            self.errors.append(f"You alread gave a feedback for this course.")
        
        if len(self.errors) == 0:
            return True
        else:
            return False
    
   