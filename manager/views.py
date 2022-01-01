from django.shortcuts import render, redirect
from django.views import View
from django.db import connection
from django.http import JsonResponse
from manager.forms import BranchEmployeeCreationForm, ChauffeurCreationForm, DamageExpertCreationForm
import datetime

# Create your views here.
# def createModelBrandTable():
#     cursor = connection.cursor()
#     cursor.execute(
#         'create table if not exists modelBrand(model varchar(15),brand varchar(20),primary key(model))engine=InnoDB;')
#
#     return 'Model brand created'
#
#
# def createVehicleTable():
#     cursor = connection.cursor()
#     cursor.execute(
#         'create table if not exists vehicle(license_plate varchar(8) not null,status varchar(20),daily_rent_price float,model varchar(15),price int,age int,kilometers int,transmission_type varchar(10),buying_manager_id int,branch_id int,check (status in ( \'on_rent\', \'available\', \'on_transfer\', \'onsale\', \'reserved\')),check (transmission_type in (\'Automatic\', \'Manual\')),PRIMARY KEY (license_plate),FOREIGN KEY (buying_manager_id) REFERENCES manager(user_id) on update cascade ,FOREIGN KEY (branch_id) REFERENCES branch(branch_id) on update cascade ,FOREIGN KEY (model) REFERENCES modelBrand(model) on delete cascade on update cascade)engine=InnoDB;')
#
#
#     return 'Vehicle created'

def get_branch_employee_info(manager_id):
    cursor = connection.cursor()
    cursor.execute(
        'select * from employee,manager where employee.user_id = manager.user_id and manager.user_id = ' + str(
            manager_id) + '; '
    )
    result = cursor.fetchall()
    for res in result:
        print(res)
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

    return branch_id, branch_name, employee_name

class ManagerMainPage(View):
    # createModelBrandTable()
    # createVehicleTable()

    def get(self, request, manager_id):
        branch_id, branch_name, employee_name = get_branch_employee_info()

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
            item_detail = [car[0], car[1], car[2], car[3], car[4], car[5], car[6], car[7]]
            vehicle_info.append(item_detail)

        cursor.execute(
            'select branch_name from branch where branch_id=\'' + str(branch_id) + '\''
        )
        result = cursor.fetchall()
        result = result[0]
        name = result[0]

        models, brands = models_and_brands()

        return render(request, 'branchCarsManaager.html',
                      {'vehicles': vehicle_info, 'name': name, 'branch_id': branch_id, 'models': models,
                       'brands': brands})


class BuyCarView(View):
    def get(self, request, branch_id):
        cursor = connection.cursor()
        cursor.execute(
            'select * from vehicle where status=\'onsale\''
        )
        result = cursor.fetchall()
        vehicle_info = []

        for car in result:
            item_detail = [car[0], car[1], car[2], car[3], car[4], car[5], car[6], car[7]]

            vehicle_info.append(item_detail)

        models, brands = models_and_brands()

        #sending models
        return render(request, 'managerBuyCars.html', {'vehicles': vehicle_info, 'branch_id' : branch_id, 'models': models, 'brands': brands})


def models_and_brands():
    # sending existing models from db to view
    cursor = connection.cursor()
    cursor.execute(
        'select * from model_brand;'
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
        'select branch.budget, employee.branch_id from employee, branch where employee.branch_id = branch.branch_id and user_id=\'' + manager + '\''
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
        'update vehicle set status = \'available\' , buying_manager_id = ' + str(manager) + ' ,branch_id = ' + str(branch_id) +' where license_plate = \'' + str(vehicle_plate) + '\';')

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
                'call insert_user( \'' + str(email) + '\', \'' + str(password) + '\', \'' + str(
                    address) + '\', \'' + str(phone_number) + '\');' )

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
                'call insert_user( \'' + str(email) + '\', \'' + str(password) + '\', \'' + str(
                    address) + '\', \'' + str(phone_number) + '\');'
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
                'call insert_user( \'' + str(email) + '\', \'' + str(password) + '\', \'' + str(
                    address) + '\', \'' + str(phone_number) + '\');'
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


