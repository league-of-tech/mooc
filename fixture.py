#-*- coding: utf-8 -*-
from datetime import datetime

from mooc.extensions import db
from mooc.models.master import Tag
from mooc.models.account import User, SzuAccount, College, Teacher, Role
from mooc.models.course import Subject, Category, Course, Lecture, LearnRecord
from mooc.models.course import Quiz, QuizOption
from mooc.models.resource import Resource
from mooc.models.discuss import Question, Answer, QuestionTag


def _init_role():
    global roles
    roles = (
        Role('anonymous'), Role('local_user'), Role('student'),
        Role('teacher'), Role('super_admin')
    )
    roles[2].parents.append(roles[1])
    roles[3].parents.append(roles[1])
    roles[4].parents.append(roles[1])
    for role in roles:
        db.session.add(role)


def _init_college():
    global csse
    csse = College(name=u'计算机与软件学院', order=13)
    db.session.add(csse)


def _init_user():
    global shonenada, key
    shonenada = User(
        username='shonenada',
        passwd='000000',
        nickname='shonenada',
        is_male=True,
    )
    key = User(
        username='key',
        passwd='123456',
        nickname='key',
        is_male=True
    )
    shonenada.active()
    key.active()
    shonenada.roles.append(roles[4])
    key.roles.append(roles[3])
    db.session.add(shonenada)
    db.session.add(key)


def _init_szu_account():
    global shonenada_account, key_account
    shonenada_account = SzuAccount(
        user=shonenada,
        card_id='112020',
        stu_number='2011150000',
        college=csse,
        szu_account_type='undergrade'
    )
    key_account = SzuAccount(
        user=key,
        card_id='113030',
        stu_number='2011150999',
        college=csse,
        szu_account_type='teacher'
    )
    db.session.add(shonenada_account)
    db.session.add(key_account)


def _init_teacher():
    global mr_key
    mr_key = Teacher(
        title='teacher',
        description='KEY',
        szu_account=key_account
    )
    db.session.add(mr_key)


def _init_tags():
    global tags
    tags = (
    )
    for t in tags:
        db.session.add(t)


def _init_subject():
    global subjects
    subjects = (
        Subject(name=u'电类', description=u'电类'),
    )
    for subject in subjects:
        db.session.add(subject)


def _init_category():
    global categorys
    categorys = (
        Category(
            name=u'数字电子技术',
            subject=subjects[0]
        ),
    )
    for category in categorys:
        db.session.add(category)


def _init_course():
    global courses
    courses = (
        Course(
            name=u'数字逻辑与数字系统.多位加法器：串行加法器',
            description=u'课程介绍数字逻辑与数字系统',
            teacher=mr_key,
            category=categorys[0]
        ),
    )
    for course in courses:
        course.college = csse
        db.session.add(course)


def _init_lecture():
    global lectures
    lectures = (
        Lecture(
            name=u'多位加法器：串行加法器',
            description=u'本课程为您讲解多位加法器：串行加法器',
            teacher=mr_key,
            course=courses[0],
            order=1,
            knowledge_point=u'<ul><li>知识点1</li><li>知识点2</li><li>...</li></ul>',
            record_time=datetime(2013, 11, 06),
            record_location=u'教学楼A101',
            video_url='http://mooc.shonenada.com/static/upload/videos/2013-11-06.caiye.mp4',
            video_length=16
        ),
    )
    for lecture in lectures:
        db.session.add(lecture)


def _init_resource():
    global resources
    resources = (
        Resource(
            name=u'示范资源',
            lecture=lectures[0],
            resource_url='/static/upload/resources/pytest.pdf',
            type='pdf',
        ),
    )
    for r in resources:
        db.session.add(r)


def _init_learn_record():
    for lecture in lectures:
        learn_record = LearnRecord()
        learn_record.lecture = lecture
        learn_record.user = shonenada
        db.session.add(learn_record)


def _init_quiz_option():
    global options
    options = (
        QuizOption(content=u'各位同时相加', is_answer=True),
        QuizOption(content=u'不同位顺序相加', is_answer=False),
        QuizOption(content=u'存在着进位信号的传递', is_answer=True),
        QuizOption(content=u'进行相加的数的大小', is_answer=False),
        QuizOption(content=u'正确答案', is_answer=True),
        QuizOption(content=u'错误答案', is_answer=False),
    )
    for option in options:
        db.session.add(option)


def _init_quiz():
    global quizs
    quizs = (
        Quiz(
            question=u'串行加法器的特点',
            time_at=350,
            lecture=lectures[0],
        ),
        Quiz(
            question=u'影响速度的主要因素',
            time_at=400,
            lecture=lectures[0],
        ),
        Quiz(
            question=u'请选择正确答案',
            time_at=3,
            lecture=lectures[0],
        ),
    )
    quizs[0].options.append(options[0])
    quizs[0].options.append(options[1])

    quizs[1].options.append(options[2])
    quizs[1].options.append(options[3])

    quizs[2].options.append(options[4])
    quizs[2].options.append(options[5])

    for quiz in quizs:
        db.session.add(quiz)


def _init_question_tag():
    global question_tags
    question_tags = (
        QuestionTag(tag=u'问题标签1'),
        QuestionTag(tag=u'问题标签2'),
        QuestionTag(tag=u'问题标签3'),
        QuestionTag(tag=u'问题标签4')
    )
    for qt in question_tags:
        db.session.add(qt)


def _init_question():
    global questions
    questions = (
        Question(
            title=u'没有对应课程的问题',
            content=u'问题内容',
            lecture=None,
            author=shonenada),
        Question(
            title=u'问题',
            content=u'问题内容~',
            lecture=lectures[0],
            author=shonenada,
            anonymous=True
        ),
    )
    questions[1].tags.append(question_tags[1])
    questions[0].tags.append(question_tags[1])
    questions[1].tags.append(question_tags[0])
    questions[0].tags.append(question_tags[3])

    for question in questions:
        db.session.add(question)


def _init_answer():
    global answers
    answers = (
    )
    for answer in answers:
        db.session.add(answer)


def init_db():
    _init_role()
    _init_college()
    _init_user()
    _init_szu_account()
    _init_teacher()
    _init_tags()
    _init_subject()
    _init_category()
    _init_course()
    _init_lecture()
    _init_resource()
    _init_learn_record()
    _init_quiz_option()
    _init_quiz()
    _init_question_tag()
    _init_question()
    _init_answer()
    db.session.commit()
