from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os


app = Flask(__name__)
application = app

app.config.from_pyfile('config.py')

ip = os.getenv('ip')
PGUSER = str(os.getenv('PGUSER'))
PGPASSWORD = str(os.getenv('PGPASSWORD'))
DATABASE = str(os.getenv('DATABASE'))

POSTGRES_URI = f'postgresql://{PGUSER}:{PGPASSWORD}@{ip}/{DATABASE}'

app.config['SQLALCHEMY_DATABASE_URI'] = POSTGRES_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(app, metadata=metadata)
migrate = Migrate(app, db)

from models import Student, PlanOfStudy, Gradebook
    

@app.route('/')
def index():
    # fill_db()
    return render_template('index.html' )

@app.route('/schetchik', methods=['GET', 'POST'])
def schetchik():
    if request.method == 'POST':
        form_of_educ = request.form['select_form']
        student_count = Student.query.filter_by(education_form=form_of_educ).count()
        return render_template('schetchik.html', title='Счетчик', student_count=student_count, form_of_educ=form_of_educ)
    return render_template('schetchik.html', title='Счетчик', student_count=None)

@app.route('/disciplineinfo', methods=['GET', 'POST'])
def disciplineinfo():
    if request.method == 'POST':
        selected_discipline = request.form.get('discipline_name')
        try:
            hours = PlanOfStudy.query.filter_by(discipline=selected_discipline).first().hours
            otchet = PlanOfStudy.query.filter_by(discipline=selected_discipline).first().exam_or_test
        except:
            flash("Такой дисциплины несуществует", "danger")
            return render_template('disciplineinfo.html', title='Инфорация о дисциплине', hours=None)
        
        return render_template('disciplineinfo.html', title='Инфорация о дисциплине', hours=hours, otchet=otchet, selected_discipline=selected_discipline)
    
    return render_template('disciplineinfo.html', title='Инфорация о дисциплине', hours=None)

@app.route('/studentslist')
def studentslist():
    students_arr = Student.query.all()
    return render_template('studentslist.html', title='Список студентов', students=students_arr)

@app.route('/educationplanslist')
def educationplanslist():
    educationplans_arr = PlanOfStudy.query.all()
    return render_template('educationplanslist.html', title='Список учебных планов', educationplans = educationplans_arr)

@app.route('/createstudent', methods=['GET', 'POST'])
def createstudent():
    if request.method == 'POST':
        name = request.form.get('name')
        lastname = request.form.get('lastname')
        surname = request.form.get('surname')
        admission_year = request.form.get('admission_year')
        education_form = request.form.get('education_form')
        group = request.form.get('group')
        try:
            student = Student(name=name, lastname=lastname, surname=surname, admission_year=admission_year, education_form=education_form, group=group)
            db.session.add(student)
            db.session.commit()
            flash("Пользователь успешно добавлен", "success")
            return redirect(url_for("studentslist"))
        except:
            flash("Произошла ошибка", "danger")
            return render_template('createstudent.html', title='Добавление студента')

    return render_template('createstudent.html', title='Добавление студента')

@app.route('/editstudent/<int:id>', methods=['GET', 'POST'])
def editstudent(id):
    student = Student.query.get_or_404(id)
    if request.method == 'POST':
        student.name = request.form.get('name')
        student.lastname = request.form.get('lastname')
        student.surname = request.form.get('surname')
        student.admission_year = request.form.get('admission_year')
        student.education_form = request.form.get('education_form')
        student.group = request.form.get('group')
        try:
            db.session.commit()
            flash("Пользователь успешно отредактирован", "success")
            return redirect(url_for("studentslist"))
        except:
            flash("Произошла ошибка", "danger")
            return render_template('editstudent/<int:id>.html', title='Редактирование студента')

    return render_template('editstudent.html', title='Редактирование студента', student=student)

@app.route('/createeducationplan', methods=['GET', 'POST'])
def createeducationplan():
    if request.method == 'POST':
        speciality = request.form.get('speciality')
        discipline = request.form.get('discipline')
        semester = request.form.get('semester')
        hours = request.form.get('hours')
        exam_or_test = request.form.get('exam_or_test')
        try:
            plan = PlanOfStudy(speciality=speciality, discipline=discipline, semester=semester, hours=hours, exam_or_test=exam_or_test)
            db.session.add(plan)
            db.session.commit()
            flash("Учебный план успешно добавлен", "success")
            return redirect(url_for("educationplanslist"))
        except:
            flash("Произошла ошибка", "danger")
            return render_template('createeducationplan.html', title='Добавление учебного плана')
    
    return render_template('createeducationplan.html', title='Добавление учебного плана')

@app.route('/editeducationplan/<int:id>', methods=['GET', 'POST'])
def editeducationplan(id):
    if request.method == 'POST':
        speciality = request.form.get('speciality')
        discipline = request.form.get('discipline')
        semester = request.form.get('semester')
        hours = request.form.get('hours')
        exam_or_test = request.form.get('exam_or_test')
        try:
            plan = PlanOfStudy(speciality=speciality, discipline=discipline, semester=semester, hours=hours, exam_or_test=exam_or_test)
            db.session.add(plan)
            db.session.commit()
            flash("Учебный план успешно отредактирован", "success")
            return redirect(url_for("educationplanslist"))
        except:
            flash("Произошла ошибка", "danger")
            return render_template('editeducationplan/<int:id>.html', title='Редактирование учебного плана')
    
    educationplan = PlanOfStudy.query.get(id)
    return render_template('editeducationplan.html', title='Редактирование учебного плана', educationplan=educationplan)

