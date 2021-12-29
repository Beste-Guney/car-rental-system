import mysql.connector
from mysql.connector import Error

try:
    connection = mysql.connector.connect(host='127.0.0.1',
                                         database='rental2',
                                         user='root',
                                         password='123')

    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)

    # connect to mysql database
    cursor = connection.cursor()

    # drop existing tables
    result = cursor.execute("DROP TABLE IF EXISTS assign_check")
    result = cursor.execute("DROP TABLE IF EXISTS driving_license")
    result = cursor.execute("DROP TABLE IF EXISTS branch_rate")
    result = cursor.execute("DROP TABLE IF EXISTS vehicle_rate")
    result = cursor.execute("DROP TABLE IF EXISTS car")
    result = cursor.execute("DROP TABLE IF EXISTS truck")
    result = cursor.execute("DROP TABLE IF EXISTS motorcycle")
    result = cursor.execute("DROP TABLE IF EXISTS inspect")
    result = cursor.execute("DROP TABLE IF EXISTS job_application")
    result = cursor.execute("DROP TABLE IF EXISTS damage_report")
    result = cursor.execute("DROP TABLE IF EXISTS damage_expertise")
    result = cursor.execute("DROP TABLE IF EXISTS reservation")
    result = cursor.execute("DROP TABLE IF EXISTS insurance")
    result = cursor.execute("DROP TABLE IF EXISTS chauffeur")
    result = cursor.execute("DROP TABLE IF EXISTS request")
    result = cursor.execute("DROP TABLE IF EXISTS vehicle")
    result = cursor.execute("DROP TABLE IF EXISTS model_brand")
    result = cursor.execute("DROP TABLE IF EXISTS customer")
    result = cursor.execute("DROP TABLE IF EXISTS customer_discount")
    result = cursor.execute("DROP TABLE IF EXISTS branch_employee")
    result = cursor.execute("DROP TABLE IF EXISTS manager")
    result = cursor.execute("DROP TABLE IF EXISTS employee")
    result = cursor.execute("DROP TABLE IF EXISTS branch")
    result = cursor.execute("DROP TABLE IF EXISTS user")

    # create tables
    result = cursor.execute("""create table user(
            user_id  int not null auto_increment,
            password varchar(50) not null,
            email  varchar(50) not null,
            address varchar(50),
            phone_number varchar(15),
            primary key (user_id)
            ) ENGINE=INNODB;""")
    print("User table created successfully ")

    result = cursor.execute("""	create table driving_license(
                user_id int not null auto_increment,
                license_number int,
                license_type char(3),
                received_date date,
                check (license_type in ("A1", "A2", "A", "M", "B1", "B", "BE", "C1", "C", "CE")),
                FOREIGN KEY (user_id) REFERENCES user(user_id),
                PRIMARY KEY (license_number)) ENGINE=INNODB;""")
    print("Driving_License table created successfully ")

    result = cursor.execute("""create table branch(
                branch_id int not null auto_increment,
                budget int,
                branch_name varchar(20),
                PRIMARY KEY (branch_id));""")
    print("Branch table created successfully ")

    result = cursor.execute("""create table employee(
                user_id int not null auto_increment,
                salary numeric(8,2),
                employee_name varchar(20),
                branch_id int not null,
                FOREIGN KEY (branch_id) REFERENCES branch(branch_id),
                FOREIGN KEY (user_id) REFERENCES user(user_id),
                PRIMARY KEY (user_id));""")
    print("Employee table created successfully")

    result = cursor.execute("""create table customer_discount(
    	    customer_status varchar(10),
    	    discount_rate int,
    	    check (discount_rate in (0, 10, 20, 30)),
    		check (customer_status in ("Gold", "Silver", "Premium", "Normal")),
    		primary key(customer_status));""")
    print("Customer_Discount table created successfully")

    result = cursor.execute("""create table customer(
                user_id int not null auto_increment,
                date_of_birth date,
                nationality varchar(20),
                customer_status varchar(10),
                customer_name varchar(20),
                check (customer_status in ("Gold", "Silver", "Premium", "Normal")),
                FOREIGN KEY (user_id) REFERENCES user(user_id),
                FOREIGN KEY (customer_status) REFERENCES customer_discount(customer_status),
                PRIMARY KEY (user_id));""")
    print("Customer table created successfully")

    result = cursor.execute("""create table manager(
                user_id int not null auto_increment,
                years_of_management int,
                FOREIGN KEY (user_id) REFERENCES employee(user_id),
                PRIMARY KEY (user_id));""")
    print("Manager table created successfully")

    result = cursor.execute("""create table model_brand(
            model varchar(15),
            brand varchar(20),
            primary key(model,brand));""")
    print("Model_Brand table created successfully")

    result = cursor.execute("""create table vehicle(
                license_plate varchar(8) not null,
                status varchar(20),
                daily_rent_price float,
                model varchar(15),
                brand varchar(20),
                price int,
                age int,
                kilometers int,
                transmission_type varchar(10),
                buying_manager_id int,
                branch_id int,
                check (status in ("on_rent", "onsale", "available", "on_transfer", "unavailable", "reserved")),
                check (transmission_type in ("Automatic", "Manual")),
                PRIMARY KEY (license_plate),
                FOREIGN KEY (buying_manager_id) REFERENCES manager(user_id),
                FOREIGN KEY (branch_id) REFERENCES branch(branch_id),
                FOREIGN KEY (model,brand) REFERENCES model_brand(model,brand));""")
    print("Vehicle table created successfully")

    result = cursor.execute("""create table car(
                license_plate varchar(8) not null,
                car_type char(1),
                check (car_type in ("A", "B", "C", "D")),
                FOREIGN KEY (license_plate) REFERENCES vehicle(license_plate),
                PRIMARY KEY (license_plate) );""")
    print("Car table created successfully")

    result = cursor.execute("""create table truck(
                license_plate varchar(8) not null,
                truck_type char(1),
                weight_capacity int,
                check (truck_type in ("A", "B", "C", "D")),
                FOREIGN KEY (license_plate) REFERENCES vehicle(license_plate),
                PRIMARY KEY (license_plate));""")
    print("Truck table created successfully")

    result = cursor.execute("""create table motorcycle(
                license_plate varchar(8) not null,
                motorcycle_type char(1),
                check (motorcycle_type in ("A", "B", "C", "D")),
                FOREIGN KEY (license_plate) REFERENCES vehicle(license_plate),
                PRIMARY KEY (license_plate));""")
    print("Truck table created successfully")

    result = cursor.execute("""create table job_application(
                application_id int not null auto_increment,
                cv blob,
                name varchar(20),
                primary key (application_id));""")
    print("Job_Application table created successfully")

    result = cursor.execute("""create table inspect(
                application_id int not null,
                manager_id int,
                FOREIGN KEY (application_id) REFERENCES job_application(application_id),
                FOREIGN KEY (manager_id) REFERENCES manager(user_id),
                PRIMARY KEY (manager_id, application_id));""")
    print("Job_Application table created successfully")

    result = cursor.execute("""create table branch_employee(
                user_id int not null,
                years_of_work int,
                FOREIGN KEY (user_id) REFERENCES employee(user_id),
                PRIMARY KEY (user_id));""")
    print("Job_Application table created successfully")

    result = cursor.execute("""create table damage_expertise(
                user_id int not null,
                interest_car_type varchar(20),
                FOREIGN KEY (user_id) REFERENCES employee(user_id),
                PRIMARY KEY (user_id));""")
    print("Damage_Expersite table created successfully")

    result = cursor.execute("""create table insurance(
                insurance_price float,
                insurance_type varchar(20),
                primary key(insurance_type));""")
    print("Insurance table created successfully")

    result = cursor.execute("""create table chauffeur(
                user_id int not null,
                drive_car_type varchar(20),
                driving_years int,
                FOREIGN KEY (user_id) REFERENCES employee(user_id),
                PRIMARY KEY (user_id) );""")
    print("Chauffeur table created successfully")

    # rental_period int(11) AS (DATEDIFF(start_date, end_date)),
    result = cursor.execute("""create table reservation(
                reservation_number int not null auto_increment,
                start_date date,
                end_date date,
                status varchar(15),
                cost float,
                reserver int not null,
                checked_by int,
                isApproved varchar(5),
                reason text,
                insurance_type varchar(20),
                license_plate varchar(8),
                reserved_chauf_id int,
                isChaufAccepted varchar(5),
                check (isApproved  in ("true", "false")),
                check (isChaufAccepted in ("true", "false")),
                check (status in ("on_rent", "accepted", "not_accepted", "canceled", "paid", "not_paid")),
                FOREIGN KEY (reserver) REFERENCES customer(user_id),
                FOREIGN KEY (checked_by) REFERENCES branch_employee(user_id),
                FOREIGN KEY (license_plate) REFERENCES vehicle(license_plate),
                FOREIGN KEY (reserved_chauf_id) REFERENCES chauffeur(user_id),
                PRIMARY KEY (reservation_number));""")
    print("Reservation table created successfully")

    result = cursor.execute("""create table damage_report(
                issue_id int not null,
                description text,
                type varchar(20),
                cost float,
                author_expertise_id int not null,
                issued_reservation int not null,
                FOREIGN KEY (author_expertise_id) REFERENCES damage_expertise(user_id),
                FOREIGN KEY (issued_reservation) REFERENCES reservation(reservation_number),
                PRIMARY KEY (issue_id));""")
    print("Damage_Report table created successfully")

    result = cursor.execute("""create table request(
                req_id int not null auto_increment,
                made_by_customer int not null,
                from_branch int not null,
                to_branch int not null,
                requested_vehicle varchar(8) not null,
                checked_by_employee int,
                isApproved boolean,
                reason varchar(50),
                FOREIGN KEY (made_by_customer) REFERENCES customer(user_id),
                FOREIGN KEY (from_branch) REFERENCES branch(branch_id),
                FOREIGN KEY (to_branch) REFERENCES branch(branch_id),
                FOREIGN KEY (requested_vehicle) REFERENCES vehicle(license_plate),
                FOREIGN KEY (checked_by_employee) REFERENCES branch_employee(user_id),
                PRIMARY KEY (req_id));""")
    print("Request table created successfully")

    result = cursor.execute("""create table vehicle_rate(
                customer_id int not null,
                license_plate varchar(8) not null,
                comment text,
                score int,
                check (score in (1, 2, 3, 4, 5)),
                FOREIGN KEY (customer_id) REFERENCES customer(user_id),
                FOREIGN KEY (license_plate) REFERENCES vehicle(license_plate),
                PRIMARY KEY (customer_id, license_plate));""")
    print("Vehicle_rate table created successfully")

    result = cursor.execute("""create table branch_rate(
                customer_id int not null,
                branch_id int not null,
                comment text,
                score int,
                check (score in (1, 2, 3, 4, 5)),
                FOREIGN KEY (customer_id) REFERENCES customer(user_id),
                FOREIGN KEY (branch_id) REFERENCES branch(branch_id),
                PRIMARY KEY (customer_id, branch_id));""")
    print("Branch_rate table created successfully")

    result = cursor.execute("""	create table assign_check(
                assigned_expertise_id int not null,
                assigning_manager_id int not null,
                assigned_vehicle_license_plate varchar(8) not null,
                FOREIGN KEY (assigned_expertise_id) REFERENCES damage_expertise(user_id),
                FOREIGN KEY (assigning_manager_id) REFERENCES manager(user_id),
                FOREIGN KEY (assigned_vehicle_license_plate) REFERENCES vehicle(license_plate),
                PRIMARY KEY (assigned_expertise_id, assigning_manager_id, assigned_vehicle_license_plate));""")
    print("Assign_check table created successfully")

    # insert tuples to tables

    # user
    result = cursor.execute(
        """insert into user values(100,"asd123","ardaonal@gmail.com","ankara,cankaya","5055821811");""")
    result = cursor.execute(
        """insert into user values(101,"asd123","besteguney@gmail.com","ankara,cankaya","5055856811");""")
    result = cursor.execute(
        """insert into user values(102,"asd123","farukguney@gmail.com","ankara,cankaya","5325856811");""")
    result = cursor.execute(
        """insert into user values(104,"asd123","kaanatesel@gmail.com","ankara,cankaya","5327756811");""")
    result = cursor.execute(
        """insert into user values(105,"asd123","ahmetmehmet@gmail.com","istanbul","5321156811");""")
    result = cursor.execute("""insert into user values(106,"asd123","aysefatma@gmail.com","izmir","5321156861");""")
    result = cursor.execute("""insert into user values(107,"asd123","hamzaerdogan@gmail.com","rize","5311156761");""")
    result = cursor.execute("""insert into user values(108,"asd123","mehmet@gmail.com","tokat","5311156761");""")
    result = cursor.execute("""insert into user values(109,"asd123","ahmet@gmail.com","trabzon","2545435435");""")
    result = cursor.execute("""insert into user values(110,"asd123","metin@gmail.com","malatya","12243242");""")

    # driving_license
    result = cursor.execute(
        """insert into driving_license values(100,55667788,"B1",STR_TO_DATE("07-25-2012","%m-%d-%Y"));""")
    result = cursor.execute(
        """insert into driving_license values(101,33667788,"A1",STR_TO_DATE("03-16-2018","%m-%d-%Y"));""")
    result = cursor.execute(
        """insert into driving_license values(102,33117788,"C1",STR_TO_DATE("12-21-2019","%m-%d-%Y"));""")

    # customer_discount
    result = cursor.execute("""insert into customer_discount values("Gold",30);""")
    result = cursor.execute("""insert into customer_discount values("Silver",20);""")
    result = cursor.execute("""insert into customer_discount values("Premium",10);""")
    result = cursor.execute("""insert into customer_discount values("Normal",0);""")

    # model_brand
    result = cursor.execute("""insert into model_brand values("Polo", "Volkswagen");""")
    result = cursor.execute("""insert into model_brand values("Golf", "Volkswagen");""")
    result = cursor.execute("""insert into model_brand values("Passat", "Volkswagen");""")
    result = cursor.execute("""insert into model_brand values("Jetta","Volkswagen");""")
    result = cursor.execute("""insert into model_brand values("A180", "Mercedes");""")
    result = cursor.execute("""insert into model_brand values("C200", "Mercedes");""")
    result = cursor.execute("""insert into model_brand values("S600", "Mercedes");""")
    result = cursor.execute("""insert into model_brand values("320D", "BMW");""")
    result = cursor.execute("""insert into model_brand values("218i", "BMW");""")
    result = cursor.execute("""insert into model_brand values("X6", "BMW");""")
    result = cursor.execute("""insert into model_brand values("X1", "BMW");""")
    result = cursor.execute("""insert into model_brand values("Civic", "Honda");""")
    result = cursor.execute("""insert into model_brand values("CRV", "Honda");""")
    result = cursor.execute("""insert into model_brand values("Cooper", "Mini");""")
    # motor, kamyon vb. turleri eklenecek

    # insurance
    result = cursor.execute("""insert into insurance values(3231, "Full Coverage");""")
    result = cursor.execute("""insert into insurance values(1000, "Semi Coverage");""")
    result = cursor.execute("""insert into insurance values(500, "Low Coverage");""")

    # branch
    result = cursor.execute("""insert into branch values(1, 150000,"Ankara");""")
    result = cursor.execute("""insert into branch values(2, 270000,"Istanbul");""")
    result = cursor.execute("""insert into branch values(3, 1500000,"New York");""")

    # employee
    result = cursor.execute("""insert into employee values(105, 6000,"Ahmet Mehmet",1);""")
    result = cursor.execute("""insert into employee values(106, 6100,"Ayse Fatma",1);""")
    result = cursor.execute("""insert into employee values(104, 15000,"Kaan Atesel",1);""")
    result = cursor.execute("""insert into employee values(107, 7000,"Hamza Erdogan",1);""")
    result = cursor.execute("""insert into employee values(108, 10000,"Mehmet Aydın",1);""")
    result = cursor.execute("""insert into employee values(109, 15000,"Melis Bayrak",1);""")
    result = cursor.execute("""insert into employee values(110, 11111,"Mazimye Celik",1);""")

    # customer
    result = cursor.execute(
        """insert into customer values(100, STR_TO_DATE("08-24-2001","%m-%d-%Y"),"Turkey","Premium","Arda Onal");""")
    result = cursor.execute(
        """insert into customer values(101, STR_TO_DATE("11-17-2001","%m-%d-%Y"),"Turkey","Gold","Beste Guney");""")
    result = cursor.execute(
        """insert into customer values(102, STR_TO_DATE("03-06-2001","%m-%d-%Y"),"Turkey","Silver","Faruk Guney");""")

    # manager
    result = cursor.execute("""insert into manager values(104, 3);""")
    result = cursor.execute("""insert into manager values(108, 8);""")
    result = cursor.execute("""insert into manager values(109, 12);""")

    # vehicle
    result = cursor.execute(
        """insert into vehicle values("06AY6527", "available",300,"Civic","Honda",250000,3,40000,"Automatic",104,1);""")
    result = cursor.execute(
        """insert into vehicle values("06TD1845", "available",400,"320D","BMW",850000,3,70000,"Automatic",104,1);""")
    result = cursor.execute(
        """insert into vehicle values("34GL3100", "available",200,"Polo","Volkswagen",170000,3,65000,"Manual",104,1);""")
    result = cursor.execute(
        """insert into vehicle values("06REK121", "onsale",200,"Polo","Volkswagen",120000,13,120000,"Manual",null,null);""")

    # car
    result = cursor.execute("""insert into car values("06AY6527", "C");""")
    result = cursor.execute("""insert into car values("06TD1845", "D");""")
    result = cursor.execute("""insert into car values("34GL3100", "B");""")

    # truck

    # motorcycle

    # job application

    # inspect

    # branch_employee
    result = cursor.execute("""insert into branch_employee values(106, 3);""")

    # damage_expertise
    result = cursor.execute("""insert into damage_expertise values(105, 10);""")

    # damage report

    # reservation
    result = cursor.execute(
        """insert into reservation values(1, STR_TO_DATE("12-17-2021","%m-%d-%Y"), STR_TO_DATE("12-27-2021","%m-%d-%Y"), "not_accepted", 3000, 100, 106, "true", "asdas", "Full Coverage", "06AY6527", null, null);""")  

    # chauffeur
    result = cursor.execute("""insert into chauffeur values(107, "car", 20);""")

    # vehicle_rate
    result = cursor.execute("""insert into vehicle_rate values(100, "06AY6527", "Very good car!", 5);""")
    result = cursor.execute("""insert into vehicle_rate values(102, "34GL3100", "Trash car!", 1);""")

    # branch_rate
    result = cursor.execute("""insert into branch_rate values(100, 1, "Very good branch!", 5);""")
    result = cursor.execute("""insert into branch_rate values(102, 1, "Trash branch!", 1);""")

    # assign_check
    result = cursor.execute("""insert into assign_check values(105, 104, "34GL3100");""")

    connection.commit()

except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
