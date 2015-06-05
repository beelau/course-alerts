from flask import render_template, session, redirect, url_for, flash
from . import db
from .models import Course, User
from forms import CourseForm
from app import app
import time
import dryscrape
from sqlalchemy.inspection import inspect
import re

@app.route('/', methods=['GET', 'POST'])
def home():
	form = CourseForm()

	if form.validate_on_submit():
		course_name = form.cname.data.upper()
		course_id = form.cid.data
		course_sec = form.sec.data.upper()
		email = form.email.data.lower()
		reserved = form.reserved.data

		result = checkCourse(course_name, course_id, course_sec)
		if result is not None:
			flash('*** ERROR - Course does not exist ***')
		else:
			course = Course.query.filter_by(cname=course_name, cid=course_id, sec=course_sec).first()
			if course is None:
				course = Course(cname=course_name, cid=course_id, sec=course_sec)
				db.session.add(course)
				db.session.flush()
				user = User(email=email, course_id=course.id, reserved=reserved)
				db.session.add(user)
				session['known'] = False
				flash('Thank you for adding your course')
				return redirect(url_for('home'))
			else:
				flash('Thank you for adding your course')
				session['known'] = True
				user = User(email=email, course_id=course.id, reserved=reserved)
				db.session.add(user)
			db.session.commit()
	return render_template('home.html', form=form, known=session.get('known'))

def checkCourse(course_name, course_id, course_sec):
	sess = dryscrape.Session()
	sess.set_attribute('auto_load_images', False)
	sess.visit("https://courses.students.ubc.ca/cs/main?sessyr=2014&sesscd=W")
	sess.at_xpath('//*[@id="ubc7-unit-navigation"]/ul/li[1]/div/a').click()
	sess.at_xpath('//*[@id="ubc7-unit-navigation"]/ul/li[1]/div/ul/li[2]/a').click()
	sess.visit("https://courses.students.ubc.ca/cs/main?pname=subjarea&tname=subjareas&req=5&dept=%s&course=%d&section=%s" % (course_name, course_id, course_sec))
	pagehtml = sess.source()
	regex = 'The requested section is either no longer offered at UBC Vancouver or is not being offered this session.'
	result = re.search(regex, pagehtml)
	return result