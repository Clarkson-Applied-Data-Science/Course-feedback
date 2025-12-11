from flask import Flask
from flask import render_template
from flask import request, session, redirect, send_from_directory
from flask_session import Session
from datetime import timedelta
from models.user import user
from models.course import course
from models.feedback import feedback
import time
from datetime import datetime

app = Flask(__name__, static_url_path='')

app.config['SECRET_KEY'] = 'sdfvbgfdjeR5y5r'
app.config['SESSION_PERMANENT'] = True
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=5)
sess = Session()
sess.init_app(app)


@app.route('/')
def home():
    return redirect('/main')


@app.route('/main')
def main():
    if checkSession() == False:
        return redirect('/login')
    if session['role'] != 'admin':
        return redirect('/courses/list_courses')

    u = user()
    c = course()
    f = feedback()

    users_by_role = u.get_stats_users_by_role()
    stats_users = [{row["role"]: row["count"]} for row in users_by_role]

    courses_by_dept = c.get_stats_courses_by_department()
    stats_courses = [{row["departmentName"]: row["count"]}
                     for row in courses_by_dept]

    course_rating_avg = f.get_stats_course_ratings()
    pending_feedback = f.get_stats_pending_count()
    new_suggestions_course = c.get_new_course_stats()
    feedback_by_user = f.get_stats_feedback_by_user()
    feedback_length_distribution = f.get_stats_feedback_length_distribution()
    feedback_char_by_course = f.get_stats_feedback_char_by_course()
    avg_courses_per_department = c.get_stats_avg_courses_per_department()
    return render_template('main.html', title='Main menu', stats={
        "total_users": sum([list(d.values())[0] for d in stats_users]),
        "total_courses": sum([list(d.values())[0] for d in stats_courses]),
        "users": stats_users,
        "courses": stats_courses,
        "pending_feedback": pending_feedback,
        "new_suggestions_course": new_suggestions_course,
        "feedback_by_user": feedback_by_user,
        "feedback_length_distribution": feedback_length_distribution,
        "feedback_char_by_course": feedback_char_by_course,
        "course_rating_avg": course_rating_avg,
        "avg_courses_per_department": avg_courses_per_department,
    })


