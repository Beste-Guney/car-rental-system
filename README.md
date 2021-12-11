# car-rental-system

This is the CS353 Database Systems course term project repository.

## Setup

examplesetting.txt --> settings.py<br />

### Create secret key

`python manage.py shell -c 'from django.core.management import utils; print(utils.get_random_secret_key())'
`<br />
Paste this to YOUR_SECRET_KEY<br />

### Create Admin Account

`python manage.py createsuperuser` <br />

### How to run

` python manage.py migrate` to create tables <br />
` python manage.py runserver` to run server

#### After creating tables

After running first time you should add forign key to employee table <br />
`alter table employee add branch_id int;` <br />
`alter table employee add foreign key (branch_id) references branch(branch_id);`