from django import forms


class BranchEmployeeCreationForm(forms.Form):
    username = forms.CharField(label='Enter Username', min_length=4, max_length=150)
    email = forms.EmailField(label='Enter email')
    password = forms.CharField(label='Enter password', widget=forms.PasswordInput)
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
    password = forms.CharField(label='Enter password', widget=forms.PasswordInput)
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
    password = forms.CharField(label='Enter password', widget=forms.PasswordInput)
    salary = forms.FloatField(label='Salary')
    phone_number = forms.CharField(label='phone_number', max_length=100)
    address = forms.CharField(label='adress', max_length=100)
    car_type = forms.ChoiceField(choices=CAR_TYPE)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': "form-group form-control mt-3"})