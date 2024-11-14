# Django E-commerce Project

A simple e-commerce store blueprint built with Django. Includes basic features like cart persistence, PayPal payment integration, and user authentication.

## Features

- **User Authentication**: Sign-up, login, and password management.
- **Product Listings**: Display products with price, description, and images.
- **Shopping Cart**: Persistent cart with add, update, and remove functions.
- **Checkout & Payment**: Integration with PayPal.
- **Order History**: Users can view past orders. (Not Yet!)

## Technologies

- **Django**: Web framework.
- **SQLite**: Database.
- **JavaScript, HTML/CSS**: Frontend.
- **PayPal REST API**: Payment processing. (https://developer.paypal.com/api/rest/authentication/)

## Setup

1. **Clone the repository**:
   ```bash
   git clone [https://github.com/oubyssf/django-ecom.git]
   cd django-ecom
2. **Create and activate a virtual environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
4. **Make migrations**:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
5. **Create superuser**:
    ```bash
    python manage.py createsuperuser
