from models.baseObject import baseObject
class course(baseObject):
    def __init__(self):
        self.setup()  
        self.departments =  ["Data science", 'Computer Science', 'Mathematics', 'Physics', 'Chemistry']
        self.semester = ["Fall", "Spring", "Summer"]
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
    def get_course_stats_by_department(self):
        self.data = []
        sql = f"SELECT departmentName, COUNT(*) AS cnt FROM `{self.tn}` where isSuggestedBy IS NULL GROUP BY departmentName;"
        self.cur.execute(sql)
        for row in self.cur:
            self.data.append({
                 row["departmentName"]: row["cnt"]
             }) 
    def get_new_course_stats(self):
        self.data = []
        sql = f"SELECT COUNT(*) AS cnt FROM `{self.tn}` where isSuggestedBy IS NOT NULL;"
        self.cur.execute(sql)
        row = self.cur.fetchone()
        return row["cnt"]
    def get_stats_courses_by_department(self):
        self.data = []
        sql = f'''
            SELECT departmentName, COUNT(*) AS count
            FROM `{self.tn}`
            GROUP BY departmentName
        '''
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        self.data = rows
        return rows
    def get_stats_avg_courses_per_department(self):
        sql = f'''
            SELECT AVG(course_count) AS avg_courses_per_department
            FROM (
              SELECT departmentName, COUNT(*) AS course_count
              FROM `{self.tn}`
              GROUP BY departmentName
            ) t
        '''
        self.cur.execute(sql)
        row = self.cur.fetchone()
        return row["avg_courses_per_department"] or 0

            
     