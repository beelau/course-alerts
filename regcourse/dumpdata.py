from regcourse import *

db_session = scoped_session(sessionmaker(bind=db))
course_list = db_session.query(Course).all()
user_list = db_session.query(User).all()

if __name__ == "__main__":
	dumpData(course_list, user_list)