from django.shortcuts import render, redirect
from django.views import View
from django.db import connection
from django.views.generic.list import ListView
from django.http import JsonResponse
from manager.forms import BranchEmployeeCreationForm, ChauffeurCreationForm, DamageExpertCreationForm


def CreateModelBrandTable():
    cursor = connection.cursor()
    cursor.execute(
        'create table if not exists modelBrand(model varchar(15),brand varchar(20),primary key(model))engine=InnoDB;')

    return 'Model brand created'


def CreateReservationTable():
    cursor = connection.cursor()
    sql = """CREATE TABLE reservation(
        reservation_number int not null auto_increment,
	    start_date date,
	    end_date date,
	    status varchar(10) DEFAULT 'not_paid' CHECK (status IN ('on_rent', 'accepted', 'not_accepted', 'canceled', 'paid', 'not_paid')),
	    cost float,
	    reserver int not null REFERENCES customer(user_id),
	    checked_by int REFERENCES branch_employee(user_id),
	    isApproved boolean DEFAULT false,
	    reason text,
	    insurance_type varchar(10) REFERENCES insurance(insurance_type),
	    license_plate varchar(8) REFERENCES vehicle(license_plate),
	    reserved_chauf_id int REFERENCES chauffeur(user_id),
	    isChaufAccepted boolean,
        PRIMARY KEY(reservation_number)
 )engine=InnoDB;"""

    cursor.execute(sql)

    return 'Reservation table created'


def CreateBranchEmployeeTable():
    cursor = connection.cursor()
    sql = """CREATE TABLE if not exists branch_employee(
            user_id int not null REFERENCES employee(user_id),
            years_of_work int,
            PRIMARY KEY (user_id)
            )engine=InnoDB;"""
    cursor.execute(sql)

    return 'Branch Employee created'


def CreateVehicleRateTable():
    cursor = connection.cursor()
    sql = """CREATE TABLE vehicle_rate(
            customer_id int not null REFERENCES customer(user_id),
            license_plate varchar(8) not null REFERENCES vehicle(license_plate),
            comment text,
            score int check (score in (1, 2, 3, 4, 5)),
            PRIMARY KEY (customer_id, license_plate)
            )engine=InnoDB;"""
    cursor.execute(sql)

    return 'Vehicle Rate Table created'


def CreateInsuranceTable():
    cursor = connection.cursor()
    sql = """CREATE TABLE if not exists insurance(
                insurance_price float,
                insurance_type varchar(10),
                primary key(insurance_type)
                )engine=InnoDB;"""
    cursor.execute(sql)

    return 'Model brand created'


def CreateRequestTable():
    cursor = connection.cursor()
    sql = """CREATE TABLE request(
            req_id int not null AUTO_INCREMENT,
            made_by_customer int not null REFERENCES customer(user_id),
            from_branch int not null REFERENCES branch(branch_id),
            to_branch int not null REFERENCES branch(branch_id),
            requested_vehicle varchar(8) not null REFERENCES vehicle(license_plate),
            checked_by_employee int REFERENCES branch_employee(user_id),
            isApproved boolean,
            reason text,
            PRIMARY KEY (req_id)
            )engine=InnoDB;"""
    cursor.execute(sql)

    return 'Request table created'


def CreateBranchRateTable():
    cursor = connection.cursor()
    sql = """CREATE TABLE branch_rate(
            customer_id int not null REFERENCES customer(user_id),
            branch_id int not null REFERENCES branch(branch_id),
            comment text,
            score int not null,
            PRIMARY KEY (customer_id, branch_id)
            )engine=InnoDB;"""
    cursor.execute(sql)

    return 'Branch Rate table created'
