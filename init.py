import mysql.connector
from mysql.connector import Error

try:
    connection = mysql.connector.connect(host='127.0.0.1',
                                         database='rental3',
                                         user='root',
                                         password='root')


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
    result = cursor.execute("DROP TRIGGER IF EXISTS assert_availability_car")
    result = cursor.execute("DROP TRIGGER IF EXISTS assert_reservation_control")
    result = cursor.execute("DROP PROCEDURE IF EXISTS insert_user")
    result = cursor.execute("DROP PROCEDURE IF EXISTS select_employees")
    result = cursor.execute("DROP PROCEDURE IF EXISTS insert_employee")


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
                user_id int not null,
                license_number int,
                license_type char(3),
                received_date date,
                check (license_type in ("A1", "A2", "A", "M", "B1", "B", "BE", "C1", "C", "CE")),
                FOREIGN KEY (user_id) REFERENCES user(user_id)
                on delete CASCADE
                on update CASCADE,
                PRIMARY KEY (license_number)) ENGINE=INNODB;""")
    print("Driving_License table created successfully ")

    result = cursor.execute("""create table branch(
                branch_id int not null auto_increment,
                budget int,
                branch_name varchar(20),
                PRIMARY KEY (branch_id)) ENGINE=INNODB;""")
    print("Branch table created successfully ")

    result = cursor.execute("""create table employee(
                user_id int not null,
                salary numeric(8,2),
                employee_name varchar(20),
                branch_id int not null,
                FOREIGN KEY (branch_id) REFERENCES branch(branch_id)
                on delete CASCADE
                on update CASCADE,
                FOREIGN KEY (user_id) REFERENCES user(user_id)
                on delete CASCADE 
                on update CASCADE,
                PRIMARY KEY (user_id)) ENGINE=INNODB;""")
    print("Employee table created successfully")

    result = cursor.execute("""create table customer_discount(
    	    customer_status varchar(10),
    	    discount_rate int,
    	    check (discount_rate in (0, 10, 20, 30)),
    		check (customer_status in ("Gold", "Silver", "Premium", "Normal")),
    		primary key(customer_status)) ENGINE=INNODB;""")
    print("Customer_Discount table created successfully")

    result = cursor.execute("""create table customer(
                user_id int not null,
                date_of_birth date,
                nationality varchar(20),
                customer_status varchar(10),
                customer_name varchar(20),
                FOREIGN KEY (user_id) REFERENCES user(user_id)
                on delete CASCADE 
                on update CASCADE,
                FOREIGN KEY (customer_status) REFERENCES customer_discount(customer_status)
                on delete set null 
                on update CASCADE ,
                PRIMARY KEY (user_id)) ENGINE=INNODB;""")
    print("Customer table created successfully")

    result = cursor.execute("""create table manager(
                user_id int not null,
                years_of_management int,
                FOREIGN KEY (user_id) REFERENCES employee(user_id)
                on delete CASCADE 
                on update CASCADE,
                PRIMARY KEY (user_id)) ENGINE=INNODB;""")
    print("Manager table created successfully")

    result = cursor.execute("""create table model_brand(
            model varchar(15),
            brand varchar(20),
            primary key(model,brand)) ENGINE=INNODB;""")
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
                FOREIGN KEY (buying_manager_id) REFERENCES manager(user_id)
                on delete set null 
                on update CASCADE,
                FOREIGN KEY (branch_id) REFERENCES branch(branch_id)
                on delete set null 
                on update CASCADE ,
                FOREIGN KEY (model,brand) REFERENCES model_brand(model,brand)
                on delete CASCADE 
                on update CASCADE ) ENGINE=INNODB;""")
    print("Vehicle table created successfully")

    result = cursor.execute("""create table car(
                license_plate varchar(8) not null,
                car_type char(1),
                check (car_type in ("A", "B", "C", "D")),
                FOREIGN KEY (license_plate) REFERENCES vehicle(license_plate)
                on delete CASCADE 
                on update CASCADE ,
                PRIMARY KEY (license_plate) ) ENGINE=INNODB;""")
    print("Car table created successfully")

    result = cursor.execute("""create table truck(
                license_plate varchar(8) not null,
                truck_type char(1),
                weight_capacity int,
                check (truck_type in ("A", "B", "C", "D")),
                FOREIGN KEY (license_plate) REFERENCES vehicle(license_plate)
                on delete CASCADE 
                on update CASCADE,
                PRIMARY KEY (license_plate)) ENGINE=INNODB;""")
    print("Truck table created successfully")

    result = cursor.execute("""create table motorcycle(
                license_plate varchar(8) not null,
                motorcycle_type char(1),
                check (motorcycle_type in ("A", "B", "C", "D")),
                FOREIGN KEY (license_plate) REFERENCES vehicle(license_plate)
                on delete CASCADE 
                on update CASCADE ,
                PRIMARY KEY (license_plate)) ENGINE=INNODB;""")
    print("Truck table created successfully")

    result = cursor.execute("""create table job_application(
                application_id int not null auto_increment,
                cv blob,
                name varchar(20),
                primary key (application_id)) ENGINE=INNODB;""")
    print("Job_Application table created successfully")

    result = cursor.execute("""create table inspect(
                application_id int not null,
                manager_id int,
                FOREIGN KEY (application_id) REFERENCES job_application(application_id)
                on delete CASCADE 
                on update CASCADE ,
                FOREIGN KEY (manager_id) REFERENCES manager(user_id)
                on delete CASCADE 
                on update CASCADE ,
                PRIMARY KEY (manager_id, application_id)) ENGINE=INNODB;""")
    print("Job_Application table created successfully")

    result = cursor.execute("""create table branch_employee(
                user_id int not null,
                years_of_work int,
                FOREIGN KEY (user_id) REFERENCES employee(user_id)
                on delete CASCADE 
                on update CASCADE ,
                PRIMARY KEY (user_id)) ENGINE=INNODB;""")
    print("Job_Application table created successfully")

    result = cursor.execute("""create table damage_expertise(
                user_id int not null,
                interest_car_type varchar(20),
                FOREIGN KEY (user_id) REFERENCES employee(user_id)
                on delete cascade 
                on update cascade,
                PRIMARY KEY (user_id)) ENGINE=INNODB;""")
    print("Damage_Expersite table created successfully")

    result = cursor.execute("""create table insurance(
                insurance_price float,
                insurance_type varchar(20),
                primary key(insurance_type)) ENGINE=INNODB;""")
    print("Insurance table created successfully")

    result = cursor.execute("""create table chauffeur(
                user_id int not null,
                drive_car_type varchar(20),
                driving_years int,
                FOREIGN KEY (user_id) REFERENCES employee(user_id)
                on delete cascade 
                on update cascade ,
                PRIMARY KEY (user_id) ) ENGINE=INNODB;""")
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
                isChaufAccepted bool,
                check (isApproved  in ("true", "false")),
                check (status in ("on_rent","accepted", "not_accepted", "canceled", "paid", "not_paid")),
                FOREIGN KEY (reserver) REFERENCES customer(user_id)
                on delete cascade 
                on update cascade,
                FOREIGN KEY (checked_by) REFERENCES branch_employee(user_id)
                on delete set null 
                on update cascade,
                FOREIGN KEY (license_plate) REFERENCES vehicle(license_plate)
                on delete set null 
                on update cascade ,
                FOREIGN KEY (reserved_chauf_id) REFERENCES chauffeur(user_id)
                on delete set null 
                on update cascade,
                PRIMARY KEY (reservation_number)) ENGINE=INNODB;""")
    print("Reservation table created successfully")

    result = cursor.execute("""create table damage_report(
                issue_id int not null auto_increment,
                description text,
                type varchar(20),
                cost float,
                author_expertise_id int not null,
                issued_reservation int not null,
                FOREIGN KEY (author_expertise_id) REFERENCES damage_expertise(user_id)
                on delete cascade 
                on update cascade ,
                FOREIGN KEY (issued_reservation) REFERENCES reservation(reservation_number)
                on delete cascade 
                on update cascade,
                PRIMARY KEY (issue_id)) ENGINE=INNODB;""")
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
                FOREIGN KEY (made_by_customer) REFERENCES customer(user_id)
                on delete cascade 
                on update cascade,
                FOREIGN KEY (from_branch) REFERENCES branch(branch_id)
                on delete cascade 
                on update cascade ,
                FOREIGN KEY (to_branch) REFERENCES branch(branch_id)
                on delete cascade 
                on update cascade ,
                FOREIGN KEY (requested_vehicle) REFERENCES vehicle(license_plate)
                on delete cascade 
                on update cascade,
                FOREIGN KEY (checked_by_employee) REFERENCES branch_employee(user_id)
                on delete set null 
                on update cascade,
                PRIMARY KEY (req_id)) ENGINE=INNODB;""")
    print("Request table created successfully")

    result = cursor.execute("""create table vehicle_rate(
                customer_id int not null,
                license_plate varchar(8) not null,
                comment text,
                score int,
                check (score in (1, 2, 3, 4, 5)),
                FOREIGN KEY (customer_id) REFERENCES customer(user_id)
                on delete cascade 
                on update cascade,
                FOREIGN KEY (license_plate) REFERENCES vehicle(license_plate)
                on delete cascade 
                on update cascade,
                PRIMARY KEY (customer_id, license_plate)) ENGINE=INNODB;""")
    print("Vehicle_rate table created successfully")

    result = cursor.execute("""create table branch_rate(
                customer_id int not null,
                branch_id int not null,
                comment text,
                score int,
                check (score in (1, 2, 3, 4, 5)),
                FOREIGN KEY (customer_id) REFERENCES customer(user_id)
                on delete cascade 
                on update cascade ,
                FOREIGN KEY (branch_id) REFERENCES branch(branch_id)
                on delete cascade 
                on update cascade ,
                PRIMARY KEY (customer_id, branch_id)) ENGINE=INNODB;""")
    print("Branch_rate table created successfully")

    result = cursor.execute("""	create table assign_check(
                assigned_expertise_id int not null,
                assigning_manager_id int not null,
                assigned_vehicle_license_plate varchar(8) not null,
                FOREIGN KEY (assigned_expertise_id) REFERENCES damage_expertise(user_id)
                on delete cascade 
                on update cascade ,
                FOREIGN KEY (assigning_manager_id) REFERENCES manager(user_id)
                on delete cascade 
                on update cascade,
                FOREIGN KEY (assigned_vehicle_license_plate) REFERENCES vehicle(license_plate)
                on delete cascade 
                on update cascade ,
                PRIMARY KEY (assigned_expertise_id, assigning_manager_id, assigned_vehicle_license_plate)) ENGINE=INNODB;""")
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
    result = cursor.execute("""insert into branch values(1, 150000000,"Ankara");""")
    result = cursor.execute("""insert into branch values(2, 270000,"Istanbul");""")
    result = cursor.execute("""insert into branch values(3, 15000,"New York");""")

    # employee
    result = cursor.execute("""insert into employee values(105, 6000,"Ahmet Mehmet",1);""")
    result = cursor.execute("""insert into employee values(106, 6100,"Ayse Fatma",1);""")
    result = cursor.execute("""insert into employee values(104, 15000,"Kaan Atesel",1);""")
    result = cursor.execute("""insert into employee values(107, 7000,"Hamza Erdogan",1);""")
    result = cursor.execute("""insert into employee values(108, 10000,"Mehmet Aydin",2);""")
    result = cursor.execute("""insert into employee values(109, 15000,"Ahmet Bayrak",2);""")
    result = cursor.execute("""insert into employee values(110, 11111,"Mazimye Celik",2);""")

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

    # vehicle
    result = cursor.execute(
        """insert into vehicle values("06AY6527", "available",300,"Civic","Honda",250000,3,40000,"Automatic",104,1);""")
    result = cursor.execute(
        """insert into vehicle values("06TD1845", "available",400,"320D","BMW",850000,3,70000,"Automatic",104,1);""")
    result = cursor.execute(
        """insert into vehicle values("34GL3100", "available",200,"Polo","Volkswagen",170000,3,65000,"Manual",104,1);""")
    result = cursor.execute(
        """insert into vehicle values("06REK121", "onsale",200,"Polo","Volkswagen",120000,13,120000,"Manual",null,null);""")
    result = cursor.execute(
        """insert into vehicle values("06ATA122", "onsale",250,"A180","Mercedes",200000,5,20000,"Automatic",null,null);""")
    result = cursor.execute(
        """insert into vehicle values("06RBG536", "onsale",250,"218i","BMW",230000,5,63000,"Automatic",null,null);""")
    result = cursor.execute(
        """insert into vehicle values("06FOO536", "onsale",150,"Jetta","Volkswagen",130000,10,80000,"Automatic",null,null);""")
    result = cursor.execute(
        """insert into vehicle values("06BAR764", "onsale",270,"Passat","Volkswagen",210000,6,76000,"Automatic",null,null);""")

    # car
    result = cursor.execute("""insert into car values("06AY6527", "C");""")
    result = cursor.execute("""insert into car values("06TD1845", "D");""")
    result = cursor.execute("""insert into car values("34GL3100", "B");""")
    result = cursor.execute("""insert into car values("06REK121", "B");""")
    result = cursor.execute("""insert into car values("06ATA122", "B");""")
    result = cursor.execute("""insert into car values("06RBG536", "C");""")
    result = cursor.execute("""insert into car values("06FOO536", "C");""")
    result = cursor.execute("""insert into car values("06BAR764", "D");""")

    # truck

    # motorcycle

    # job application

    # inspect

    # branch_employee
    result = cursor.execute("""insert into branch_employee values(106, 3);""")
    result = cursor.execute("""insert into branch_employee values(109, 3);""")

    # damage_expertise
    result = cursor.execute("""insert into damage_expertise values(105, 10);""")

    # damage report

    # chauffeur
    result = cursor.execute("""insert into chauffeur values(107, "car", 20);""")
    result = cursor.execute("""insert into chauffeur values(110, "car", 20);""")

    # reservation
    # result = cursor.execute(
    #     """insert into reservation values(1, STR_TO_DATE("12-17-2021","%m-%d-%Y"), STR_TO_DATE("12-27-2021","%m-%d-%Y"), "accepted", 3000, 100, 106, "true", "asdas", "Full Coverage", "06AY6527", null, null);""")

    # result = cursor.execute(
    #     """insert into reservation values(2, STR_TO_DATE("11-17-2021","%m-%d-%Y"), STR_TO_DATE("12-27-2021","%m-%d-%Y"), "canceled", 70000, 100, 106, "true", "asdas", "Full Coverage", "06AY6527", null, null);""")
    #
    # result = cursor.execute(
    #     """insert into reservation values(3, STR_TO_DATE("11-17-2021","%m-%d-%Y"), STR_TO_DATE("11-27-2021","%m-%d-%Y"), "not_accepted", 7, 100, 106, "true", "asdas", "Full Coverage", "06AY6527", null, null);""")
    #
    # result = cursor.execute(
    #     """insert into reservation values(4, STR_TO_DATE("10-17-2021","%m-%d-%Y"), STR_TO_DATE("10-27-2021","%m-%d-%Y"), "not_accepted", 120, 100, 106, "true", "asdas", "Full Coverage", "06AY6527", null, null);""")
    #
    # result = cursor.execute(
    #     """insert into reservation values(5, STR_TO_DATE("9-17-2021","%m-%d-%Y"), STR_TO_DATE("12-27-2021","%m-%d-%Y"), "not_accepted", 450, 100, 106, "true", "asdas", "Full Coverage", "06AY6527", null, null);""")
    #
    # result = cursor.execute(
    #     """insert into reservation values(6, STR_TO_DATE("9-17-2021","%m-%d-%Y"), STR_TO_DATE("12-27-2021","%m-%d-%Y"), "not_accepted", 56, 100, 106, "true", "asdas", "Full Coverage", "06AY6527", null, null);""")
    #
    # result = cursor.execute(
    #     """insert into reservation values(7, STR_TO_DATE("9-17-2021","%m-%d-%Y"), STR_TO_DATE("12-27-2021","%m-%d-%Y"), "not_accepted", 17, 100, 106, "true", "asdasf", "Full Coverage", "34GL3100", 107, null);""")
    #
    # result = cursor.execute(
    #     """insert into reservation values(8, STR_TO_DATE("9-17-2021","%m-%d-%Y"), STR_TO_DATE("12-27-2021","%m-%d-%Y"), "not_paid", 17, 100, 106, "true", "asdasf", "Full Coverage", "34GL3100", 107, null);""")
    #
    # result = cursor.execute(
    #     """insert into reservation values(9, STR_TO_DATE("9-17-2021","%m-%d-%Y"), STR_TO_DATE("12-27-2021","%m-%d-%Y"), "not_paid", 17, 100, 106, "true", "asdasf", "Full Coverage", "34GL3100", 107, null);""")
    #
    # result = cursor.execute(
    #     """insert into reservation values(10, STR_TO_DATE("11-19-2021","%m-%d-%Y"), STR_TO_DATE("12-26-2021","%m-%d-%Y"), "paid", 17, 100, 106, "true", "asdasf", "Full Coverage", "34GL3100", 107, null);""")
    #
    # result = cursor.execute(
    #     """insert into reservation values(11, STR_TO_DATE("11-19-2021","%m-%d-%Y"), STR_TO_DATE("12-26-2021","%m-%d-%Y"), "paid", 190, 100, 106, "true", "asdasf", "Full Coverage", "34GL3100", 107, null);""")


    # vehicle_rate
    result = cursor.execute("""insert into vehicle_rate values(100, "06AY6527", "Very good car!", 5);""")
    result = cursor.execute("""insert into vehicle_rate values(102, "34GL3100", "Trash car!", 1);""")

    # branch_rate
    result = cursor.execute("""insert into branch_rate values(100, 1, "Very good branch!", 5);""")
    result = cursor.execute("""insert into branch_rate values(102, 1, "Trash branch!", 1);""")

    # assign_check
    result = cursor.execute("""insert into assign_check values(105, 104, "34GL3100");""")


    #triggers
    #whenever a request is accepted the car is in transfer

    result = cursor.execute("""
    create trigger update_vehicle_status 
    after update on request 
    for each row
    begin 
    if NEW.isApproved = 1 then
    update vehicle set status = "available"
    where vehicle.license_plate = NEW.requested_vehicle; end if;
    end;""")

    # whenever a branch manager buys a car update branch budget
    result = cursor.execute("""
    create trigger update_branch_budget
    after update on vehicle 
    for each row 
    begin
    if OLD.status = "onsale" then
    update branch set budget = budget - OLD.price
    where branch.branch_id = NEW.branch_id;
    end if;
    end;
    """)

    # whenever a customer makes a reservation check whether car is available
    result = cursor.execute("""
    create trigger assert_availability_car before insert on reservation
    for each row 
    begin 
    if exists(select * from reservation where  NEW.start_date > start_date and NEW.end_date < end_date and NEW.license_plate = reservation.license_plate) then
    SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'BIG Errorrrr';
    end if;
    end;
    """)

    #whenevere a customer makes a request check whether there is another reservation at that time
    result = cursor.execute("""
           create trigger assert_reservation_control before insert on reservation
           for each row 
           begin 
           if exists(select * from reservation where  NEW.start_date > start_date and NEW.end_date < end_date and NEW.reserver = reservation.reserver) then
           SIGNAL SQLSTATE '45000'
               SET MESSAGE_TEXT = 'BIG Errorrrr';
           end if;
           end;
           """)

    #stored procedures
    #inserting user
    result = cursor.execute("""create procedure insert_user( in emailValue varchar(50), in passwordValue varchar(50), in addressValue varchar(50), in phone varchar(15))
    begin
        insert into user(email, password, address, phone_number) values( emailValue, passwordValue, addressValue, phone);
    end;""")

    #selecting employees of a branch
    cursor.execute("""create procedure select_employees(in branch int, in manager int)
    begin
        select * from employee where branch_id= branch and user_id <> manager;
    end""")

    #inserting a new employee to a branch
    cursor.execute("""create procedure insert_employee(in userId int , in sal numeric(8,2), in name varchar(20), in branch int)
    begin 
        insert into employee(user_id, salary, employee_name, branch_id) values(userId, sal, name, branch );
    end""")
    connection.commit()

except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
