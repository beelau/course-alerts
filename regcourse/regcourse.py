
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, Query
from config import SQLALCHEMY_DATABASE_URI
from sqlalchemy.orm import relationship, backref
import time
import dryscrape
import re

# initiate database connection
db = create_engine("%s" % SQLALCHEMY_DATABASE_URI)
base = declarative_base()
base.metadata.reflect(db)

# Classes for accesses
class Course(base):
	__table__ = base.metadata.tables['courses']

class User(base):
	__table__ = base.metadata.tables['users']

# Methods
def startSession():
	db_session = scoped_session(sessionmaker(bind=db))
	course_list = db_session.query(Course).all()
	user_list = db_session.query(User).all()
	regCourse(course_list, user_list)

def printDb(course_list, user_list):
	for c in course_list:
		id = c.id
		cname = c.cname
		cid = c.cid
		sec = c.sec
		print "%d - %s, %d, %s" % (id, cname, cid, sec)	

	for u in user_list:
		print "%d - %s, %d, %s" % (u.id, u.email, u.course_id, u.reserved)

def regCourse(course_list, user_list):

	print "start"	
	for c in course_list:
		id = c.id
		cname = c.cname
		cid = c.cid
		sec = c.sec

		sess = dryscrape.Session()
		sess.set_attribute('auto_load_images', False)
		sess.visit("https://courses.students.ubc.ca/cs/main?sessyr=2014&sesscd=W")
		sess.at_xpath('//*[@id="ubc7-unit-navigation"]/ul/li[1]/div/a').click()
		sess.at_xpath('//*[@id="ubc7-unit-navigation"]/ul/li[1]/div/ul/li[2]/a').click()
		sess.visit("https://courses.students.ubc.ca/cs/main?pname=subjarea&tname=subjareas&req=5&dept=%s&course=%d&section=%s" % (cname, cid, sec))
		pagehtml = sess.source()
		findSeats(pagehtml)
	print "end"	

def findSeats(pagehtml):
	seatsRE = '<td width="200px">Total Seats Remaining:</td><td align="left"><strong>(\d+)</strong></td>' + '.+' + \
				'<td width="200px">General Seats Remaining:</td><td align="left"><strong>(\d+)</strong>' + '.+' + \
				'<td width="200px">Restricted Seats Remaining\*:</td><td align="left"><strong>(\d+)</strong></td>'
	seats = re.search(seatsRE, pagehtml)
	if seats is not None:
		totalseats = int(seats.group(1))
		generalseats = int(seats.group(2))
		reservedseats = int(seats.group(3))

	print "%d" % totalseats
	room = 0
	reserved = False
	if totalseats > 0:
		if generalseats > 0:
			room = generalseats
		elif reservedseats > 0:
			room = reservedseats
			reserved = True

	
def main():
	start_time = time.time()
	startSession()
	print("--- %s seconds ---" % (time.time() - start_time))

main()