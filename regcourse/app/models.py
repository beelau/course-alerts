from . import db

class Course(db.Model):
	__tablename__ = 'courses'
	id = db.Column(db.Integer, primary_key=True)
	cname = db.Column(db.String(4))
	cid = db.Column(db.Integer)
	sec = db.Column(db.String(4))
	users = db.relationship('User', backref='course', lazy='dynamic')

	def __repr__(self):
		return 'Course %r' % self.cname

class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(64))
	course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
	reserved = db.Column(db.Boolean)


	def __repr__(self):
		return '<User %r>' % self.email