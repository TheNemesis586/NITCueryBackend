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


class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    card_serial = db.Column(db.Integer, nullable=False)
    roll_no = db.Column(db.String(10), nullable=False)

    def __init__(self, id, card_serial, roll_no):
        self.id = id
        self.card_serial = card_serial
        self.roll_no = roll_no


class StudentIDRequestsSchema(ma.Schema):
    class Meta:
        fields = ('id', 'card_serial', 'roll_no')


students_schema = StudentIDRequestsSchema()
students_multiple_schema = StudentIDRequestsSchema(many=True)


class ProfessorID(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    card_serial = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    staff_no = db.Column(db.String(10), nullable=False)
    department = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    mobile_number = db.Column(db.Integer, nullable=False)
    available = db.Column(db.Integer, nullable=False)

    def __init__(self, id, card_serial, staff_no, name, department, email, location, mobile_number, available):
        self.id = id
        self.card_serial = card_serial
        self.name = name
        self.staff_no = staff_no
        self.department = department
        self.email = email
        self.location = location
        self.mobile_number = mobile_number
        self.available = available


class ProfessorIDRequestsSchema(ma.Schema):
    class Meta:
        fields = (
            'id', 'card_serial', 'staff_no', 'name', 'department', 'email', 'location', 'mobile_number', 'available')


professorid_request_schema = ProfessorIDRequestsSchema()
professorid_requests_schema = ProfessorIDRequestsSchema(many=True)


class Facilities(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    facility_name = db.Column(db.String(25), nullable=False)
    location = db.Column(db.String(20), nullable=False)
    seating_capacity = db.Column(db.Integer, nullable=True)
    availability = db.Column(db.Boolean, nullable=False)
    access_rights = db.Column(db.String(25), nullable=False)
    faculty_in_charge = db.Column(db.String(25), nullable=False)

    def __init__(self, id, facility_name, location, seating_capacity, availability, access_rights, faculty_in_charge):
        self.id = id
        self.facility_name = facility_name
        self.location = location
        self.seating_capacity = seating_capacity
        self.availability = availability
        self.access_rights = access_rights
        self.faculty_in_charge = faculty_in_charge


class FacilitiesSchema(ma.Schema):
    class Meta:
        fields = (
            'id', 'facility_name', 'location', 'seating_capacity', 'availability', 'access_rights', 'faculty_in_charge')


facilities_schema = FacilitiesSchema()
facilities_multiple_schema = FacilitiesSchema(many=True)


class AppointmentRequests(db.Model):
    app_id = db.Column(db.Integer, primary_key=True)
    app_title = db.Column(db.String(50), nullable=False)
    app_date = db.Column(db.DateTime(timezone=True))
    app_message = db.Column(db.String(2000), nullable=False)
    faculty_id = db.Column(db.Integer, nullable=False)
    student_id = db.Column(db.Integer, nullable=False)
    app_response = db.Column(db.String(2000), nullable=False)
    approved = db.Column(db.Integer, nullable=False)

    def __init__(self, id, title, date, message, faculty, student, app_response, approved):
        self.app_id = id
        self.app_title = title
        self.app_date = date
        self.app_message = message
        self.faculty_id = faculty
        self.student_id = student
        self.app_response = app_response
        self.approved = approved


class AppointmentRequestsSchema(ma.Schema):
    class Meta:
        fields = (
            'app_id', 'app_title', 'app_date', 'app_message', 'faculty_id', 'student_id', 'app_response', 'approved')


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
    approved = db.Column(db.Integer, nullable=False)

    def __init__(self, access_id, access_title, access_date_start, access_date_end, access_message,
                 facility_id, student_id, approved):
        self.access_id = access_id
        self.access_title = access_title
        self.access_date_start = access_date_start
        self.access_date_end = access_date_end
        self.access_message = access_message
        self.student_id = student_id
        self.facility_id = facility_id
        self.approved = approved


class AccessRequestSchema(ma.Schema):
    class Meta:
        fields = ('access_id', 'access_title', 'access_date_start', 'access_date_end',
                  'access_message',
                  'facility_id', 'student_id', 'approved')


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
    approved = db.Column(db.Integer, nullable=False)

    def __init__(self, facility_request_id, facility_id, facility_request_title, facility_request_date_start,
                 facility_request_date_end, facility_request_activity,
                 facility_request_additional_eq, student_id, approved):
        self.facility_request_id = facility_request_id
        self.facility_id = facility_id
        self.facility_request_title = facility_request_title
        self.facility_date_start = facility_request_date_start
        self.facility_date_end = facility_request_date_end
        self.facility_activity = facility_request_activity
        self.facility_additional_eq = facility_request_additional_eq
        self.student_id = student_id
        self.approved = approved


class FacilityRequestSchema(ma.Schema):
    class Meta:
        fields = ('facility_request_id', 'facility_id', 'facility_request_title', 'facility_date_start',
                  'facility_date_end', 'facility_activity',
                  'facility_additional_eq', 'student_id', 'approved')


facility_request_schema = FacilityRequestSchema()
facility_requests_schema = FacilityRequestSchema(many=True)


@app.route('/post_search_specific', methods=['POST'])
def search_specific():
    database_select = request.json['table']

    if database_select == 'faculty':
        search_result = db.session.execute(db.select(ProfessorID)).scalars()
        print(search_result)
        return professorid_requests_schema.jsonify(search_result)
    elif database_select == 'facilities':
        search_result = db.session.execute(db.select(Facilities)).scalars()
        print(search_result)
        return facility_requests_schema.jsonify(search_result)
    else:
        search_result = db.session.execute(db.select(Facilities)).scalars()
        print(search_result)
        return access_requests_schema.jsonify(search_result)


@app.route('/post_rfid_prof', methods=['POST'])
def toggle_availability():
    card_serial = request.json['card_serial']

    update_availability = db.session.execute(
        db.select(ProfessorID).where(ProfessorID.card_serial == card_serial)).scalar_one()
    if update_availability.available == 1:
        update_availability.available = 0
    else:
        update_availability.available = 1
    db.session.add(update_availability)
    db.session.commit()
    return professorid_request_schema.jsonify(update_availability)


@app.route('/post_prof_details', methods=['POST'])
def fetch_prof_details():
    staff_no = request.json['staff_no']

    result = db.session.execute(db.select(ProfessorID).where(ProfessorID.staff_no == staff_no)).scalar_one()
    return professorid_request_schema.jsonify(result)


@app.route('/post_facility_details', methods=['POST'])
def fetch_facility_details():
    facility_name = request.json['facility_name']
    result = db.session.execute(db.select(Facilities).where(Facilities.facility_name == facility_name)).scalar_one()
    return facilities_schema.jsonify(result)


@app.route('/post_appointment', methods=['POST'])
def add_appointment():
    app_id = None
    app_title = request.json["appointment_title"]
    app_date = request.json["appointment_date"]
    app_message = request.json["appointment_message"]
    student_id = request.json["student"]
    faculty_id = request.json["faculty"]
    app_response = ''
    approved = 0

    dateformat = '%I:%M %p, %d-%m-%Y'
    appointment_date = datetime.strptime(app_date, dateformat)

    new_appointment = AppointmentRequests(app_id, app_title, appointment_date, app_message, faculty_id, student_id,
                                          app_response,
                                          approved)

    db.session.add(new_appointment)
    db.session.commit()

    return appointment_request_schema.jsonify(new_appointment)


@app.route('/post_appointment_approval', methods=['POST'])
def appointment_approval():
    app_id = request.json['app_id']

    appointment_id = db.session.execute(
        db.select(AppointmentRequests).where(AppointmentRequests.app_id == app_id)).scalar_one()
    return appointment_request_schema.jsonify(appointment_id)


@app.route('/post_access_approval', methods=['POST'])
def access_approval():
    access_id = request.json['access_id']

    access_request_id = db.session.execute(
        db.select(AccessRequest).where(AccessRequest.access_id == access_id)).scalar_one()
    return access_request_schema.jsonify(access_request_id)


@app.route('/post_facility_approval', methods=['POST'])
def facility_approval():
    facility_request_id = request.json['facility_request_id']
    print(facility_request_id)

    result = db.session.execute(
        db.select(FacilityRequest).where(FacilityRequest.facility_request_id == facility_request_id)).scalar_one()
    return facility_request_schema.jsonify(result)


@app.route('/post_facility_toggle', methods=['POST'])
def facility_toggle():
    approved = request.json['approved']
    facility_request_id = request.json['facility_request_id']

    facility_toggle_result = db.session.execute(
        db.select(FacilityRequest).where(FacilityRequest.facility_request_id == facility_request_id)).scalar_one()

    facility_toggle_result.approved = approved
    db.session.add(facility_toggle_result)
    db.session.commit()

    return facility_request_schema.jsonify(facility_toggle_result)


@app.route('/post_faculty_message', methods=['POST'])
def faculty_message():
    response = request.json['app_response']
    app_id = request.json['app_id']
    approved = request.json['approved']

    appointment_id = db.session.execute(
        db.select(AppointmentRequests).where(AppointmentRequests.app_id == app_id)).scalar_one()

    appointment_id.app_response = response
    appointment_id.approved = approved
    db.session.add(appointment_id)
    db.session.commit()

    return appointment_request_schema.jsonify(appointment_id)


@app.route('/post_access_toggle', methods=['POST'])
def access_toggle():
    approved = request.json['approved']
    access_id = request.json['access_id']

    access_toggle_result = db.session.execute(
        db.select(AccessRequest).where(AccessRequest.access_id == access_id)).scalar_one()

    access_toggle_result.approved = approved
    db.session.add(access_toggle_result)
    db.session.commit()

    return appointment_request_schema.jsonify(access_toggle)


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
    approved = request.json['approved']

    # print("Activity:")
    # print(facility_activity)
    # print("Activity:")
    # print(facility_additional_eq)

    dateformat = '%I:%M %p, %d-%m-%Y'
    facility_date_start = datetime.strptime(facility_date_start, dateformat)
    facility_date_end = datetime.strptime(facility_date_end, dateformat)

    new_facility = FacilityRequest(facility_request_id, facility_id, facility_request_title, facility_date_start,
                                   facility_date_end,
                                   facility_activity, facility_additional_eq, student_id, approved)

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
    approved = request.json["approved"]

    dateformat = '%I:%M %p, %d-%m-%Y'
    access_date_start = datetime.strptime(access_date_start, dateformat)
    access_date_end = datetime.strptime(access_date_end, dateformat)

    new_access = AccessRequest(access_id, access_title, access_date_start, access_date_end, access_message, facility_id,
                               student_id, approved)

    db.session.add(new_access)
    db.session.commit()

    return access_request_schema.jsonify(new_access)


if __name__ == '__main__':
    app.run(debug=True)
