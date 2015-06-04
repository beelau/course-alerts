from flask import render_template, session, redirect, url_for, flash
from . import db
from .models import Course, User
from forms import CourseForm
from app import app
import time
import dryscrape

@app.route('/', methods=['GET', 'POST'])
def home():
	form = CourseForm()
	if form.validate_on_submit():
		course = Course.query.filter_by(cname=form.cname.data, cid=form.cid.data, sec=form.sec.data).first()
		if course is None:
			course = Course(cname=form.cname.data, cid=form.cid.data, sec=form.sec.data)
			user = User(email=form.email.data)
			db.session.add(course)
			db.session.add(user)
			session['known'] = False
			flash('Thank you for adding your course')
			return redirect(url_for('home'))
		else:
			flash('Thank you for adding your course')
			session['known'] = True
			user = User(email=form.email.data, course_id=course.id)
			db.session.add(user)
	return render_template('home.html', form=form, known=session.get('known'))

