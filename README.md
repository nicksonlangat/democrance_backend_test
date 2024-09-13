### PROJECT DETAILS
This repo hosts the codebase for democrance backend test which is an API backend for managing customers and customer policies/quotes.

### LOCAL DEV SETUP
You need the following installed on your system.
- [Python](https://www.python.org/downloads/)
- [PostgreSQL](https://www.postgresql.org/download/)

### APPS AND MODULES
The main project settings and configs is found in the `mysite` folder.
The business logic is in the app called `core`
To handles users, authentication and authorization, the app is `accounts`
Shared utilities are found in the `common`
Swagger documentation for all the API endpoints is found via `http://localhost:8000`
To run the tests issue `make test` or `export DJANGO_SETTINGS_MODULE=mysite.settings && pytest -vv`

To set up the codebase on your local machine, follow the steps below:

- Clone [this repo ](https://github.com/nicksonlangat/democrance_backend_test.git) on to your desktop/project folder.
- Create a new database for the project e.g `democrance_db`
- Navigate into the project and create a virtual environment i.e `virtualenv env` then `source env/bin/activate`
- Install project dependencies `pip install -r requirements.txt`
- Create a `.env ` file and add the following secrets to it:
    ```
    SECRET_KEY=YOUR_SECRET_KEY
    DEBUG=on
    DB_NAME=YOUR_DB_NAME
    DB_USER=YOUR_DB_USER
    DB_PASSWORD=YOUR_DB_PASSWORD
    DB_HOST=localhost
    DB_PORT=5432
    ```
- Run database migrations `python manage.py migrate`
- Create a superuser `python manage.py createsuperuser`
- Spin up the dev server `python manage.py runserver` visit the browser at `http://localhost:8000` to interact with the API docs

### COMPLETED API ENDPOINTS AND HOW TO TEST

1. Customer Creation
- To create a customer, send a `POST` request to:
`api/v1/create-customer/`
with the payload in the format below:
    ```js
    {
        "first_name": "Roy",
        "last_name": "Rotich",
        "email": "roy@gmail.com",
        "phone_number": "0713754946",
        "date_of_birth": "1995-06-12",
        "gender": "male"
    }
    ```

2. Policy/Quote Creation
- To create a quote for a customer, send a `POST` request to:
`api/v1/quote/`
with the payload in the format below:
    ```js
    {
        "customer": 3,
        "policy_type": "motor",
        "coverage_amount": "3000000",
        "start_date": "2024-09-13"
    }
    ```
    `policy_type` can be one of `[motor, health, life, home]`

    When a new quote is created, the backend will calculate how much the customer is to pay as premium based on the `coverage_amount` and the `policy_type`
    the assumption is that the policies are valid for a year and thus the response will have:
    ```js
    {
        "id": 15,
        "policy_number": "833B6352F4",
        "customer": {
            "id": 3,
            "user": 3,
            "first_name": "Roy",
            "last_name": "Rotich",
            "email": "roy@gmail.com",
            "phone_number": "0713754946",
            "date_of_birth": "1995-06-12",
            "gender": "male"
        },
        "policy_type": "motor",
        "premium_amount": "180000.00",
        "coverage_amount": "3000000.00",
        "start_date": "2024-09-13",
        "end_date": "2025-09-13",
        "status": "quoted",
        "has_expired": false
    }
    ```
3. Viewing A Policy/Quote
- To view a quote, send a `GET` request to:
`api/v1/quote/<id>/`
 response will be:

 ```js
    {
    "id": 17,
    "policy_number": "8FEA8D92C5",
    "customer": {
        "id": 6,
        "user": 6,
        "first_name": "Roy",
        "last_name": "Rotich",
        "email": "roy@gmail.com",
        "phone_number": "0712754946",
        "date_of_birth": "1990-01-15",
        "gender": "male"
    },
    "policy_type": "home",
    "premium_amount": "162000.00",
    "coverage_amount": "3000000.00",
    "start_date": "2024-09-13",
    "end_date": "2025-09-13",
    "status": "quoted",
    "has_expired": false
    }
 ```

4. Accepting A Policy/Quote
- To accept a quote, send a `PATCH` request to:
`api/v1/quote/<id>/`
with the payload in the format below:
    ```js
    {
        "status": "accepted",

    }
    ```
   The response will show that the Policy status changed from `quoted` to `accepted`

5. Activating A Policy/Quote
- To convert a quote into a live policy, send a `PATCH` request to:
`api/v1/quote/<id>/`
with the payload in the format below:
    ```js
    {
        "status": "active"
    }
    ```
   The assumption is that payment will be invoiced to the customer at a later date.
   The response will show that the Policy status changed from `accepted` to `active`

6. Policy/Quote Status History
- To view status history of a policy, send a `GET` request to:
 `api/v1/policies/<id>/history/`
And the response will look like:

    ```js
    [
    {
        "policy": {
        "id": 15,
        "policy_number": "833B6352F4",
        "policy_type": "motor",
        "premium_amount": "180000.00"
        },
        "status": "active",
        "updated_at": "2024-09-13T11:51:49.633810+03:00"
    },
    {
        "policy": {
        "id": 15,
        "policy_number": "833B6352F4",
        "policy_type": "motor",
        "premium_amount": "180000.00"
        },
        "status": "accepted",
        "updated_at": "2024-09-13T11:49:35.129227+03:00"
    },
    {
        "policy": {
        "id": 15,
        "policy_number": "833B6352F4",
        "policy_type": "motor",
        "premium_amount": "180000.00"
        },
        "status": "quoted",
        "updated_at": "2024-09-13T11:39:53.097199+03:00"
    }
    ]
    ```
7. List All Policies
- To view all policies, send a `GET` request to:
 `api/v1/policies/`
And the response will look like:
    ```js
    [
    {
        "id": 15,
        "policy_number": "833B6352F4",
        "customer": {
        "id": 3,
        "user": 3,
        "first_name": "Roy",
        "last_name": "Rotich",
        "email": "roy@gmail.com",
        "phone_number": "0713754946",
        "date_of_birth": "1995-06-12",
        "gender": "male"
        },
        "policy_type": "motor",
        "premium_amount": "180000.00",
        "coverage_amount": "3000000.00",
        "start_date": "2024-09-13",
        "end_date": "2025-09-13",
        "status": "active",
        "has_expired": false
    }
    ]
    ```

8. List All Policies For A Customer
- To view all policies for a customer, send a `GET` request to:
 `api/v1/policies/?customer_id=id`
And the response will look like:
    ```js
    [
    {
        "id": 15,
        "policy_number": "833B6352F4",
        "customer": {
        "id": 3,
        "user": 3,
        "first_name": "Roy",
        "last_name": "Rotich",
        "email": "roy@gmail.com",
        "phone_number": "0713754946",
        "date_of_birth": "1995-06-12",
        "gender": "male"
        },
        "policy_type": "motor",
        "premium_amount": "180000.00",
        "coverage_amount": "3000000.00",
        "start_date": "2024-09-13",
        "end_date": "2025-09-13",
        "status": "active",
        "has_expired": false
    }
    ]
    ```

9. Filter/Search Policies
- To filter/search polices, send a `GET` request to:
 `api/v1/policies/?policy_status=status` or
  `api/v1/policies/?policy_type=type` or

10. List All Customers
- To view all customers, send a `GET` request to:
 `api/v1/customers/`
And the response will look like:
    ```js
    [
    {
        "id": 3,
        "user": 3,
        "first_name": "Roy",
        "last_name": "Rotich",
        "email": "roy@gmail.com",
        "phone_number": "0713754946",
        "date_of_birth": "1995-06-12",
        "gender": "male"
    }
    ]
    ```

11. Filter/Search  Customers
- To filter/search customers, send a `GET` request with the query_params to:
 `api/v1/customers/?first_name=name` or
 `api/v1/customers/?last_name=name` or
 `api/v1/customers/?date_of_birth=date` or
 `api/v1/customers/?email=email`
And the response will look like:
    ```js
    [
    {
        "id": 3,
        "user": 3,
        "first_name": "Roy",
        "last_name": "Rotich",
        "email": "roy@gmail.com",
        "phone_number": "0713754946",
        "date_of_birth": "1995-06-12",
        "gender": "male"
    }
    ]
    ```

### AUTHENTICATION OF USERS/CUSTOMERS
In the spirit of separation of concerns, a `Customer` and a `User` are two different entities each playing a specific role in the system.
The `User` model is responsible for handling authentication and authorization while the `Customer` model stores and handles business-specific information and roles eg Policy creation and assignment.
At the end of the day, a customer is a user in the system so there exists a `OneToOne` relationship in the `Customer` model. A user can only belong to one customer and vice-versa in the system.
Each time a new customer is created, an associated user is created as well via a `signal`.