class FilterView(View):
    def post(self, request):
        user_id = request.session['logged_in_user']
        print(request.POST)

        #finding the branch id information
        cursor = connection.cursor()
        cursor.execute(
            'select * from employee where user_id=\'' + str(user_id) + '\''
        )
        result = cursor.fetchall()
        result = result[0]
        branch_id = result[3]
        employee_name = result[2]

        #finding the branch name
        cursor.execute(
            'select branch_name from branch where branch_id=\'' + str(branch_id) + '\''
        )
        result = cursor.fetchall()
        result = result[0]
        name = result[0]


        #taking filtering conditions from post
        license = request.POST['license']
        age = request.POST['age-vehicle']
        model = request.POST['model-vehicle']
        kilometers = request.POST['kilometers']
        brand = request.POST['brand']
        low = request.POST['lowest']
        high = request.POST['highest']

        print(kilometers)
        #if plate is entered find the car
        if license:
            cursor.execute(
                'create view filter6 as select * from vehicle where license_plate like \'' + license + '%\''
            )
        else:
            cursor.execute(
                'create view filter6 as select * from vehicle;'
            )
         # filtering according to other conditions
        if int(age) != -1:
            print('here1')
            upper_bound = int(age) + 5
            cursor.execute(
                        'create view filter1 as select * from filter6 where age between\'' + str(age) + '\'and \'' + str(upper_bound) +'\';'
            )

        else:
            cursor.execute(
                        'create view filter1 as '
                        'select * from filter6;'
            )

        if model != 'empty':
            cursor.execute(
                        'create view filter2 as select * from filter1 where model=\'' + model + '\';'
            )
        else:
            cursor.execute(
                        'create view filter2 as '
                        'select * from filter1;'
            )

        if int(kilometers) != -1:
            print('here3')

            if int(kilometers) == 40000:
                cursor.execute(
                            'create view filter3 as '
                            'select * from filter2 where kilometers > 40000;'
                )
            else:
                upper_bound = int(kilometers) * 2
                cursor.execute(
                            'create view filter3 as select * from filter2 where kilometers between ' + str(kilometers) + ' and ' + str(upper_bound) +';'
                )


        else:
            cursor.execute(
                        'create view filter3 as '
                        'select * from filter2;'
            )

        if int(high) == 0:
            cursor.execute(
                        'create view filter4 as select * from filter3 where daily_rent_price > ' + str(low) + ';'
            )
        else:
            cursor.execute(
                        'create view filter4 as select * from filter3 where daily_rent_price between ' + str(low) + ' and ' + str(high) +';'
            )

        if brand != 'empty':
            cursor.execute(
                        'create view filter5 as select * from filter4 where brand=\'' + brand + '\';'
            )
        else:
            cursor.execute(
                        'create view filter5 as select * from filter4;'
            )

        #gathering filtered vehicles
        cursor.execute(
                'select * from vehicle, filter5 where vehicle.license_plate = filter5.license_plate and vehicle.branch_id = ' + str(branch_id) + ';'
        )
        result = cursor.fetchall()
        vehicle_info = []

        for car in result:
            item_detail = [car[0], car[1], car[2], car[3], car[4], car[5], car[6]]
            vehicle_info.append(item_detail)

        cursor.execute('drop view filter1')
        cursor.execute('drop view filter2')
        cursor.execute('drop view filter3')
        cursor.execute('drop view filter4')
        cursor.execute('drop view filter5')
        cursor.execute('drop view filter6')
        models, brands = models_and_brands()

        return render(request, 'branchCarsManaager.html',
                              {'vehicles': vehicle_info, 'name': name, 'branch_id': branch_id, 'models': models,
                               'brands': brands})

