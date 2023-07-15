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
        self.app_id = id
        self.app_title = title
        self.app_date = date
        self.app_message = message
        self.faculty_id = faculty
        self.student_id = student


class AppointmentRequestsSchema(ma.Schema):
    class Meta:
        fields = ('app_id', 'app_title', 'app_date', 'app_message', 'faculty_id', 'student_id')


appointment_request_schema = AppointmentRequestsSchema()
appointment_requests_schema = AppointmentRequestsSchema(many=True)


class AccessRequest(db.Model):
    access_id = db.Column(db.Integer, primary_key=True)
    access_title = db.Column(db.String(50), nullable=False)
    access_date_start = db.Column(db.DateTime(timezone=True))
    access_date_end = db.Column(db.DateTime(timezone=True))
    access_message = db.Column(db.String(2000), nullable=False)
    facility_id = db.Column(db.Integer, nullable=False)
    student_id = db.Column(db.Integer, nullable=False)

    def __init__(self, access_id, access_title, access_date_start, access_date_end, access_message,
                 facility_id, student_id):
        self.access_id = access_id
        self.access_title = access_title
        self.access_date_start = access_date_start
        self.access_date_end = access_date_end
        self.access_message = access_message
        self.student_id = student_id
        self.facility_id = facility_id


class AccessRequestSchema(ma.Schema):
    class Meta:
        fields = ('access_id', 'access_title', 'access_date_start', 'access_date_end',
                  'access_message',
                  'facility_id', 'student_id')


access_request_schema = AccessRequestSchema()
access_requests_schema = AccessRequestSchema(many=True)


class FacilityRequest(db.Model):
    facility_request_id = db.Column(db.Integer, primary_key=True)
    facility_id = db.Column(db.Integer, nullable=False)
    facility_request_title = db.Column(db.String(100), nullable=False)
    facility_date_start = db.Column(db.DateTime(timezone=True))
    facility_date_end = db.Column(db.DateTime(timezone=True))
    facility_activity = db.Column(db.String(2000), nullable=False)
    facility_additional_eq = db.Column(db.String(1000), nullable=False)
    student_id = db.Column(db.Integer, nullable=False)

    def __init__(self, facility_request_id, facility_id, facility_request_title, facility_request_date_start,
                 facility_request_date_end, facility_request_activity,
                 facility_request_additional_eq, student_id):
        self.facility_request_id = facility_request_id
        self.facility_id = facility_id
        self.facility_request_title = facility_request_title
        self.facility_date_start = facility_request_date_start
        self.facility_date_end = facility_request_date_end
        self.facility_request_activity = facility_request_activity
        self.facility_request_additional_eq = facility_request_additional_eq
        self.student_id = student_id


class FacilityRequestSchema(ma.Schema):
    class Meta:
        fields = ('facility_request_id', 'facility_id', 'facility_request_title', 'facility_request_date_start',
                  'facility_request_date_end', 'facility_request_activity',
                  'facility_request_additional_eq', 'student')


facility_request_schema = FacilityRequestSchema()
facility_requests_schema = FacilityRequestSchema(many=True)


def status_update(content):
    print("1")


@app.route('/post_rfid_hall', methods=['POST'])
async def json_handler():
    print(request.is_json)
    content = request.get_json()
    print(content)
    return status_update(content)


@app.route('/post_appointment', methods=['POST'])
def add_appointment():
    app_id = None
    app_title = request.json["appointment_title"]
    app_date = request.json["appointment_date"]
    app_message = request.json["appointment_message"]
    student_id = request.json["student"]
    faculty_id = request.json["faculty"]

    dateformat = '%b %d %Y %I:%M%p'
    appointment_date = datetime.strptime(app_date, dateformat)

    new_appointment = AppointmentRequests(app_id, app_title, appointment_date, app_message, faculty_id, student_id)

    db.session.add(new_appointment)
    db.session.commit()

    return appointment_request_schema.jsonify(new_appointment)


@app.route('/post_facility', methods=['POST'])
def add_facility():
    facility_request_id = None
    facility_id = request.json["facility_id"]
    facility_request_title = request.json["facility_title"]
    facility_date_start = request.json["date_start"]
    facility_date_end = request.json["date_end"]
    facility_activity = request.json["activity"]
    facility_additional_eq = request.json["additional_eq"]
    student_id = request.json['student_id']

    dateformat = '%b %d %Y %I:%M%p'
    facility_date_start = datetime.strptime(facility_date_start, dateformat)
    facility_date_end = datetime.strptime(facility_date_end, dateformat)

    new_facility = FacilityRequest(facility_request_id, facility_id, facility_request_title, facility_date_start,
                                   facility_date_end,
                                   facility_activity, facility_additional_eq, student_id)

    db.session.add(new_facility)
    db.session.commit()

    return facility_request_schema.jsonify(new_facility)


@app.route('/post_access', methods=['POST'])
def add_access():
    access_id = None
    facility_id = request.json["facility_id"]
    access_title = request.json["access_title"]
    access_date_start = request.json["date_start"]
    access_date_end = request.json["date_end"]
    access_message = request.json["request"]
    student_id = request.json["student_id"]

    dateformat = '%b %d %Y %I:%M%p'
    access_date_start = datetime.strptime(access_date_start, dateformat)
    access_date_end = datetime.strptime(access_date_end, dateformat)

    new_access = AccessRequest(access_id, access_title, access_date_start, access_date_end, access_message, facility_id,
                               student_id)

    db.session.add(new_access)
    db.session.commit()

    return access_request_schema.jsonify(new_access)


if __name__ == '__main__':
    app.run(debug=True)
