# Clarkson Course Feedback & Suggestion System

A Flask-based web application for the Clarkson University community to:

- Collect structured feedback from students on courses they’ve taken
- Allow alumni to suggest new courses based on real-world trends
- Provide faculty and administrators with analytics dashboards for data-driven course and curriculum improvement

> **Roles supported:** Students, Alumni, Faculty, and Administrators.

# Setup & Installation

## Clone the Repository

flask
flask_sqlalchemy
flask_wtf
wtforms
python-dotenv

## 1. Project Overview

The system is a web-based application designed for the Clarkson University community to provide insightful feedback on academic courses. The platform aims to improve the learning experience by:

- Collecting student feedback
- Offering analytical dashboards for instructors and administrators
- Enabling students and alumni to suggest new courses for future semesters

Key principles:

- Only students enrolled in a course can provide feedback.
- Students can view and edit their submissions within a limited time frame (and, ideally, even after graduation).
- Faculty and administrators can monitor feedback trends, view summarized analytics, and make data-driven decisions regarding course improvement and curriculum development.
- Feedback is only posted after review and approval by an administrator (e.g., validating attendance or enrollment).
- Alumni can suggest new courses based on trends they see in the field, helping Clarkson remain an always-evolving university.

## 2. Objectives

- Develop a centralized system for course feedback collection.
- Provide a mechanism for alumni to suggest new courses.
- Allow students to provide, edit, and review their feedback.
- Enable faculty and administrators to analyze feedback trends through an intuitive dashboard.
- Improve communication and feedback loops between students (current and alumni), instructors, and departments.
- Allow students to see course feedback to help them decide whether to enroll, beyond just the catalog description.

## 3. Key Features

> **Condition:** This is an app used by the Clarkson community.

### 3.1 Student Features

- View available and enrolled courses.
- Search and filter courses by name, department, or semester.
- Submit feedback only for courses taken in the current or past semesters.
- Edit feedback until a set deadline (`editable_until`).
- View previously given feedback.
- Suggest new courses and provide descriptions.

### 3.2 Alumni Features

- Select a department and suggest a new course.
- Add a description and justification for the new course suggestion.

### 3.3 Faculty / Admin Features

- Add and manage course details.
- Mark which courses are being offered in the current semester.
- Access a dashboard displaying feedback analytics (rating distributions, counts, trends).
- Review and approve/reject new course suggestions.
- Review and approve/reject feedback before publication.
- Delete clearly inappropriate or invalid feedback.

## 4. Tech Stack

- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, Jinja2 templates (optionally Bootstrap or Tailwind CSS)
- **Database:** SQLite (default) via SQLAlchemy (can be swapped for PostgreSQL/MySQL)
- **Auth/Sessions:** Flask session (optionally Flask-Login or similar)
- **Environment:** Python 3.x

## 5. Project Structure

Your actual structure may differ slightly, but a typical layout:
.
├── app.py # Flask entry point
├── config.py # Configuration (DB URI, secret key, etc.)
├── models.py # Models
├── forms.py # WTForms / Flask-WTF forms (if used)
├── requirements.txt # Python dependencies
├── README.md # This file
├── /templates # HTML templates (Jinja2)
│ ├── base.html
│ ├── index.html
│ ├── login.html
│ ├── courses.html
│ ├── feedback_form.html
│ ├── suggestions.html
│ ├── admin_dashboard.html
│ └── ...
└── /static # CSS, JS, images
├── css/
├── js/
└── img/

## 6. Database Design

# 6.1 Core Tables
