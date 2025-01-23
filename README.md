# Bank Account Manager

This project is made with django. It is a bank account manager to track your expenses through a web interface.

## Installation
1 - Clone this repos
> git clone https://gitlab.com/private75690930/bank-account-manager.git

2 - Make migrations
> cd bank-account-manager\
> python manage.py makemigrations app\
> python manage.py migrate

3 - Create a super user
> python manage.py createsuperuser

4 - Run it
> python manage.py runserver 0.0.0.0:8000

5 - Go on your interface
> http://127.0.0.1:8000/admin/

6 - Create a user account to use it as simple user (withou staff or superuser rights)

![add-account](./git-image/create-account.png)

7 - Create an account where your admin account is the owner and which is called exactly `Bank`

![bank-account](./git-image/bank-account.png)

8 - Logout

9 - Go to user panel
> http://127.0.0.1:8000/login/

10 - Login with new user account

![login](./git-image/login.png)

## Usage

### Admin

To add categories, you must do it through the admin panel.\
Do not create any account as administrator account except the `Bank` one.

### User

You can make transactions betweens accounts `color: 🟦`

![internal-transaction](./git-image/internal-transaction.png)

or simulate an external transaction (such as an in-store purchase) by credit `color: 🟩` or debit `color: 🟥` with a “Bank” account

![external-transaction](./git-image/external-transaction.png)