class FilterForBuyingView(View):
    def post(self, request):
        user_id = request.session['logged_in_user']
        print(request.POST)

        #finding the branch id information
        cursor = connection.cursor()
        cursor.execute(
            'select * from employee where user_id=\'' + str(user_id) + '\''
        )
        result = cursor.fetchall()
        result = result[0]
        branch_id = result[3]
        employee_name = result[2]

        #finding the branch name
        cursor.execute(
            'select branch_name from branch where branch_id=\'' + str(branch_id) + '\''
        )
        result = cursor.fetchall()
        result = result[0]
        name = result[0]


        #taking filtering conditions from post
        license = request.POST['license']
        age = request.POST['age-vehicle']
        print(age)
        model = request.POST['model-vehicle']
        kilometers = request.POST['kilometers']
        brand = request.POST['brand']
        low = request.POST['lowest']
        high = request.POST['highest']

        print(kilometers)
        if license:
            cursor.execute(
                'create view filter6 as select * from vehicle where vehicle.status = \'onsale\' and license_plate like \'' + license + '%\''
            )
        else:
            cursor.execute(
                'create view filter6 as select * from vehicle where status = \'onsale\';'
            )

         # filtering according to other conditions
        if int(age) != -1:
            print('here1')
            upper_bound = int(age) + 5
            cursor.execute(
                        'create view filter1 as select * from filter6 where age between\'' + str(age) + '\'and \'' + str(upper_bound) +'\';'
            )

        else:
            cursor.execute(
                        'create view filter1 as '
                        'select * from filter6;'
            )

        if model != 'empty':
            cursor.execute(
                        'create view filter2 as select * from filter1 where model=\'' + model + '\';'
            )
        else:
            cursor.execute(
                        'create view filter2 as '
                        'select * from filter1;'
            )

        if int(kilometers) != -1:
            print('here3')

            if int(kilometers) == 40000:
                cursor.execute(
                            'create view filter3 as '
                            'select * from filter2 where kilometers > 40000;'
                )
            else:
                upper_bound = int(kilometers) * 2
                cursor.execute(
                            'create view filter3 as select * from filter2 where kilometers between ' + str(kilometers) + ' and ' + str(upper_bound) +';'
                )


        else:
            cursor.execute(
                        'create view filter3 as '
                        'select * from filter2;'
            )

        if int(high) == 0:
            cursor.execute(
                        'create view filter4 as select * from filter3 where daily_rent_price > ' + str(low) + ';'
            )
        else:
            cursor.execute(
                        'create view filter4 as select * from filter3 where daily_rent_price between ' + str(low) + ' and ' + str(high) +';'
            )

        if brand != 'empty':
            cursor.execute(
                        'create view filter5 as select * from filter4 where brand=\'' + brand + '\';'
            )
        else:
            cursor.execute(
                        'create view filter5 as select * from filter4;'
            )

        #gathering filtered vehicles
        cursor.execute(
                'select * from vehicle, filter5 where vehicle.license_plate = filter5.license_plate and vehicle.branch_id = ' + str(branch_id) + ';'
        )
        result = cursor.fetchall()
        vehicle_info = []

        for car in result:
            item_detail = [car[0], car[1], car[2], car[3], car[4], car[5], car[6]]
            vehicle_info.append(item_detail)

        cursor.execute('drop view filter1')
        cursor.execute('drop view filter2')
        cursor.execute('drop view filter3')
        cursor.execute('drop view filter4')
        cursor.execute('drop view filter5')
        cursor.execute('drop view filter6')
        models, brands = models_and_brands()

        models, brands = models_and_brands()
        return render(request, 'managerBuyCars.html',
                              {'vehicles': vehicle_info, 'branch_id': branch_id, 'models': models, 'brands': brands})


