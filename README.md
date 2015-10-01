# Overview
Course-alerts is a Flask web-app for UBC Students to help keep tabs on the space available in classes that are full. This app only works for classes that have no waitlist. I created this application to automate the process of periodically checking for space. I have provided my code and installation instructions for students interested in learning how to build one themselves.

#####Flask web-app
The user interface for students to enter their course information and email. 

#####regcourse.py
This is the script that is responsible for querying the database in the background, and scraping each course page for the space availability and sending an email if there is available space. I decided to use regex instead of Xpath or CSSselect for scraping because it worked easier and the site layout from term to term remained consistent. 

####config.py
Contains configuration information for some flask extensions and email info.

#Usage
Installation instructions for Ubuntu:
```
 # Install virtualenv: https://virtualenv.pypa.io/en/latest/index.html
 # Install the dependencies in your virtual environment: pip install -r requirements.txt
 # Install dryscrape: https://dryscrape.readthedocs.org/en/latest/
```
