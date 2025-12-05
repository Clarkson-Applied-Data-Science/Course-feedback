
from models.baseObject import baseObject
from models.course import course
from models.user import user


class feedback(baseObject):
    def __init__(self):
        self.setup()

    def verify_new(self):
        self.errors = []

        f = feedback()
        f.getByFields(
            {"uuid": self.data[0]['uuid'], "courseID": self.data[0]['courseID']}, op="AND")

        if len(f.data) > 0:
            self.errors.append(f"You alread gave a feedback for this course.")

        if len(self.errors) == 0:
            return True
        else:
            return False

    def verify_update(self):
        self.errors = []
        f = feedback()
        f.getByFields(
            {"uuid": self.data[0]['uuid'], "courseID": self.data[0]['courseID']}, op="AND")
        if len(self.data) == 1 and self.data[0]['status'] == 'approved':
            return True

        if len(f.data) > 0:
            self.errors.append(f"You already gave a feedback for this course.")

        if len(self.errors) == 0:
            return True
        else:
            return False

    def get_with_course_and_instructor(self, instructor_id):
        self.data = []
        c = course()
        u = user()
        sql = f"""
            SELECT
                f.*,
                c.courseName AS courseName,
                c.instructor AS instructorID,
                u.name AS name
            FROM `{self.tn}` f
            JOIN `{c.tn}` c
                ON c.courseID = f.courseID
            JOIN `{u.tn}` u 
                ON u.uuid = c.instructor
            WHERE c.instructor = %s 
            AND f.status != 'pending'
            ORDER BY f.feedbackID DESC
        """

        self.cur.execute(sql, (instructor_id,))
        rows = self.cur.fetchall()
        self.data = rows
        return rows

    def get_pending_feedback_count(self):

        sql = f"SELECT COUNT(*) AS cnt FROM `{self.tn}` WHERE status = 'pending';"
        self.cur.execute(sql)
        row = self.cur.fetchone()
        return row["cnt"]

    def get_stats_pending_count(self):
        sql = f"""
            SELECT COUNT(*) AS c
            FROM `{self.tn}`
            WHERE status = 'pending'
        """
        self.cur.execute(sql)
        row = self.cur.fetchone()
        return row["c"]

    def get_stats_feedback_by_user(self):
        self.data = []
        sql = f"""
            SELECT u.uuid,
                   u.name AS name,
                   COUNT(f.feedbackID) AS feedback_count,
                   AVG(LENGTH(f.feedbackText)) AS avg_chars
            FROM `{self.tn}` f
            JOIN users u ON u.uuid = f.uuid
            GROUP BY u.uuid, u.name
            ORDER BY feedback_count DESC
        """
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        self.data = rows
        return rows

    def get_stats_feedback_length_distribution(self):
        self.data = []
        sql = f"""
            SELECT
              CASE
                WHEN LENGTH(f.feedbackText) <= 50 THEN '0-50'
                WHEN LENGTH(f.feedbackText) <= 100 THEN '51-100'
                WHEN LENGTH(f.feedbackText) <= 200 THEN '101-200'
                ELSE '200+'
              END AS bucket,
              COUNT(*) AS count
            FROM `{self.tn}` f
            GROUP BY bucket
            ORDER BY bucket
        """
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        self.data = rows
        return rows

    def get_stats_feedback_char_by_course(self):
        self.data = []
        c = course()
        sql = f"""
            SELECT c.courseName AS course,
                   MAX(LENGTH(f.feedbackText)) AS max_chars,
                   AVG(LENGTH(f.feedbackText)) AS avg_chars,
                   COUNT(*) AS feedback_count
            FROM `{self.tn}` f
            JOIN `{c.tn}` c ON c.courseID = f.courseID
            GROUP BY c.courseID, c.courseName
            ORDER BY feedback_count DESC
        """
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        self.data = rows
        return rows
