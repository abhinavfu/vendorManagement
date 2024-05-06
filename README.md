# Welcome to Vendor Management System

This Project is based on `Django` and `Django REST Framework` for vendor
management, integrating aspects of data handling, API development, and basic performance
metric calculations.

Follow the below instructions for quick start and installation of the project.
After successfull installation test the APIs endpoints Using `Postman`, `Insomnia` or other related apps or softwares. The users are authenticated using `Token-based authentication`.


### Objective
Develop a Vendor Management System using Django and Django REST Framework. This
system will handle vendor profiles, track purchase orders, and calculate vendor performance
metrics.

### Technical Requirements

- Django (latest stable version)
- Django REST Framework (latest stable version)
- Comprehensive data validations
- Django ORM for database interactions
- Token-based authentication
- PEP 8 compliant code



## Quick start
### Creating Vendor Management project
- Creating `virtual environment`
    ```bash
    python -m venv /path/to/new/virtual/environment
    ```
    ```bash
    python -m venv c:\path\to\myenv
    ```
    - command to activate virtual environment
    ```bash
    venv\Scripts\activate
    ```

    - install required libraries using command prompt
    ```bash
    pip install -r "requirements.txt"
    ```
    or
    ```bash
    pip install django
    pip install djangorestframework
    pip install djoser
    ```
    
- Another method for creating new `virtual environment` using command prompt (CMD)
    ```bash
    pip install pipenv
    ```
    - After installing pipenv
    ```bash
    pipenv shell
    ```
    ```bash
    pipenv install -r "requirements.txt"
    ```
    or
    ```bash
    pipenv install django
    pipenv install djangorestframework
    pipenv install djoser
    ```


- Create a new project `vendorManagement`
    ```bash
    django-admin startproject vendorManagement
    ```
- After creating project, add `vendorApp` in project sub directory folder
    ```bash
    cd vendorManagement
    django-admin startapp vendorApp
    ```


### Installation
1. Add "app" to your INSTALLED_APPS setting in your project `settings.py` like this::
    ```bash
    INSTALLED_APPS = [
        'rest_framework',
        'rest_framework.authtoken',
        'djoser',
        'vendorApp',
    ]
    ```
2. Include the app URLconf in your project `urls.py` like this::
    ```bash
    urlpatterns = [
        # vendor app
        path('', include('vendorApp.urls')),
        # rest_framework & djoser
        path('api-auth/', include('rest_framework.urls', namespace='rest_framework')), # login/logout
        path('auth/', include('djoser.urls')), # create new user, activation, change password, etc.
        path('auth/', include('djoser.urls.authtoken')),
    ]
    ```
3. Very important for `Token-based authentication`.
    Add these lines of codes in the `setting.py` file to make token based authentication possible.
    ```bash
    REST_FRAMEWORK = {
        'DEFAULT_RENDERER_CLASSES': [
            'rest_framework.renderers.JSONRenderer',
            'rest_framework.renderers.BrowsableAPIRenderer',
        ],
        'DEFAULT_FILTER_BACKENDS': [
            'rest_framework.filters.OrderingFilter',
            'rest_framework.filters.SearchFilter',
        ],
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework.authentication.TokenAuthentication', # important
            'rest_framework.authentication.SessionAuthentication',
        ),
    }
    ```
4. Run ``python manage.py makemigrations`` to make migrations to the INSTALLED_APPS models.
5. Run ``python manage.py migrate`` to create the INSTALLED_APPS models.

6. To create a Super_User or **Admin**, Run `python manage.py createsuperuser`.
    - username
    - email
    - password
    
6. Start the development server ``python manage.py runserver``.


##
## Details on using the API endpoints
These are the useful **`URLs`** to navigate easily in **`web browser`**, **`Postman`** or **`Insomnia`** and can test these API endpoints.


### Users
- Using **`Djoser`** library for registration, change password, etc.
- Users can `create new user` and can `login`.
- Users can only see their informations. Admin can see list of all users.
- For `registration` go to `http://127.0.0.1:8000/auth/users/`.

|URLs|User|
|:----- |:------|
|http://127.0.0.1:8000/auth/users/|GET|
|http://127.0.0.1:8000/api-auth/login/|POST|

### Token Generation
Users can generate token for authentication.
Use `POST` method with `username` and `password` for token generation.

|URLs|User|
|:----- |:------|
| http://127.0.0.1:8000/api-token-auth/ | POST |

