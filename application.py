#Lang Tuang  |  11/15/2020
#The hardest assignment so far for me.

import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, g

DATABASE     = "hw13.db"
USERNAME    = "admin"
PASSWORD     = "password"
SECRET_KEY  = "nosecret"

app = Flask(__name__)
app.config.from_object(__name__)

#1connet to database
def db.connect():
    return sqlite3.connect (app.config['DATABASE'])

#2before_request decorator allows to create a func that will run before each request.
@app.before_request
def before_request():
    g.db = connnect_db()

#3teardown_request decorator allows to cleanup operations afrer requests.
@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

#4route for main page
@app.route('/')
def index():
    return redirect('/login')

#5 Teacher Login | Part2
@app.route('/login', methods = ['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin':
            error = 'Invalid Username.'
            return render_template ('login.html', error = error)
        elif request.form['password'] != 'password':
            error = 'WRONG password'
            return render_template('login.html', error = error)
        else:
            session ['logged_in'] = True
            return redirect(url_for('dashboard'))
    else:
        return render_template('login.html', error = error)

#6 Dashboard Page | Part3
@app.route('/dashboard', methods=['GET'])
def dashboard():
    if session['logged_in'] is not True:
        return redirect('/login')
    else:
        cur = g.db.execute('SELECT id, firstname, lastname from students')
        students = [dict(id=row[0], firstname=row[1], lastname=row[2])
                    for row in cur.fetchall()]

        cur = g.db.execute('SELECT id, qz_subject, questions, quiz_date from quiz')
        quizzes = [dict(quiz_id=row[0], subject=row[1], quiznum=row[2], date=row[3])
                   for row in cur.fetchall()]

        return render_template("dashboard.html", students=students, quizzes=quizzes)


#7 Add students to the class | Part4
@app.route('/student/add', methods=['GET', 'POST'])
def add_student():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    elif request.method == 'GET':
        return render_template("add_student.html")

    elif request.method == 'POST':
        g.db.execute('INSERT into Students (firstname, lastname) values (?, ?)',
                     [request.form['StudentFirstName'], request.form['StudentLastName']])
        g.db.commit()

    return redirect(url_for('dashboard'))

#8 Add quizzes to the class | Part5
@app.route('/quiz/add', methods=['GET', 'POST'])
def add_quiz():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    elif request.method == 'GET':
        return render_template('add_quiz.html')

    elif request.method == 'POST':
        g.db.execute('INSERT into Quiz (subject, quiznum , date) '
                     'values (?, ?, ?)', [request.form['QuizSubject'], request.form['QuizQuestions'],request.form['QuizDate']])

        g.db.commit()
    return redirect(url_for('dashboard'))

#9 View Quiz Results  | Part6
@app.route('/results', methods=['GET'])
def view_results():
    if session['logged_in'] is not True:
        return redirect('/login')
    else:
        cur = g.db.execute("""SELECT students.firstname, students.lastname, quiz.subject, results.score
                            FROM students
                            JOIN Results ON students.id = results.student_id
                            JOIN Quiz ON results.id = quiz.quiz_id;"""
                           )
        students = [dict(firstname=row[0], lastname=row[1], subject=row[2], score=row[3])
                    for row in cur.fetchall()]


        return render_template("results.html", students=students)

#10 Add a student's Quiz Result  | Part7
@app.route('/results/add', methods=['GET', 'POST'])
def add_result():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    elif request.method == 'GET':
        return render_template('add_score.html')

    elif request.method == 'POST':
        g.db.execute("INSERT into Results (studentid, quizid, score) values "
                     "(?, ?, ?)", (request.form['StudentID'], request.form['QuizID'], request.form['Score']))

        g.db.commit()
    return redirect('dashboard')

if __name__ == '__main__':
    app.run(debug=True)
