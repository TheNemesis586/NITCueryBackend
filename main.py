import os
from datetime import datetime
from flask_marshmallow import Marshmallow
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'main_db.sqlite')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


class StudentID(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    card_serial = db.Column(db.Integer, nullable=False)
    roll_no = db.Column(db.String(10), nullable=False)

    @property
    def __repr__(self):
        return f'<StudentID {self.roll_no}>'


class ProfessorID(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    card_serial = db.Column(db.Integer, nullable=False)
    department = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    location = db.Column(db.String(30), nullable=False)
    mobile_number = db.Column(db.String(10), nullable=False)
    available = db.Column(db.Boolean, nullable=False)


class Facilities(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    facility_name = db.Column(db.String(25), nullable=False)
    location = db.Column(db.String(20), nullable=False)
    seating_capacity = db.Column(db.Integer, primary_key=True)
    availability = db.Column(db.Boolean, nullable=False)
    access_rights = db.Column(db.String(25), nullable=False)


class AppointmentRequests(db.Model):
    app_id = db.Column(db.Integer, primary_key=True)
    app_title = db.Column(db.String(50), nullable=False)
    app_date = db.Column(db.DateTime(timezone=True))
    app_message = db.Column(db.String(2000), nullable=False)
    faculty_id = db.Column(db.Integer, nullable=False)
    student_id = db.Column(db.Integer, nullable=False)

    def __init__(self, id, title, date, message, faculty, student):
        self.id = id
        self.title = title
        self.date = date
        self.message = message
        self.faculty = faculty
        self.student = student


class AppointmentRequestsSchema(ma.Schema):
    class Meta:
        fields = ('app_id', 'app_title', 'app_date', 'app_message', 'faculty_id', 'student_id')


appointment_request_schema = AppointmentRequestsSchema()
appointment_requests_schema = AppointmentRequestsSchema(many=True)


class AccessRequests(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    date_start = db.Column(db.DateTime(timezone=True))
    date_end = db.Column(db.DateTime(timezone=True))
    message = db.Column(db.String(2000), nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    facility = db.Column(db.Integer, primary_key=True)
    student = db.Column(db.Integer, nullable=False)


class FacilityBooking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    date_start = db.Column(db.DateTime(timezone=True))
    date_end = db.Column(db.DateTime(timezone=True))
    activity = db.Column(db.String(2000), nullable=False)
    additional_eq = db.Column(db.String(1000), nullable=False)
    availability = db.Column(db.Boolean, nullable=False)


def status_update(content):
    print("1")


@app.route('/postjson', methods=['POST'])
async def json_handler():
    print(request.is_json)
    content = request.get_json()
    print(content)
    return status_update(content)


@app.route('/post_appointment', methods=['POST'])
def add_appointment():
    app_id = 1
    app_title = request.json['appointment_title']
    app_date = request.json['appointment_date']
    app_message = request.json['appointment_message']
    student_id = request.json['student']
    faculty_id = request.json['faculty']

    dateformat = '%b %d %Y %I:%M%p'
    appointment_date = datetime.strptime(app_date, dateformat)

    new_appointment = AppointmentRequests(app_id, app_title, appointment_date, app_message, faculty_id, student_id)

    db.session.add(new_appointment)
    db.session.commit()

    return appointment_request_schema.jsonify(new_appointment)


if __name__ == '__main__':
    app.run(debug=True)