- After user get their `token` they can `get access` to API endpoints.
- Without `token` users `can not get acceess` to API endpoints.


### 1. Vendor Profile Management:
|URLs|Admin|User|Vendor|
|:----- |:------|:-------|:-------|
|http://127.0.0.1:8000/api/vendors/|GET, POST|GET, POST|GET, POST|

- Authentication: Token-based authentication required.
- All Users can `get` list of all vendors and can `create` a new vendor by adding following fields such as
    - `name`,
    - `contact_details`,
    - `address`,
    - `vendor_code` should be unique.

|URLs|Admin|User|Vendor|
|:----- |:------|:-------|:-------|
|http://127.0.0.1:8000/api/vendors/{vendor_id}/|GET, DELETE|GET|GET, PUT|

- Authentication: Token-based authentication required.
- Admin can `get` information about single Vendor and can only `delete` single Vendor.
- Users can `get` information about single Vendor.
- Vendors can `get` information about single Vendor
and can only `update` their 
    - `name`, 
    - `contact_details`, 
    - `address`.


### 2. Purchase Order Tracking:

|URLs|Admin|User|Vendor|
|:----- |:------|:-------|:-------|
|http://127.0.0.1:8000/api/purchase_orders/|GET|GET, POST|GET|

- Authentication: Token-based authentication required.
- Admin can `get` list of Purchase Orders.
- Users can `get` list of Purchase Orders and can `create` a new Purchase order by adding following fields such as
    - `po_number` should be unique,
    - `vendor` select vendor using vendor_id, 
    - `items` in JSON format (eg.- {"name":"Item name"} ),
    - `quantity` must be greater than 0.
- Vendor can `get` list of Purchase Orders.


|URLs|Admin|User|Vendor|
|:----- |:------|:-------|:-------|
|http://127.0.0.1:8000/api/purchase_orders/{po_id}/|GET,   DELETE|GET, PUT|GET, PUT|

- Authentication: Token-based authentication required.
- Admin can `get` information about single Purchase Order and only can `delete` single Purchase Order.
- Users can `get` information about single Purchase Order and can `update` field like 
    - `status` to be 'cancelled' to cancel the Purchase Order, before status field is completed or acknowledged by vendor.
    - `quality_rating` after status field is completed.
- Vendors can `get` information about single Purchase Order and can `update` 
    - `status` field as 'placed'.


|URLs|Admin|User|Vendor|
|:----- |:------|:-------|:-------|
|http://127.0.0.1:8000/api/purchase_orders/{po_id}/acknowledge/|||POST|

- Authentication: Token-based authentication required.
- Only same `Vendor` as `Purchase Order's vendor` can acknowledge the Purchase Order.


### 3. Vendor Performance Evaluation:

|URLs|Admin|User|Vendor|
|:----- |:------|:-------|:-------|
|http://127.0.0.1:8000/api/vendors/{vendor_id}/performance|GET|GET|GET|

- Authentication: Token-based authentication required.
- All Users can get information about single vendor performance.


#### (Optional) Another way for testing API endpoints using Python requests
```bash
import requests

url = "http://127.0.0.1:8000/api/vendors/"

payload = { 
        "name": "Vendor Name",
        "contact_details": "Contact Details",
        "address": "Vendor Address",
        "vendor_code": "VENDOR123" 
        }
headers = {
	"content-type": "application/json",
	"Authorization": "token token_value_here"
}

response = requests.post(url, json=payload, headers=headers)

print(response.json())
```




##
## Details on using the Test Suite
In command prompt type below code to run the test cases.
```bash
python manage.py test
```

If test case `pass`, it will show as `.` dot sign

If test case `fail`, it will show as letter `F`

Let's assume two Test Cases
- If both test cases `passes`
    ```bash
    ------------
    ..
    ------------
    Ran 2 test in 0.006s

    OK
    ```
- If both test cases `fails`
    ```bash
    ------------
    FF
    ------------
    Ran 2 tests in 0.009s

    FAILED (failures=2)
    ```
- If one test cases `passes` while another `fails`
    ```bash
    ------------
    .F
    ------------
    Ran 2 tests in 0.007s

    FAILED (failures=1)
    ```

##
### Note
Please, don't forget to install all required packages.

If you are running application from local server, probably, you will have to run server via `python manage.py runserver 0.0.0.0:8000`.
(Optional - Don't forget to add server's IP to ALLOWED_HOSTS in settings.)

##

Thank you for your time and consideration.

Regards

Abhinav Anand

