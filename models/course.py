from models.baseObject import baseObject
from datetime import datetime, date


class course(baseObject):
    def __init__(self):
        self.setup()
        self.departments = ["Data science", 'Computer Science',
                            'Mathematics', 'Business Analytics', 'Chemistry']
        self.semester = ["Fall", "Spring", "Summer"]

    def verify_new(self):
        self.errors = []
        #
        if len(self.data[0]['courseName']) <= 2:
            self.errors.append('Name must be greater than two character.')
        c = course()
        c.getByField('courseName', self.data[0]['courseName'])
        if len(c.data) > 0:
            self.errors.append(
                f"This course already exist ({self.data[0]['courseName']})")

        desc_length = len(self.data[0]['description'].strip())
        if desc_length < 250 or desc_length > 600:
            self.errors.append(
                "Your course description must be between 250 and 600 characters."
            )
        if self.data[0]['startDate'] == '' or self.data[0]['endDate'] == '':
            self.errors.append(
                "Start date and end date must be provided."
            )
        else:
            start = self.data[0]['startDate']
            end = self.data[0]['endDate']
            if isinstance(start, str):
                start = datetime.strptime(start, "%Y-%m-%d").date()
            if isinstance(end, str):
                end = datetime.strptime(end, "%Y-%m-%d").date()

            if start > end:
                self.errors.append("Start date cannot be later than end date.")
        if len(self.errors) == 0:
            return True
        else:
            return False

    def verify_update(self):
        self.errors = []
        #
        if len(self.data[0]['courseName']) <= 2:
            self.errors.append('Name must be greater than two character.')
        c = course()
        c.getByField('courseName', self.data[0]['courseName'])
        if len(c.data) > 0 and c.data[0][c.pk] != self.data[0][self.pk]:
            self.errors.append(
                f"This course already exist ({self.data[0]['courseName']})")
        #
        desc_length = len(self.data[0]['description'].strip())
        if desc_length < 250 or desc_length > 600:
            self.errors.append(
                "Your course description must be between 250 and 600 characters."
            )
        if self.data[0]['startDate'] == '' or self.data[0]['endDate'] == '':
            self.errors.append(
                "Start date and end date must be provided."
            )
        else:
            start = self.data[0]['startDate']
            end = self.data[0]['endDate']
            if isinstance(start, str):
                start = datetime.strptime(start, "%Y-%m-%d").date()
            if isinstance(end, str):
                end = datetime.strptime(end, "%Y-%m-%d").date()

            if start > end:
                self.errors.append("Start date cannot be later than end date.")

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
