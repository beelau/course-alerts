from flask.ext.wtf import Form
from wtforms import IntegerField, BooleanField, StringField, validators, SubmitField
from wtforms.validators import Required, Length, Email

class CourseForm(Form):
	cname = StringField('Course Name', [validators.Length(min=4, max=4), validators.Required()])
	cid = IntegerField('Course ID', [validators.Required()])
	sec = StringField('Course Section', [validators.Length(min=3, max=3), validators.Required()])
	email = StringField('Email', [validators.Email(), validators.Required()])
	reserved = BooleanField('Reserved',)
	submit = SubmitField('submit')