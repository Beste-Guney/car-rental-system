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
