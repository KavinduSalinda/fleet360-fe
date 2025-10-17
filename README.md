# Fleet360 Django REST API

A comprehensive fleet management system built with Django REST Framework, MySQL database, and JWT authentication.

## Features

- **Customer Management**: Complete CRUD operations for customers with document management
- **Vehicle Management**: Vehicle inventory with categories, subcategories, and availability tracking
- **Driver Management**: Driver profiles with availability status
- **User Authentication**: JWT-based authentication system
- **Booking System**: Complete booking lifecycle with returns and extensions
- **Document Management**: File upload and management system

## API Endpoints

### Authentication
- `POST /api/users/login` - User login
- `GET /api/user/1/` - Get user details
- `PUT /api/user/1/` - Update user details
- `POST /api/user/1/change-password/` - Change password

### Customers
- `POST /api/customers/` - Create customer
- `GET /api/customers/` - List customers (with search)
- `GET /api/customers/1/` - Get customer details
- `PUT /api/customers/1/` - Update customer
- `DELETE /api/customers/1/` - Delete customer
- `GET /api/customers/1/status/` - Get customer status
- `PATCH /api/customers/1/status/` - Update customer status

### Vehicles
- `POST /api/vehicle/` - Add vehicle
- `GET /api/vehicles/` - List vehicles (with filters)
- `GET /api/vehicle/1/` - Get vehicle details
- `PUT /api/vehicle/1/` - Update vehicle
- `DELETE /api/vehicle/1/` - Delete vehicle
- `PATCH /api/vehicle/1/status/` - Update vehicle availability
- `GET /api/vehicle/1/status/` - Check vehicle availability

### Drivers
- `POST /api/drivers/` - Create driver
- `GET /api/drivers/` - List drivers (with search)
- `GET /api/driver/1/` - Get driver details
- `PUT /api/driver/1/` - Update driver
- `DELETE /api/driver/1/` - Delete driver
- `GET /api/driver/1/status/` - Check driver availability

### Bookings
- `POST /api/booking/` - Place booking
- `GET /api/bookings/` - List bookings (with filters)
- `GET /api/booking/1/` - Get booking details
- `POST /api/bookings/1/returns` - Return booking
- `POST /api/booking/1/extensions/` - Extend booking
- `GET /api/bookings/locations/` - Get all locations

### Documents
- `POST /api/documents/` - Upload document

## Installation

### Prerequisites
- Python 3.8+
- MySQL 5.7+
- pip

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd fleet361
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup environment variables**
   ```bash
   cp env.example .env
   ```
   
   Edit `.env` file with your configuration:
   ```
   DEBUG=True
   SECRET_KEY=your-secret-key-here-change-in-production
   DATABASE_NAME=fleet360_db
   DATABASE_USER=root
   DATABASE_PASSWORD=your-mysql-password
   DATABASE_HOST=localhost
   DATABASE_PORT=3306
   JWT_SECRET_KEY=your-jwt-secret-key-here
   JWT_ALGORITHM=HS256
   JWT_ACCESS_TOKEN_LIFETIME=604800
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

5. **Setup MySQL database**
   ```sql
   CREATE DATABASE fleet360_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

6. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

8. **Run development server**
   ```bash
   python manage.py runserver
   ```

## Database Schema

### Key Models

- **Customer**: Customer information with documents
- **Vehicle**: Vehicle details with categories and images
- **Driver**: Driver profiles with availability
- **Booking**: Complete booking system with add-ons
- **Location**: Pickup and dropoff locations
- **User**: Authentication and user profiles

## Authentication

The API uses JWT (JSON Web Tokens) for authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

## Testing

You can test the API using the provided Postman collection or any REST client. The API follows RESTful conventions and returns JSON responses.

## Admin Interface

Access the Django admin interface at `http://localhost:8000/admin/` to manage data through the web interface.

## Production Deployment

For production deployment:

1. Set `DEBUG=False` in your environment variables
2. Configure proper database credentials
3. Set up static file serving
4. Use a production WSGI server like Gunicorn
5. Configure reverse proxy with Nginx
6. Set up SSL certificates

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License.
