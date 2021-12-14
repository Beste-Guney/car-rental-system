from django.shortcuts import render, redirect
from django.views import View
from django.db import connection
from django.http import JsonResponse
from manager.forms import BranchEmployeeCreationForm, ChauffeurCreationForm, DamageExpertCreationForm


# Create your views here.
def createModelBrandTable():
    cursor = connection.cursor()
    cursor.execute(
        'create table if not exists modelBrand(model varchar(15),brand varchar(20),primary key(model))engine=InnoDB;')

    return 'Model brand created'


def createVehicleTable():
    cursor = connection.cursor()
    cursor.execute(
        'create table if not exists vehicle(license_plate varchar(8) not null,status varchar(20),daily_rent_price float,model varchar(15),price int,age int,kilometers int,transmission_type varchar(10),buying_manager_id int,branch_id int,check (status in ( \'on_rent\', \'available\', \'on_transfer\', \'onsale\', \'reserved\')),check (transmission_type in (\'Automatic\', \'Manual\')),PRIMARY KEY (license_plate),FOREIGN KEY (buying_manager_id) REFERENCES manager(user_id) on update cascade ,FOREIGN KEY (branch_id) REFERENCES branch(branch_id) on update cascade ,FOREIGN KEY (model) REFERENCES modelBrand(model) on delete cascade on update cascade)engine=InnoDB;')


    return 'Vehicle created'


class ManagerMainPage(View):
    createModelBrandTable()
    createVehicleTable()

    def get(self, request, manager_id):
        cursor = connection.cursor()
        cursor.execute(
            'select * from employee where user_id=\'' + str(manager_id) + '\''
        )
        result = cursor.fetchall()
        result = result[0]
        branch_id = result[3]
        employee_name = result[2]

        # finding the branch
        cursor.execute(
            'select * from branch where branch_id=\'' + str(branch_id) + '\''
        )
        result = cursor.fetchall()
        result = result[0]
        branch_name = result[2]

        return render(request, 'managerDashboard.html',
                      {'branch_id': branch_id, 'branch_name': branch_name, 'name': employee_name})


class BranchCarView(View):

    def get(self, request, branch_id):
        cursor = connection.cursor()
        cursor.execute(
            'select * from vehicle where branch_id=\'' + str(branch_id) + '\''
        )
        result = cursor.fetchall()

        # storing vehicle info in arrays
        vehicle_info = []

        for car in result:
            item_detail = [car[0], car[1], car[2], car[3], car[4], car[5], car[6]]
            vehicle_info.append(item_detail)

        cursor.execute(
            'select branch_name from branch where branch_id=\'' + str(branch_id) + '\''
        )
        result = cursor.fetchall()
        result = result[0]
        name = result[0]
        return render(request, 'branchCarsManaager.html',
                      {'vehicles': vehicle_info, 'name': name, 'branch_id': branch_id})


class BuyCarView(View):
    def get(self, request, branch_id):
        cursor = connection.cursor()
        cursor.execute(
            'select * from vehicle where status=\'onsale\''
        )
        result = cursor.fetchall()
        vehicle_info = []

        for car in result:
            item_detail = [car[0], car[1], car[2], car[3], car[4], car[5], car[6]]

            vehicle_info.append(item_detail)

        models, brands = models_and_brands()

        #sending models
        return render(request, 'managerBuyCars.html', {'vehicles': vehicle_info, 'branch_id' : branch_id, 'models': models, 'brands': brands})


def models_and_brands():
    # sending existing models from db to view
    cursor = connection.cursor()
    cursor.execute(
        'select * from modelBrand;'
    )
    result = cursor.fetchall()
    models = []

    for res in result:
        models.append(res[0])

    #sending existng brands
    brands = set()

    for res in result:
        brands.add(res[1])

    return models, brands


