# E-commerce API with User Authentication and JWT

This Django Rest Framework API provides functionalities for managing products, user authentication, cart management, order creation, product reviews, and more.

## Features

- User authentication using JWT (JSON Web Tokens)
- Custom permissions for different user roles:
  - Only admin users can perform operations related to products
  - Logged-in users can add reviews to products and modify their own reviews
- Custom filters for searching and filtering products
- Cart management:
  - Users can add items to their cart and modify the cart without logging in
  - Users must log in to create an order from their cart and the items related to it
- Payment methods (to be added in future updates)

## Some Endpoints

- /api/products/: List and create products (admin only)
- /api/products/<id>/: Retrieve, update, or delete a specific product (admin only)
- /api/products/<id>/reviews/: List and create reviews for a product (logged-in users only)
- /api/cart/: View and modify the user's cart
- /api/orders/: Create an order from the user's cart (logged-in users only)
- /api/auth/login/: Obtain a JWT token by providing valid credentials
- /api/auth/refresh/: Refresh the JWT token
- /api/auth/logout/: Logout and invalidate the JWT token

    All other endpoints can be seen on the main url

![image](https://github.com/SiandjaRemy/drf-ecommerce-api/assets/122384822/388a5ab6-d840-4c65-87fd-7cbf83031fca)


## Setup

1. Clone the repository:

- git clone https://github.com/SiandjaRemy/drf-ecommerce-api.git
- cd drf-ecommerce-api

2. Create a virtual environment and install dependencies:

- virtualenv env
- env\scripts\activate
- pip install -r requirements.txt

3. Set up the database:

- python manage.py migrate
- python manage.py createsuperuser

4. Run the development server:

- python manage.py runserver
   
## Usage
1. Access the API endpoints using tools like Postman or cURL.
2. Register a new user or log in with an existing user to access restricted endpoints.
3. Add products to the cart, create orders, add reviews to products, and perform other actions based on your user role.

## Contributors
- [Siandja Remy](https://github.com/SiandjaRemy)

Feel free to contribute by submitting bug reports, feature requests, or pull requests.


<!-- ###### ###### ###### ###### ###### ###### ###### ###### ######  Note  ##### ###### ###### ###### ###### ###### ###### ###### ###### -->

## Environment Variables
This project uses environment variables to store sensitive information such as secret keys and API keys. To set up your own environment variables, follow these steps:

1. Create a .env file in the root directory of the project.
2. Add the following key-value pairs to the .env file:

- SECRET_KEY=your_secret_key_here
   
3. Make sure to replace your_secret_key_here with your actual secret key value.
4. Add the .env file to your .gitignore file to prevent it from being committed to version control.

By setting up your own .env file with the required environment variables, you can securely store sensitive information without exposing it in your codebase. Remember not to share your .env file or its contents publicly to maintain the security of your application.
