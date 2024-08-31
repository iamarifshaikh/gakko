## Overview

This Django project(application) provides a robust system for user management, focusing on roles such as Administrators and Superadmins. The project includes features for secure user registration, login, and role-based access control, with custom decorators ensuring that only authorized users can access specific endpoints.

## Table of Contents

1. [Installation and Setup](#installation-and-setup)
   - [Traditional setup](#Run project with traditional setup)
   - [Docker setup](#Run project with Docker setup)
2. [Environment Variables](#environment-variables)
3. [API Documentation](#api-documentation)
   - [SuperAdmin Registration](#superadminregistration---post-superadminregister)
   - [Approve Administrator](#approveadministrator---post-adminapprove)
   - [Get All Unapproved Administrators](#getallunapprovedadministrator---get-adminunapproved)
   - [Register Administrator](#registeradministrator---post-administratorregister)
   - [Login](#login---post-login)
   - [Test Authentication](#test-authentication---get-testauth)
4. [Custom Decorators](#custom-decorators)
5. [Logging and Debugging](#logging-and-debugging)
6. [Contributing](#contributing)

## Installation and Setup
### Run project with traditional setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/iamarifshaikh/gakko.git
   cd gakko
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   (activate the env)

3. **Set up the environment variables** (see [Environment Variables](#environment-variables)).

5. **Run the server**:
   ```bash
   python manage.py runserver
   ```

### Run project with Docker setup

```
docker-compose up --build

```

Stopping the Docker Containers
To stop the running containers, use:

```
docker-compose down

```

## Environment Variables

Create a `.env` file in the root directory of the project and define the following environment variables:

```env
SECRET_KEY=your_secret_key_here
DEBUG=True  # Set to False in production
DATABASE_URL=your_database_url_here
```

## API Documentation

### SuperAdminRegistration - `POST /superadmin/register` (API only accessible by the system)

**Purpose**: Registers a new Superadmin. This operation is reserved for the system or existing Superadmins.

- **Request Body**:
  ```json
  {
    "name": "John Doe",
    "email": "john@example.com",
    "password": "securepassword"
  }
  ```
- **Response**:
  - **Success (200 OK)**:
    ```json
    {
      "message": "Admin created successfully",
      "payload": {
        "id": "66bc77f24d96747788ad9d9f",
        "name": "John Doe",
        "email": "john@example.com",
        "role": "Admin"
      }
    }
    ```
  - **Failure (401 Unauthorized)**:
    ```json
    {
      "error": "Registration failed for admin"
    }
    ```

### ApproveAdministrator - `POST /admin/approve`

**Purpose**: Approves an unapproved Administrator. Only accessible by Superadmins.

- **Request Headers**:
  - `Authorization:  <JWT_TOKEN>`
- **Request Body**:
  ```json
  {
    "id": "administrator_id"
  }
  ```
- **Response**:
  - **Success (200 OK)**:
    ```json
    {
      "message": "Administrator approved successfully."
    }
    ```
  - **Failure (400 Bad Request)**:
    ```json
    {
      "message": "Administrator is already approved."
    }
    ```

### **Administrator Approval Process (`approve` method)**

The `approve` method is responsible for completing the administrator approval process. When an administrator is approved:

1. **Status Update:**
   - The `is_approved` flag is set to `True`.
   - The `is_rejected` flag is set to `False`.
   - The `approval_date` is recorded with the current date and time.

2. **Unique ID Generation:**
   - A unique identifier (`unique_ID`) is created for the administrator. This ID is a combination of the first four characters of the school name, the first four characters of the school address, and a random four-digit number.

3. **Password Creation:**
   - A random password is generated using a mix of letters, numbers, and symbols.
   - This password is then hashed using `bcrypt` and securely stored in the database.

4. **Save and Notify:**
   - The updated administrator details, including the hashed password and unique ID, are saved to the database.
   - An email is sent to the administrator containing their `unique_ID` and the newly generated password, enabling them to log in.

This process ensures that the administrator's credentials are securely created and communicated, following best practices for password management.

### getALLUnApprovedAdministrator - `GET /admin/unapproved`

**Purpose**: Retrieves all unapproved Administrators. Only accessible by Superadmins.

- **Request Headers**:
  - `Authorization: <JWT_TOKEN>`
- **Response**:
  - **Success (200 OK)**:
    ```json
    {
      "message": "All unapproved administrators.",
      "payload": [
        {
          "id": "66bc77f24d96747788ad9d9f",
          "name": "Jane Doe",
          "email": "jane@example.com",
          "role": "Administrator",
          "is_approved": false
        }
        // More administrators
      ]
    }
    ```

### RegisterAdministrator - `POST /administrator/register`

**Purpose**: Registers a new Administrator. Requires a unique email address.

- **Request Body**:
  ```json
  {
  "school_name":"Government muncipal school",
  "school_address":"C.S.T Mumbai , near station...",
  "contact_number":"1234567890",
  "email_address":"email@gmail.com",
  "school_type":"private/public"
  }

  ```
- **Response**:

  - **Failure (400 Bad Request)**:
    ```json
    {
      "error": "Registration failed",
      "details": {
        "email_address": ["Email address already exists"]
      }
    }
    ```

### Login - `POST /login`

**Purpose**: The `/login` API endpoint authenticates users based on their role (e.g., Administrator or Admin). The API responds with a JWT token upon successful authentication, which is used for subsequent secure communications.

### Request Body

The required fields in the request body vary depending on the role of the user:

```json
{
  "role": "Administrator",
  "unique_ID": "UNIQUE1234",
  "password": "securepassword"
}
```

```json
{
  "role": "Admin",
  "username": "Admin123",
  "email": "admin@example.com",
  "password": "securepassword"
}
```

### Response

- **Success (200 OK)**: If the login is successful, the API responds with a message, a JWT token, and a refresh token.
  ```json
  {
    "message": "Administrator logged in successfully",
    "token": "<JWT_TOKEN>",
    "refresh_token": "<REFRESH_TOKEN>"
  }
  ```

- **Failure (400 Bad Request)**: If the credentials are invalid or required fields are missing, the API responds with an error message.
  ```json
  {
    "error": "Invalid credentials"
  }
  ```

#### **1. Role-Based Validation:**

- **Admin Login:**
  - **Required Fields:** `username`, `email`, and `password`.
  - The `username` and `password` are validated against hardcoded values for the purpose of this demonstration.
  - If the credentials are correct, the corresponding `Superadmin` object is retrieved from the database.
  - If the credentials are invalid or the account is not found, an appropriate error is raised.

- **Administrator Login:**
  - **Required Fields:** `unique_ID` and `password`.
  - The `unique_ID` is used to find the corresponding `Administrator` object in the database.
  - The password is validated using the `check_password` method, which compares the provided password with the stored hashed password.
  - The account must be approved (`is_approved` must be `True`). If the account is not yet approved, an error is raised.

#### **2. Password and Account Validation:**

- For **Administrators**, the password must match the hashed password stored in the database, and the account must be approved before logging in.
- For **Admins**, a static check is performed to validate the username and password. If valid, the user is authenticated.

### Test Authentication - `GET /test/auth`

**Purpose**: Test endpoint to verify authentication and role-based access. Accessible only to authenticated Administrators.

- **Request Headers**:
  - `Authorization: <JWT_TOKEN>`
- **Response**:
  - **Success (200 OK)**:
    ```json
    {
      "message": "You are authenticated",
      "user_id": "admin_id",
      "administrator": {
        "id": "66bc77f24d96747788ad9d9f",
        "name": "Jane Doe",
        "email": "jane@example.com",
        "role": "Administrator"
      }
    }
    ```

## Custom Decorators

- **`is_logged_in`**: Ensures the user is authenticated by checking for a valid JWT token.
- **`is_administrator`**: Restricts access to users with the `Administrator` role.
- **`is_Admin`**: Restricts access to users with the `Admin` (Superadmin) role.

These decorators are applied to views to enforce role-based access control, ensuring that only authorized users can access specific resources.
