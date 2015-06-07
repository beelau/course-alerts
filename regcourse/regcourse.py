
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, Query
from config import SQLALCHEMY_DATABASE_URI
from sqlalchemy.orm import relationship, backref
import time
from time import strftime
from email.mime.text import MIMEText
import smtplib
import dryscrape
import re
from config import USER_EMAIL, PASSWORD

db = create_engine("%s" % SQLALCHEMY_DATABASE_URI)
base = declarative_base()
base.metadata.reflect(db)
db_session = scoped_session(sessionmaker(bind=db))

# Classes for accesses
class Course(base):
	__table__ = base.metadata.tables['courses']

class User(base):
	__table__ = base.metadata.tables['users']

# Methods
def startSession():
	conn = db.connect()
	session = db_session(bind=conn)
	avail_courses = regCourse(session)
	if avail_courses != None:
		sendMail(avail_courses, session)
	session.close()

def dumpData(course_list, user_list):
	for c in course_list:
		id = c.id
		cname = c.cname
		cid = c.cid
		sec = c.sec
		print "%d - %s, %d, %s" % (id, cname, cid, sec)	

	for u in user_list:
		print "%d - %s, %d, %s" % (u.id, u.email, u.course_id, u.reserved)

def regCourse(session):
	course_list = session.query(Course).all()

	print "start"	
	avail_courses = []
	for c in course_list:
		pkey = c.id
		cname = c.cname
		cid = c.cid
		sec = c.sec
		print "%d - %s, %d, %s" % (pkey, cname, cid, sec)	
		sess = dryscrape.Session()
		sess.set_attribute('auto_load_images', False)
		sess.visit("https://courses.students.ubc.ca/cs/main?sessyr=2015&sesscd=W")
		sess.at_xpath('//*[@id="ubc7-unit-navigation"]/ul/li[1]/div/a').click()
		sess.at_xpath('//*[@id="ubc7-unit-navigation"]/ul/li[1]/div/ul/li[2]/a').click()
		sess.visit("https://courses.students.ubc.ca/cs/main?pname=subjarea&tname=subjareas&req=5&dept=%s&course=%d&section=%s" % (cname, cid, sec))
		pagehtml = sess.source()
		(room, reserved) = findSeats(pagehtml)

		if room > 0:
			course_name = "%s %d %s" % (cname, cid, sec)
			avail_courses.append([pkey, course_name, room, reserved])
	
	return avail_courses

def findSeats(pagehtml):
	totalre = "<td width=200px>Total Seats Remaining:</td><td align=left><strong>(\d+)</strong></td>"
	generalre = "<td width=200px>General Seats Remaining:</td><td align=left><strong>(\d+)</strong>"
	reservedre = "<td width=200px>Restricted Seats Remaining\*:</td><td align=left><strong>(\d+)</strong></td>"

	tseats = re.search(totalre, pagehtml)
	gseats = re.search(generalre, pagehtml)
	rseats = re.search(reservedre, pagehtml)

	if tseats != None:
		tseats = int(tseats.group(1))
	if gseats != None:
		gseats = int(gseats.group(1))
	if rseats != None:
		rseats = int(rseats.group(1))

	room = 0
	reserved = False
	if tseats > 0:
		if gseats > 0:
			room = gseats
		elif rseats > 0:
			room = rseats
			reserved = True

	return (room, reserved)

def sendMail(avail_courses, session):
	server = smtplib.SMTP("smtp.gmail.com", 587)
	server.ehlo()
	server.starttls()
	server.login(USER_EMAIL, PASSWORD)
	addr_from = USER_EMAIL

	for course in avail_courses:
		pkey = course[0]
		course_name = course[1]
		seats = course[2]
		reserved = course[3]
		print "%d, %s, %d, %s" % (pkey, course_name, seats, reserved)

		user_list = []
		if reserved == True:
			user_list = session.query(User).filter_by(course_id = pkey, reserved=reserved)
		else:
			user_list = session.query(User).filter_by(course_id = pkey)

		for user in user_list:
			pid = user.id
			email = user.email

			addr_to = email

			when = strftime("%m/%d/%Y %H:%M")
			msg = MIMEText("Hi there! \n\n%d seats are available in %s (as of %s)\n" % (seats, course_name, when))
			msg['To'] = addr_to
			msg['From'] = addr_from
			msg['Subject'] = "A seat is available in your class!"

			server.sendmail(addr_from, addr_to, msg.as_string())
			session.delete(user)

	session.commit()
	server.quit()

def main():
	start_time = time.time()
	startSession()
	print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == "__main__":
	main()