@app.context_processor
def inject_user():
    return dict(me=session.get('user'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    un = request.form.get('name')
    pw = request.form.get('password')

    if un is not None and pw is not None:
        u = user()
        if u.tryLogin(un, pw):
            print(f"login ok as {u.data[0]['email']}")
            session['user_id'] = u.data[0][u.pk]
            session['role'] = u.data[0]['role']
            session['user'] = u.data[0]
            session['active'] = time.time()
            if session['role'] == "admin":
                return redirect('main')
            else:
                return redirect('/courses/list_courses')
        else:
            print("login failed")
            return render_template('login.html', title='Login', msg='Incorrect username or password.')

    m = 'Welcome back'
    return render_template('login.html', title='Login', msg=m)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if session.get('user') is not None:
        del session['user']
        del session['user_id']
        del session['role']
        del session['active']
    return render_template('login.html', title='Login', msg='Welcome back')


@app.route('/users/manage', methods=['GET', 'POST'])
def manage_user():
    if checkSession() == False:
        return redirect('/login')
    o = user()
    action = request.args.get('action')
    pkval = request.form.get('pkval')
    create = request.args.get('create')
    if action is not None and action == 'delete':
        o.deleteById(pkval)
        del session['user']
        del session['user_id']
        del session['role']
        del session['active']
        return render_template('login.html', title='Login', msg='You have logged out.')

    if action is not None and action == 'insert':
        d = {}
        d['name'] = request.form.get('name')
        d['email'] = request.form.get('email')
        d['role'] = request.form.get('role')
        d['password'] = request.form.get('password')
        d['password2'] = request.form.get('password2')
        d['graduationDate'] = request.form.get('graduationDate')

        o.set(d)
        if o.verify_new():
            o.insert()
            return render_template('ok_dialog.html', msg=f"User {o.data[0][o.pk]} added.")
        else:
            return render_template('users/add.html', obj=o)
    if action is not None and action == 'update':
        o.getById(pkval)
        o.data[0]['name'] = request.form.get('name')
        o.data[0]['email'] = request.form.get('email')
        o.data[0]['role'] = request.form.get('role')
        o.data[0]['password'] = request.form.get('password')
        o.data[0]['password2'] = request.form.get('password2')
        o.data[0]['graduationDate'] = request.form.get('graduationDate')
        if o.verify_update():
            o.update()
            return render_template('ok_dialog.html', msg="User updated. ")
        else:
            return render_template('users/manage.html', obj=o)

    if create == 'new':
        o.createBlank()
        return render_template('users/add.html', obj=o)
    else:
        o.getById(pkval)
        return render_template('users/manage.html', obj=o)


@app.route('/courses/manage', methods=['GET', 'POST'])
def manage_course():
    if checkSession() == False:
        return redirect('/login')
    o = course()
    u = user()
    action = request.args.get('action')
    suggest = request.args.get('suggest')
    create = request.args.get('create')
    pkval = request.form.get('pkval')

    if action is not None and action == 'delete':
        o.deleteById(pkval)
        return render_template('ok_dialog.html', msg=f"Record ID {pkval} Deleted.")
    if action is not None and action == 'insert':
        d = {}
        d['courseName'] = request.form.get('courseName')
        d['description'] = request.form.get('description')
        d['semesterOffered'] = request.form.get('semesterOffered')
        d['departmentName'] = request.form.get('department')
        d['startDate'] = request.form.get('startDate')
        d['endDate'] = request.form.get('endDate')
        d['instructor'] = request.form.get('instructor')
        if suggest is not None:
            d['isSuggestedBy'] = session['user_id']

        o.set(d)
        if o.verify_new():
            o.insert()
            return render_template('ok_dialog.html', msg="Course added.")
        else:
            if suggest is None:
                o.data[0]['departments'] = o.departments
                o.data[0]['semester'] = o.semester
                u.getByField('role', 'instructor')
                o.data[0]['instructors'] = u.data
                return render_template('courses/add.html', obj=o)
            else:
                o.data[0]['departments'] = o.departments
                o.data[0]['semester'] = o.semester
                return render_template('courses/suggest_course.html', obj=o)
    if action is not None and action == 'update':
        o.getById(pkval)

        o.data[0]['courseName'] = request.form.get('courseName')
        o.data[0]['description'] = request.form.get('description')
        o.data[0]['semesterOffered'] = request.form.get('semesterOffered')
        o.data[0]['instructor'] = request.form.get('instructor')
        o.data[0]['startDate'] = datetime.strptime(
            request.form.get('startDate'), "%Y-%m-%d").date()
        o.data[0]['endDate'] = datetime.strptime(
            request.form.get('endDate'), "%Y-%m-%d").date()
        o.data[0]['departmentName'] = request.form.get('department')
        if o.verify_update():
            o.update()
            return render_template('ok_dialog.html', msg="Course updated. ")
        else:
            o.data[0]['departments'] = o.departments
            o.data[0]['semester'] = o.semester
            u.getByField('role', 'instructor')
            o.data[0]['instructors'] = u.data
            return render_template('courses/manage.html', obj=o)

    if create == 'new':
        o.createBlank()
        o.data[0]['departments'] = o.departments
        o.data[0]['semester'] = o.semester
        u.getByField('role', 'instructor')
        o.data[0]['instructors'] = u.data
        return render_template('courses/add.html', obj=o)
    else:
        o.getById(pkval)
        o.data[0]['departments'] = o.departments
        o.data[0]['semester'] = o.semester
        u.getByField('role', 'instructor')
        o.data[0]['instructors'] = u.data
        return render_template('courses/manage.html', obj=o)


@app.route('/feedbacks/manage', methods=['GET', 'POST'])
def manage_feedback():
    if checkSession() == False:
        return redirect('/login')
    o = feedback()
    action = request.args.get('action')
    create = request.args.get('create')
    pkval = request.form.get('pkval')

    if action is not None and action == 'delete':
        o.deleteById(pkval)
        return render_template('ok_dialog.html', msg=f"Feedback ID {pkval} Deleted.")

    if action is not None and action == 'insert':
        d = {}
        d['feedbackText'] = request.form.get('feedbackText')
        d['rating'] = request.form.get('rating')
        d['dateGiven'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        d['status'] = "pending"
        d['courseID'] = request.form.get('courseID')
        d['uuid'] = session['user_id']

        o.set(d)
        if o.verify_new():
            o.insert()
            return render_template('ok_dialog.html', msg=f"Feedback {o.data[0][o.pk]} added.")
        else:
            f = feedback()
            f.getByFields({"uuid": session['user_id']}, op="AND")
            given_course_ids = [row['courseID'] for row in f.data]
            c = course()
            c.getNotIn('courseID', given_course_ids)
            o.data[0]['courses'] = {row['courseID']: row['courseName'] for row in c.data}
            return render_template('feedbacks/add.html', obj=o)
    if action is not None and action == 'update':
        o.getById(pkval)
        if session['role'] == 'admin':
            o.data[0]['status'] = "approved"
        else:
            print(o)
            o.data[0]['feedbackText'] = request.form.get('feedbackText')
            o.data[0]['rating'] = request.form.get('rating')
            o.data[0]['courseID'] = request.form.get('courseID')

        if o.verify_update():
            o.update()
            return render_template('ok_dialog.html', msg="Feedback updated.")
        else:
            if session['role'] == 'admin':
                return redirect('/feedbacks/list_feedback')
            f = feedback()
            f.getByFields({"uuid": session['user_id']}, op="AND")
            given_course_ids = [row['courseID'] for row in f.data]
            c = course()
            c.getNotIn('courseID', given_course_ids)
            o.data[0]['courses'] = {row['courseID']: row['courseName'] for row in c.data}
            return render_template('feedbacks/manage.html', obj=o)

    if create == 'new':
        o.createBlank()
    else:
        o.getById(pkval)

    f = feedback()
    f.getByFields({"uuid": session['user_id']}, op="AND")
    given_course_ids = [row['courseID'] for row in f.data]
    c = course()
    c.getNotIn('courseID', given_course_ids)
    o.data[0]['courses'] = {row['courseID']: row['courseName'] for row in c.data}
    if create == 'new':
        return render_template('feedbacks/add.html', obj=o)
    else:
        return render_template('feedbacks/manage.html', obj=o)


@app.route('/session', methods=['GET', 'POST'])
def session_test():
    print(session)
    return f"{session}"


@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


def checkSession():
    if 'active' in session.keys():
        timeSinceAct = time.time() - session['active']

        if timeSinceAct > 500:
            session['msg'] = 'Your session has timed out.'
            return False
        else:
            session['active'] = time.time()
            return True
    else:
        return False


@app.route('/users/list_users')
def list_users():
    if checkSession() == False:
        return redirect('/login')
    o = user()
    uuid = request.args.get('uuid')
    if uuid is None:
        o.getAll()
        return render_template('users/list.html', obj=o)


@app.route('/courses/list_courses')
def list_courses():
    if checkSession() == False:
        return redirect('/login')
    o = course()
    courseID = request.args.get('courseID')
    if courseID is None:
        o.getByField('isSuggestedBy', None)
        return render_template('courses/list.html', obj=o)


@app.route('/courses/suggest_course')
def suggest_courses():
    if checkSession() == False:
        return redirect('/login')
    o = course()
    o.createBlank()
    o.data[0]['semester'] = o.semester
    o.data[0]['departments'] = o.departments
    return render_template('courses/suggest_course.html', obj=o)


@app.route('/feedbacks/list_feedback')
def list_feedback():
    if checkSession() == False:
        return redirect('/login')
    o = feedback()
    c = course()
    if session['role'] == 'admin':
        o.getByField('status', 'pending')
    if session['role'] == 'instructor':
        o.get_with_course_and_instructor(session['user_id'])
        return render_template('feedbacks/list.html', obj=o)

    feedbackID = request.args.get('feedbackID')
    if feedbackID is None and session['role'] != 'admin':
        o.getByField('uuid', session['user_id'])

    for co in o.data:
        c = course()
        c.getById(co['courseID'])
        if len(c.data) > 0:
            co['courseName'] = c.data[0]['courseName']
        else:
            co['courseName'] = "Unknown Course"
    return render_template('feedbacks/list.html', obj=o)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
