# course-alerts

Course-alerts is a Flask web-app for UBC Students to help keep tabs on the space available in classes that are full. This app only works for classes that have no waitlist. I created this application to provide a free service for students and to learn Python, web-app development, and web-scraping.

Flask web-app
The user interface for students to enter their course information and email. There are checks in place to validate the course. Upon submission it will insert into a database. 

regcourse.py
This is the script that is responsible for querying the database in the background, and scraping each course page for the space availability and sending an email if there is available space.