def ajaxBuyCar(request):
    print('called')
    vehicle_plate = request.GET.get('car_plate', None)
    manager = request.GET.get('manager_id', None)
    print(manager)
    # checking if we can afford it
    cursor = connection.cursor()
    cursor.execute(
        'select budget, branch_id from branch where manager_id=\'' + manager + '\''
    )
    result = cursor.fetchall()
    result = result[0]  # budget of the branch
    budget = result[0]
    branch_id = result[1]
    print(budget)
    cursor = connection.cursor()
    cursor.execute(
        'select price from vehicle where license_plate=\'' + vehicle_plate + '\''
    )
    result = cursor.fetchall()
    result = result[0]  # budget of the branch
    price = result[0]
    print(price)
    # response data
    data = {}
    data['can_buy'] = True

    if int(price) > int(budget):
        data['can_buy'] = False
        return JsonResponse(data)

    # if we can afford it means that we bought it
    cursor.execute(
        'update vehicle set status = \'available\'  where license_plate = \'' + str(vehicle_plate) + '\';')
    cursor.execute(
        'update vehicle set buying_manager_id = ' + str(manager) + ' where license_plate = \'' + str(
            vehicle_plate) + '\';'
    )
    cursor.execute(
        'update vehicle set branch_id = ' + str(branch_id) + ' where license_plate = \'' + str(vehicle_plate) + '\';'
    )
    cursor.execute(
        'update branch set budget = budget - ' + str(price) + ' where branch_id = \'' + str(branch_id) + '\';'
    )

    return JsonResponse(data)


def findEmployeeType(id):
    cursor = connection.cursor()
    cursor.execute(
        'select * from branch_employee where user_id=' + str(id) + ';'
    )
    result = cursor.fetchall()
    if len(result) == 0:
        cursor.execute(
            'select * from chauffeur where user_id=' + str(id) + ';'
        )
        result = cursor.fetchall()
        if len(result) == 0:
            return 'damage_expertise'
        else:
            return 'chauffeur'
    else:
        return 'branch_employee'


class EmployeeView(View):

    def get(self, request, branch_id):
        # fetching all employees at that branch
        cursor = connection.cursor()
        cursor.execute(
            'select * from employee where branch_id=' + str(branch_id) + ' and user_id <>' + str(
                request.session['logged_in_user']) + ';'
        )
        result = cursor.fetchall()

        employee_list = []

        for emp in result:
            type = findEmployeeType(emp[0])
            employee_info = [emp[0], emp[1], emp[2], type]
            employee_list.append(employee_info)

        cursor.execute(
            'select branch_name from branch where branch_id=\'' + str(branch_id) + '\''
        )
        result = cursor.fetchall()
        result = result[0]
        name = result[0]

        return render(request, 'branchEmployee.html',
                      {'employees': employee_list, 'name': name, 'branch_id': branch_id})


class AddBranchEmployeeView(View):
    def post(self, request):

        # getting current branch
        cursor = connection.cursor()
        cursor.execute(
            'select * from employee where user_id=' + str(
                request.session['logged_in_user']) + ';'
        )
        result = cursor.fetchall()
        result = result[0]
        branch_id = result[3]

        # taking form values
        form = BranchEmployeeCreationForm(request.POST)
        print(form.errors)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = form.cleaned_data['username']
            salary = form.cleaned_data['salary']
            address = form.cleaned_data['address']
            phone_number = form.cleaned_data['phone_number']

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

            # inserting into employee tables
            print('insert into employee(user_id, salary, employee_name, branch_id) values(\'' + str(
                user_id) + '\',\'' + str(salary) + '\',\'' + username + '\',\'' + str(branch_id) + '\' );'
                  )
            cursor.execute(
                'insert into employee(user_id, salary, employee_name, branch_id) values(\'' + str(
                    user_id) + '\',\'' + str(salary) + '\',\'' + username + '\',\'' + str(branch_id) + '\' );')

            cursor.execute(
                'insert into branch_employee(user_id, years_of_work) values(' + str(
                    user_id) + ',' + str(0) + ');'
            )
            return redirect('manager:branch-employees', branch_id)

        else:
            form = BranchEmployeeCreationForm()
            context = {'form': form}
            return render(request, 'managerAddBranchEmployee.html', context)

    def get(self, request):
        # getting current branch
        cursor = connection.cursor()
        cursor.execute(
            'select * from employee where user_id=' + str(
                request.session['logged_in_user']) + ';'
        )
        result = cursor.fetchall()
        result = result[0]
        branch_id = result[3]
        form = BranchEmployeeCreationForm()
        context = {'form': form, 'branch_id': branch_id}
        return render(request, 'managerAddBranchEmployee.html', context)


