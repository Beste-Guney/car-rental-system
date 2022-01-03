from django import forms
from django.db import connection


class BranchEmployeeCreationForm(forms.Form):
    username = forms.CharField(label='Enter Username', min_length=4, max_length=150)
    email = forms.EmailField(label='Enter email')
    password = forms.CharField(label='Enter password', widget=forms.PasswordInput,min_length=6)
    salary = forms.FloatField(label='Salary')
    phone_number = forms.CharField(label='phone_number', max_length=100)
    address = forms.CharField(label='adress', max_length=100)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': "form-group form-control mt-3"})


class ChauffeurCreationForm(forms.Form):
    CAR_TYPE = (('sedan', 'sedan'), ('suv', 'suv'), ('limo', 'limo'))

    username = forms.CharField(label='Enter Username', min_length=4, max_length=150)
    email = forms.EmailField(label='Enter email')
    password = forms.CharField(label='Enter password', widget=forms.PasswordInput, min_length=6)
    salary = forms.FloatField(label='Salary')
    phone_number = forms.CharField(label='phone_number', max_length=100)
    address = forms.CharField(label='adress', max_length=100)
    years = forms.IntegerField(label='driving_years')
    car_type = forms.ChoiceField(choices=CAR_TYPE)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': "form-group form-control mt-3"})


class DamageExpertCreationForm(forms.Form):
    CAR_TYPE = (('sedan', 'sedan'), ('suv', 'suv'), ('limo', 'limo'))

    username = forms.CharField(label='Enter Username', min_length=4, max_length=150)
    email = forms.EmailField(label='Enter email')
    password = forms.CharField(label='Enter password', widget=forms.PasswordInput, min_length=6)
    salary = forms.FloatField(label='Salary')
    phone_number = forms.CharField(label='phone_number', max_length=100)
    address = forms.CharField(label='adress', max_length=100)
    car_type = forms.ChoiceField(choices=CAR_TYPE)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': "form-group form-control mt-3"})

class AssignCheckForm(forms.Form):
    branchId = forms.IntegerField(widget=forms.HiddenInput())
    print("branch ID : ", branchId.widget.attrs.get('value'))
    sql = "SELECT user_id, employee_name FROM damage_expertise NATURAL JOIN employee"# WHERE employee.branch_id = {}".format(1)
    cursor = connection.cursor()
    cursor.execute(sql)
    dExperts = cursor.fetchall()
    sql = "SELECT license_plate FROM vehicle"# WHERE branch_id = {}".format(1)
    cursor.execute(sql)
    vehicles = cursor.fetchall()
    i = 1
    vehicleChoices = ()
    while i <= len(vehicles):
        vehicleChoices += ((*vehicles[i-1], *vehicles[i-1]),) 
        i = i + 1
    damage_expertise = forms.ChoiceField(label="Pick a damage expertise", choices=dExperts)
    vehicle = forms.ChoiceField(label="Pick a vehicle",choices=vehicleChoices)

    def __init__(self, *args, **kwargs):
        branch_id = kwargs.pop('branch_id')
        super().__init__(*args, **kwargs)
        self.fields['branchId'].widget.attrs.update({'value': branch_id})
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': "form-group form-control mt-3"})