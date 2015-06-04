from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from config import SQLALCHEMY_DATABASE_URI


db = create_engine("%s" % SQLALCHEMY_DATABASE_URI)
sess = sessionmaker(db)
sess = sess.configure(db)


def run(stmt):
	rs = stmt.execute()
	for row in rs:
		print row

courses = sess.query(Course).all()