class AddChauffeurView(View):
    def post(self, request):

        # getting current branch
        cursor = connection.cursor()
        cursor.execute(
            'select * from employee where user_id=' + str(
                request.session['logged_in_user']) + ';'
        )
        result = cursor.fetchall()
        result = result[0]
        branch_id = result[3]

        # taking form values
        form = ChauffeurCreationForm(request.POST)
        print(form.errors)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = form.cleaned_data['username']
            salary = form.cleaned_data['salary']
            address = form.cleaned_data['address']
            phone_number = form.cleaned_data['phone_number']
            car_type = form.cleaned_data['car_type']
            years = form.cleaned_data['years']

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

            # inserting into employee tables
            cursor.execute(
                'insert into employee(user_id, salary, employee_name, branch_id) values(\'' + str(
                    user_id) + '\',\'' + str(salary) + '\',\'' + username + '\',\'' + str(branch_id) + '\' );')

            cursor.execute(
                'insert into chauffeur(user_id, drive_car_type, driving_years) values(' + str(
                    user_id) + ',\'' + car_type + '\',' + str(years) + ');'
            )
            return redirect('manager:branch-employees', branch_id)

        else:
            form = ChauffeurCreationForm()
            context = {'form': form}
            return render(request, 'managerAddChauffeur.html', context)

    def get(self, request):
        # getting current branch
        cursor = connection.cursor()
        cursor.execute(
            'select * from employee where user_id =' + str(
                request.session['logged_in_user']) + ';'
        )
        result = cursor.fetchall()
        result = result[0]
        branch_id = result[3]

        form = ChauffeurCreationForm()
        context = {'form': form, 'branch_id': branch_id}
        return render(request, 'managerAddChauffeur.html', context)


class AddDamageExpertView(View):
    def post(self, request):

        # getting current branch
        cursor = connection.cursor()
        cursor.execute(
            'select * from employee where user_id =' + str(
                request.session['logged_in_user']) + ';'
        )
        result = cursor.fetchall()
        result = result[0]
        branch_id = result[3]

        # taking form values
        form = DamageExpertCreationForm(request.POST)
        print(form.errors)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = form.cleaned_data['username']
            salary = form.cleaned_data['salary']
            address = form.cleaned_data['address']
            phone_number = form.cleaned_data['phone_number']
            car_type = form.cleaned_data['car_type']

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

            # inserting into employee tables
            cursor.execute(
                'insert into employee(user_id, salary, employee_name, branch_id) values(\'' + str(
                    user_id) + '\',\'' + str(salary) + '\',\'' + username + '\',\'' + str(branch_id) + '\' );')

            cursor.execute(
                'insert into damage_expertise(user_id, interest_car_type) values(' + str(
                    user_id) + ',\'' + car_type + '\');'
            )
            return redirect('manager:branch-employees', branch_id)

        else:
            form = DamageExpertCreationForm()
            context = {'form': form}
            return render(request, 'managerAddDamageExpert.html', context)

    def get(self, request):
        # getting current branch
        cursor = connection.cursor()
        cursor.execute(
            'select * from employee where user_id =' + str(
                request.session['logged_in_user']) + ';'
        )
        result = cursor.fetchall()
        result = result[0]
        branch_id = result[3]
        form = DamageExpertCreationForm()
        context = {'form': form, 'branch_id': branch_id}
        return render(request, 'managerAddDamageExpert.html', context)

def filter_car_by_age(request, value):
    #gathering necessary info
    user_id = request.session['logged_in_user']
    cursor = connection.cursor()
    cursor.execute(
        'select * from employee where user_id=\'' + str(user_id) + '\''
    )
    result = cursor.fetchall()
    result = result[0]
    branch_id = result[3]
    employee_name = result[2]

    # getting right cars
    print(        'select * from vehicle where branch_id =' + str(branch_id) + 'and age between' + str(value) + 'and' + str(value + 5) +';'
)
    cursor = connection.cursor()
    cursor.execute(
        'select * from vehicle where branch_id =' + str(branch_id) + ' and age between ' + str(value) + ' and ' + str(value + 5) +';'
    )
    result = cursor.fetchall()
    # storing vehicle info in arrays
    vehicle_info = []

    for car in result:
        item_detail = [car[0], car[1], car[2], car[3], car[4], car[5], car[6]]
        vehicle_info.append(item_detail)

    cursor.execute(
        'select branch_name from branch where branch_id=\'' + str(branch_id) + '\''
    )
    result = cursor.fetchall()
    result = result[0]
    name = result[0]
    return render(request, 'branchCarsManaager.html',
                  {'vehicles': vehicle_info, 'name': name, 'branch_id': branch_id})