class StatisticsView(View):
    def get(self, request, manager_id):
        user_id = request.session['logged_in_user']
        branch_id, branch_name, employee_name = get_branch_employee_info(manager_id)


        # for the first statistic on the main page
        # retriveing the name of the employee with the most expensive reservation at each month

        most_expensive_rent_of_month = {}

        # finding the branch id information
        cursor = connection.cursor()
        cursor.execute('select budget from branch where branch_id = ' + str(branch_id) + ';')
        result = cursor.fetchall()
        budget = str(result[0])

        #total cost of salaries
        cursor.execute('select sum(salary) from employee where branch_id = ' + str(branch_id) + ';')
        result = cursor.fetchall()[0]
        sum_salary = result


        #total number of cars in the branch
        cursor.execute('select count(*) as car_count from vehicle where branch_id = ' + str(branch_id) + ';')
        result = cursor.fetchall()[0]
        total_cars = result

        cursor.execute(
            'select B.user_id, (select employee_name from employee where employee.user_id = B.user_id) as name, T.cost, T.start_date from branch_employee B, (select reservation_number, checked_by, max(cost) as cost, start_date  from reservation group by month(start_date)) as T where T.checked_by = B.user_id and (select branch_id from employee where employee.user_id = B.user_id) = ' + str(branch_id) + ';'
        )
        result = cursor.fetchall()
        for res in result:
            month = ''
            if res[3].month == 12:
                month = 'December'
            elif res[3].month == 11:
                month = 'November'
            elif res[3].month == 10:
                month = 'October'
            elif res[3].month == 9:
                month = 'September'
            elif res[3].month == 8:
                month = 'August'
            elif res[3].month == 7:
                month = 'July'
            elif res[3].month == 6:
                month = 'June'
            elif res[3].month == 5:
                month = 'May'
            elif res[3].month == 4:
                month = 'April'
            elif res[3].month == 3:
                month = 'March'
            elif res[3].month == 2:
                month = 'February'
            else:
                month = 'January'
            most_expensive_rent_of_month[month] = [res[1], res[2]]

        # for the second statistic on the main page
        # retrieving the name of the employee with number of approves, rejects of reservations
        cursor.execute(
        'select count(*) as operation_number, status, (select employee_name from employee where employee.user_id = B.user_id) as name from branch_employee B , reservation R where B.user_id = R.checked_by and (select branch_id from employee where employee.user_id = B.user_id)  = ' + str(branch_id) + ' group by status having count(*) > 0;'
        )
        result = cursor.fetchall()

        number_of_denials = {}
        number_of_approvals = {}
        for res in result:
            if res[1] == 'accepted':
                number_of_approvals[res[2]] = [res[0], res[1]]
            elif res[1] == 'canceled':
                number_of_denials[res[2]] = [res[0], res[1]]

        print(branch_id)
        # for the third statistic in the page manager can see the income for each month
        cursor.execute('create view sum_reserved_employee as (select employee_name, sum(cost) as sum_cost, month(start_date) as month from reservation, employee, vehicle where reservation.license_plate = vehicle.license_plate and reservation.checked_by = employee.user_id group by reservation.checked_by, month(start_date));')
        cursor.execute(
            'select month(R.start_date) as month, '
            '(select S.employee_name from sum_reserved_employee S '
            'where S.month = month(R.start_date) and '
            'S.sum_cost=(select max(sum_cost) from sum_reserved_employee T where T.month = '
            'S.month)) as employee, sum(R.cost) as total_income from reservation R ,vehicle V where R.license_plate = V.license_plate '
            'and R.status = \'paid\' and V.branch_id = ' + str(branch_id) + ' group by month(start_date)'
        )
        result = cursor.fetchall()
        for res in result:
            print(res)

        cursor.execute('drop view sum_reserved_employee')
        context = {
            'branch_id': branch_id, 'branch_name': branch_name, 'employee_name': employee_name,
            'expensive_rents': most_expensive_rent_of_month,
            'approve': number_of_approvals,
            'deny': number_of_denials,
            'budget': budget,
            'sum_salary': sum_salary,
            'total_car': total_cars,
            'month_info': result
        }

        return render(request, 'managerDashboard.html', context)


def ajaxFireEmployee(request):
    employee = request.GET.get('employee', None)
    manager = request.GET.get('manager', None)

    cursor = connection.cursor()
    cursor.execute('delete from user where user_id = ' + str(employee) + ';');

    data = {}
    data['fired'] = True
    return JsonResponse(data)