from django.shortcuts import render
from django.views import View
from django.db import connection
from django.views.generic.list import ListView
from django.http import JsonResponse

# Create your views here.
def createModelBrandTable():
    cursor = connection.cursor()
    cursor.execute(
        'create table if not exists modelBrand(model varchar(15),brand varchar(20),primary key(model))engine=InnoDB;')

    return 'Model brand created'

def createVehicleTable():
    cursor = connection.cursor()
    cursor.execute(
        'create table if not exists vehicle(license_plate varchar(8) not null,status varchar(20),daily_rent_price float,model varchar(15),price int,age int,kilometers int,transmission_type varchar(10),buying_manager_id int,branch_id int,check (status in ( \'on_rent\', \'available\', \'on_transfer\', \'unavailable\', \'reserved\')),check (transmission_type in (\'Automatic\', \'Manual\')),PRIMARY KEY (license_plate),FOREIGN KEY (buying_manager_id) REFERENCES manager(user_id),FOREIGN KEY (branch_id) REFERENCES branch(branch_id),FOREIGN KEY (model) REFERENCES modelBrand(model))engine=InnoDB;')

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

        #finding the branch
        cursor.execute(
            'select * from branch where branch_id=\'' + str(branch_id) + '\''
        )
        result = cursor.fetchall()
        result = result[0]
        branch_name = result[2]

        return render(request, 'managerDashboard.html', {'branch_id' : branch_id, 'branch_name':branch_name })


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
        return render(request, 'branchCarsManaager.html', {'vehicles':vehicle_info})

class BuyCarView(View):
    def get(self, request):
        cursor = connection.cursor()
        cursor.execute(
            'select * from vehicle where status=\'unavailable\''
        )
        result = cursor.fetchall()
        vehicle_info = []

        for car in result:
            item_detail = [car[0], car[1], car[2], car[3], car[4], car[5], car[6]]
            vehicle_info.append(item_detail)
        return render(request, 'managerBuyCars.html', {'vehicles': vehicle_info})

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
    result = result[0] #budget of the branch
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
        'update vehicle set status = \'available\'  where license_plate = \'' + str(vehicle_plate) + '\';'    )
    cursor.execute(
        'update vehicle set buying_manager_id = ' + str(manager) + ' where license_plate = \'' + str(vehicle_plate) + '\';'
    )
    cursor.execute(
        'update vehicle set branch_id = ' + str(branch_id) + ' where license_plate = \'' + str(vehicle_plate) + '\';'
    )
    cursor.execute(
        'update branch set budget = budget - ' + str(price) + ' where branch_id = \'' + str(branch_id) + '\';'
    )

    return JsonResponse(data)


