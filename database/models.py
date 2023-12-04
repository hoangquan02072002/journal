import os
import sqlalchemy as sa
from app import db

class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    lastname = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    admission_year = db.Column(db.Integer, nullable=False)
    education_form = db.Column(db.String(100), nullable=False)
    group = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<Student %r>' % self.lastname
    
    # __table_args__ = {'extend_existing': True}
    
class PlanOfStudy(db.Model):
    __tablename__ = 'planofstudy'

    id = db.Column(db.Integer, primary_key=True)
    speciality = db.Column(db.String(100), nullable=False)
    discipline = db.Column(db.String(100), nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    hours = db.Column(db.Integer, nullable=False)
    exam_or_test = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return self.discipline

class Gradebook(db.Model):
    __tablename__ = 'gradebook'

    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    discipline_id = db.Column(db.Integer, db.ForeignKey("planofstudy.id"), nullable=False)
    mark = db.Column(db.Integer, nullable=False)

    student = db.relationship('Student')
    planofstudy = db.relationship('PlanOfStudy')

# def fill_db():
#     users = [
#         Student(lastname='Иванов', name='Иван', surname='Иванович', admission_year=2018, group=101, education_form='дневная'),
#         Student(lastname='Петрова', name='Анна', surname='Сергеевна', admission_year=2020, group=203, education_form='вечерняя'),
#         Student(lastname='Смирнов', name='Дмитрий', surname='Александрович', admission_year=2019, group=305, education_form='заочная'),
#         Student(lastname='Козлова', name='Екатерина', surname='Владимировна', admission_year=2017, group=102, education_form='дневная'),
#         Student(lastname='Морозов', name='Павел', surname='Андреевич', admission_year=2021, group=204, education_form='вечерняя'),
#         Student(lastname='Иванова', name='Ивана', surname='Ивановича', admission_year=2018, group=102, education_form='дневная'),
#         Student(lastname='Петрова', name='Анна', surname='Сергеевна', admission_year=2020, group=203, education_form='вечерняя'),
#         Student(lastname='Смирнов', name='Дмитрий', surname='Александрович', admission_year=2019, group=305, education_form='заочная'),
#         Student(lastname='Козлова', name='Екатерина', surname='Владимировна', admission_year=2017, group=102, education_form='дневная'),
#         Student(lastname='Морозов', name='Павел', surname='Андреевич', admission_year=2021, group=204, education_form='вечерняя'),
#         Student(lastname='Иванов', name='Иван', surname='Иванович', admission_year=2018, group=101, education_form='дневная'),
#         Student(lastname='Петрова', name='Анна', surname='Сергеевна', admission_year=2020, group=203, education_form='вечерняя'),
#         Student(lastname='Смирнов', name='Дмитрий', surname='Александрович', admission_year=2019, group=305, education_form='заочная'),
#         Student(lastname='Козлова', name='Екатерина', surname='Владимировна', admission_year=2017, group=102, education_form='дневная'),
#         Student(lastname='Морозов', name='Павел', surname='Андреевич', admission_year=2021, group=204, education_form='вечерняя'),
#         Student(lastname='Иванов', name='Иван', surname='Иванович', admission_year=2018, group=101, education_form='дневная'),
#         Student(lastname='Петрова', name='Анна', surname='Сергеевна', admission_year=2020, group=203, education_form='вечерняя'),
#         Student(lastname='Смирнов', name='Дмитрий', surname='Александрович', admission_year=2019, group=305, education_form='заочная'),
#         Student(lastname='Козлова', name='Екатерина', surname='Владимировна', admission_year=2017, group=102, education_form='дневная'),
#         Student(lastname='Морозов', name='Павел', surname='Андреевич', admission_year=2021, group=204, education_form='вечерняя'),
#     ]

#     # Добавьте объекты в сессию и сохраните их в базе данных
#     for user in users:
#         db.session.add(user)
#     db.session.commit()

# def fill_db2():
#     data = [
#         PlanOfStudy(speciality="Информатика", discipline="Программирование", semester=3, hours=60, exam_or_test="Экзамен"),
#         PlanOfStudy(speciality="Математика", discipline="Математический анализ", semester=2, hours=45, exam_or_test="Зачет"),
#         PlanOfStudy(speciality="Физика", discipline="Общая физика", semester=1, hours=75, exam_or_test="Экзамен"),
#         PlanOfStudy(speciality="Искусствоведение", discipline="История искусства", semester=4, hours=90, exam_or_test="Экзамен"),
#         PlanOfStudy(speciality="Экономика", discipline="Экономическая теория", semester=5, hours=120, exam_or_test="Экзамен"),
#         PlanOfStudy(speciality="Лингвистика", discipline="Английский язык", semester=1,hours= 60, exam_or_test="Зачет"),
#         PlanOfStudy(speciality="Прикладная математика", discipline="Теория вероятностей и математическая статистика", semester=3, hours=75, exam_or_test="Экзамен"),
#         PlanOfStudy(speciality="Гуманитарные науки", discipline="Философия", semester=2, hours=45, exam_or_test="Зачет"),
#         PlanOfStudy(speciality="Менеджмент", discipline="Маркетинг", semester=4, hours=90, exam_or_test="Экзамен"),
#         PlanOfStudy(speciality="Юриспруденция", discipline="Основы права", semester=1, hours=60, exam_or_test="Зачет"),
#         PlanOfStudy(speciality="История", discipline="История России", semester=3, hours=70, exam_or_test="Экзамен"),
#         PlanOfStudy(speciality="Биология", discipline="Генетика", semester=4, hours=80, exam_or_test="Экзамен"),
#         PlanOfStudy(speciality="Психология", discipline="Общая психология", semester=2, hours=50, exam_or_test="Зачет"),
#         PlanOfStudy(speciality="Химия", discipline="Неорганическая химия", semester=5, hours=100, exam_or_test="Экзамен"),
#         PlanOfStudy(speciality="Социология", discipline="Социологические исследования", semester=4, hours=90, exam_or_test="Экзамен"),
#     ]
    
#     for i in data:
#         db.session.add(i)
#     db.session.commit()