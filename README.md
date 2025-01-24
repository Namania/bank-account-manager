# Bank Account Manager

This project is made with django. It is a bank account manager to track your expenses through a web interface.

![main](./git-image/main.png)

## Installation
1 - Clone this repos
> git clone https://gitlab.com/private75690930/bank-account-manager.git

2 - Make migrations & installation
> cd bank-account-manager\
> pip install -r requirement.txt\
> python manage.py makemigrations app\
> python manage.py migrate

3 - Create a super user
> python manage.py createsuperuser

4 - Run it
> python manage.py runserver 0.0.0.0:8000

5 - Go on your interface
> http://127.0.0.1:8000/admin/

6 - Create a user account to use it as simple user (without staff or superuser rights)

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

Do not create any account where the owner is an administrator except the `Bank` one.\
Do not create transaction from admin panel (if you do, there is no accounts update).\
Else you can edit all Accounts

### User

<span style="color: green">// `Bank` account only usable on credit or debit transaction</span>

Transaction color code:
- `Betweens accounts: 🟦`
- `Credit: 🟥`
- `Debit: 🟩`

You can make transactions betweens accounts:

![internal-transaction](./git-image/internal-transaction.png)

Or simulate an external transaction (such as an in-store purchase) by credit or debit (automatically select `Bank` account):

![external-transaction](./git-image/external-transaction.png)
![transaction-bank](./git-image/transaction-bank.png)

You can also create categories.

![category-create](./git-image/cat-new.png)
![category](./git-image/cat.png)
![category-edit](./git-image/cat-edit.png)
