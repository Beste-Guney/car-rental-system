from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.db import connection
from django.views import View
from account.forms import CustomerCreationForm, UserLoginForm
from customer.views import CustomerDashboard


# Create your views here.

def createUserTable():
    cursor = connection.cursor()
    cursor.execute(
        'create table if not exists user(user_id int not null auto_increment, password varchar(50) not null, email varchar(50) not null, address varchar(50), phone_number varchar(15), primary key(user_id)) engine=InnoDB')

    return 'User table created'


def createCustomerTable():
    cursor = connection.cursor()
    cursor.execute(
        'create table if not exists customer(user_id int not null auto_increment, '
        U'date_of_birth varchar(50), nationality varchar(50), discount_rate varchar(50), customer_status varchar(15),'
        U'customer_name varchar(30), foreign key(user_id) references user(user_id) on delete cascade on update cascade)engine=InnoDB;')


    return 'Customer table created'


def createEmployeeTable():
    cursor = connection.cursor()
    cursor.execute(
        'create table if not exists employee(user_id int not null auto_increment, '
        U'salary numeric(8,2), employee_name varchar(50), foreign key(user_id) references user(user_id) on delete cascade on update cascade, primary key(user_id))engine=InnoDB;')


    return 'Employee table created'


def createBranchEmployeeTable():
    cursor = connection.cursor()
    cursor.execute(
        'create table if not exists branch_employee(user_id int not null, '
        U'years_of_work int, foreign key(user_id) references employee(user_id) on delete cascade on update cascade, primary key(user_id))engine=InnoDB;')

    return 'Branch employee table created'


def createDamageExpertTable():
    cursor = connection.cursor()
    cursor.execute(
        'create table if not exists damage_expertise(user_id int not null, '
        U'interest_car_type varchar(50), foreign key(user_id) references employee(user_id) on delete cascade on update cascade, primary key(user_id))engine=InnoDB;')

    return 'Damage Expert table created'


def createManagerTable():
    cursor = connection.cursor()
    cursor.execute(
        'create table if not exists manager(user_id int not null, '
        U'years_of_management int, foreign key(user_id) references employee(user_id) on delete cascade on update cascade, primary key(user_id))engine=InnoDB;')

    return 'Manager table created'


def createChauffeurTable():
    cursor = connection.cursor()
    cursor.execute(
        'create table if not exists chauffeur(user_id int not null, '
        U'drive_car_type varchar(50), driving_years int, foreign key(user_id) references employee(user_id) on delete cascade on update cascade, primary key(user_id))engine=InnoDB;')

    return 'Chauffeur table created'


def createBranchTable():
    cursor = connection.cursor()
    cursor.execute(
        'create table if not exists branch(branch_id int not null auto_increment, '
        U'budget int, branch_name varchar(20), manager_id int, city varchar(20), foreign key(manager_id) references manager(user_id) on update cascade, primary key(branch_id))engine=InnoDB;')

    return 'Branch table created'


# methods to insert into some necessary tables
def insertIntoBranch(branch, budget, city):
    cursor = connection.cursor()
    cursor.execute('insert into branch(branch_name, budget, city) values(' + branch + ',' + budget + ',' + city + ');')


def insertIntoEmployee(name, salary, branch_id):
    cursor = connection.cursor()
    cursor.execute(
        'insert into employee(employee_name, salary, branch_id) values(' + name + ',' + salary + ',' + branch_id + ');')


def insertIntoManager(years, id):
    cursor = connection.cursor()
    cursor.execute(
        'insert into manager(years_of_management, user_id) values(' + years + ',' + id + ');')


# adding foreign key to employee
def alterEmployee():
    cursor = connection.cursor()
    cursor.execute(
        'alter table employee add branch_id int;'
        'alter table employee add foreign key (branch_id) references branch(branch_id);')


class RegisterCustomer(View):
    createUserTable()
    createCustomerTable()

    def post(self, request):
        form = CustomerCreationForm(request.POST)
        print(form.errors)
        if form.is_valid():
            print('not valid')
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            username = form.cleaned_data['username']
            phone_number = form.cleaned_data['phone_number']
            address = form.cleaned_data['address']
            state = form.cleaned_data['state']
            # birth = form.cleaned_data['birth_date']

            cursor = connection.cursor()
            cursor.execute(
                'insert into user(email, password, address, phone_number) values(\'' + email + '\',\'' + password + '\',\'' + address + '\',\'' + phone_number + '\');'
            )

            cursor2 = connection.cursor()
            cursor2.execute(
                'select user_id from user where email=\'' + email + '\' and password=\'' + password + '\''
            )
            desc = cursor2.fetchall()
            desc = desc[0]
            user_id = desc[0]

            cursor3 = connection.cursor()
            cursor3.execute(
                'insert into customer values(\'' + str(
                    user_id) + '\',\'' + '1999-08-21' + '\',\'' + state + '\',\'' + str(
                    0) + '\',\'' + 'active' + '\',\'' + username + '\');'
            )
            request.session['logged_in_user'] = user_id
            request.session['user_type'] = 'customer'
            return render(request, 'customerDashboard.html')
        else:
            form = CustomerCreationForm()
            context = {'form': form}
            return render(request, 'customerRegister.html', context)

    def get(self, request):
        form = CustomerCreationForm()
        context = {'form': form}
        return render(request, 'customerRegister.html', context)


class LoginView(View):
    # creating related tables at db
    createUserTable()
    createCustomerTable()
    createEmployeeTable()
    createBranchEmployeeTable()
    createManagerTable()
    createDamageExpertTable()
    createChauffeurTable()
    createBranchTable()

    # alterEmployee()

    # post request
    def post(self, request):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # checking if user exists
            cursor = connection.cursor()
            cursor.execute(
                'select user_id from user where email=\'' + email + '\' and password=\'' + password + '\''
            )
            desc = cursor.fetchall()

            if len(desc) == 0:
                return redirect('login_user')

            # storing user_id in session
            desc = desc[0]
            user_id = desc[0]
            request.session['logged_in_user'] = user_id

            # checking if user is employee or customer
            cursor.execute(
                'select user_id from customer where user_id=\'' + str(user_id) + '\''
            )
            desc = cursor.fetchall()

            if len(desc) == 0:
                # then user is an employee
                cursor.execute(
                    'select * from branch_employee where user_id=\'' + str(user_id) + '\''
                )
                desc = cursor.fetchall()
                if len(desc) == 0:
                    cursor.execute(
                        'select * from manager where user_id=\'' + str(user_id) + '\''
                    )
                    desc = cursor.fetchall()
                    if len(desc) == 0:
                        cursor.execute(
                            'select * from damage_expertise where user_id=\'' + str(user_id) + '\''
                        )
                        desc = cursor.fetchall()
                        if len(desc) == 0:
                            request.session['user_type'] = 'chauffeur'
                        else:
                            request.session['user_type'] = 'damage_expert'
                    else:
                        request.session['user_type'] = 'manager'
                        return redirect('manager:manager_dashboard', manager_id=user_id)
                else:
                    request.session['user_type'] = 'branch_employee'
                    return redirect('employee:employee-dashboard', employee_id=user_id)
                desc = cursor.fetchall()
                print()
            else:
                request.session['user_type'] = 'customer'
            return redirect('customer:customer_dashboard')
        else:
            form = UserLoginForm()
            context = {'form': form}
            return render(request, 'login.html', context)

    def get(self, request):
        form = UserLoginForm()
        context = {'form': form}
        return render(request, 'login.html', context)
