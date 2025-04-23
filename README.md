# scanNhelp

## Project Description
scanNhelp is a Django-based web application designed to manage users and products with RFID tag scanning functionality. It allows users to register, manage their products, and scan tags to retrieve detailed information including contact, reward, or medical details based on the tag type.

## Features
- User registration and authentication using email and JWT tokens.
- Custom user model with extended fields like phone numbers and address.
- Product management with detailed information including contact, reward, and medical data.
- Tag scanning API to retrieve product and owner information based on tag ID and type.
- RESTful API endpoints for users and products.
- CORS enabled for all origins to support cross-domain requests.

## Installation

### Prerequisites
- Python 3.8+
- pip (Python package installer)
- virtualenv (recommended)

### Setup Steps
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd scanNhelp
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Apply database migrations:
   ```bash
   python manage.py migrate
   ```

5. Create a superuser (optional, for admin access):
   ```bash
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Usage

### API Endpoints

- **Ping**
  - `GET /a/`
  - Simple endpoint to check if the server is running.

- **User Registration**
  - `POST /signup/`
  - Register a new user with email, name, password, phone, and address.

- **Authentication**
  - `POST /token/`
  - Obtain JWT access and refresh tokens.

- **User Management**
  - `GET /users/` - List all users (requires authentication).
  - `POST /users/` - Create a new user (requires authentication).
  - `GET /users/<id>/` - Retrieve user details.
  - `PUT/PATCH /users/<id>/` - Update user details.
  - `DELETE /users/<id>/` - Delete a user.

- **Product Management**
  - `GET /products/user/?user_id=<user_id>` - Get all products of a user.
  - `GET /products/<id>/` - Get details of a specific product.
  - `POST /products/add/` - Add a new product.
  - `PUT /products/modify/<id>/` - Modify an existing product.
  - `DELETE /products/delete/<id>/` - Delete a product.

- **Tag Scanning**
  - `POST /scan`
  - Scan a tag by providing `tag_id` and `tag_type` to retrieve product and owner information.

## Models Overview

- **User**
  - Custom user model using email as the username.
  - Fields: email, name, phone, alternate number, address, and standard Django user fields.

- **Product**
  - Represents a product linked to a user (owner).
  - Fields include tag_id, tag_type, product_name, description, display flag, contact info, reward details (for tag_type=1), and medical details (for tag_type=2).

## Authentication
- Uses JWT (JSON Web Tokens) for authentication.
- Obtain tokens via `/token/` endpoint.
- Protected endpoints require the JWT access token in the Authorization header.

## Additional Information
- CORS is enabled for all origins.
- Uses SQLite as the default database.
- Static files are served from the `/static/` directory.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
