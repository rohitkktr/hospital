# Hospital Management System API

A FastAPI-based REST API for managing hospital operations including patients, admissions, beds, units, restraints, and user management.

## Features

- **Patient Management** - Create, read, update, and delete patient records with anonymized IDs
- **Admission Tracking** - Manage patient admissions to beds with timestamps
- **Bed Management** - Track available and occupied beds across units
- **Unit Management** - Organize hospital departments and units
- **Restraint Records** - Document treatment and restraint information
- **User Management** - Manage staff with role-based access control (Admin, Staff, Doctor)
- **Security** - JWT authentication and bcrypt password hashing
- **Database** - MySQL with SQLAlchemy ORM

## Tech Stack

- **Backend Framework:** FastAPI 0.115.0
- **Web Server:** Uvicorn 0.30.1
- **Database ORM:** SQLAlchemy 2.0.36
- **Database Driver:** PyMySQL 1.1.1
- **Authentication:** JWT (python-jose) + bcrypt
- **Validation:** Pydantic 2.5.0
- **Environment:** Python 3.8+

## Prerequisites

- Python 3.8 or higher
- MySQL Server 5.7 or higher
- pip (Python package manager)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/rohitkktr/hospital.git
cd hospital
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory:

```env
# Database Configuration
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=hospital_db

# JWT Configuration
SECRET_KEY=your-secret-key-change-this-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 5. Create Database

```bash
# Login to MySQL
mysql -u root -p

# Create database
CREATE DATABASE hospital_db;
EXIT;
```

### 6. Run the Application

You can run the app in two ways. Recommended: run from the project root so the `app` package is importable.

```bash
# From the project root (recommended)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

If you prefer to run from the `app/` directory, set `PYTHONPATH` so the top-level package is available:

```bash
# From inside the app/ folder (less recommended)
# ensure the project root is on PYTHONPATH
PYTHONPATH=".." uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

## API Documentation

Once the server is running, visit:

- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

## API Endpoints

### Patients
- `POST /patients` - Create patient
- `GET /patients` - List all patients
- `GET /patients/{patient_id}` - Get patient details
- `PUT /patients/{patient_id}` - Update patient
- `DELETE /patients/{patient_id}` - Delete patient

### Admissions
- `POST /admissions` - Create admission
- `GET /admissions` - List all admissions
- `GET /admissions/{admission_id}` - Get admission details
- `PUT /admissions/{admission_id}` - Update admission
- `DELETE /admissions/{admission_id}` - Delete admission

### Beds
- `POST /beds` - Create bed
- `GET /beds` - List all active beds
- `GET /beds/{bed_id}` - Get bed details
- `PUT /beds/{bed_id}` - Update bed
- `DELETE /beds/{bed_id}` - Delete bed

### Units
- `POST /units` - Create unit
- `GET /units` - List all units
- `GET /units/{unit_id}` - Get unit details
- `PUT /units/{unit_id}` - Update unit
- `DELETE /units/{unit_id}` - Delete unit

### Restraints
- `POST /restraints` - Create restraint record
- `GET /restraints` - List all restraints
- `GET /restraints/{restraint_id}` - Get restraint details
- `PUT /restraints/{restraint_id}` - Update restraint
- `DELETE /restraints/{restraint_id}` - Delete restraint

### Users
- `POST /users` - Create user
- `GET /users` - List all users
- `GET /users/{user_id}` - Get user details
- `PUT /users/{user_id}` - Update user
- `DELETE /users/{user_id}` - Delete user

## Project Structure

```
hospital/
├── app/
│   ├── main.py              # FastAPI app initialization
│   ├── crud/                # Database operations
│   │   ├── patient.py
│   │   ├── admission.py
│   │   ├── bed.py
│   │   ├── unit.py
│   │   ├── restraint.py
│   │   └── user.py
│   ├── models/              # SQLAlchemy ORM models
│   │   ├── patients.py
│   │   ├── admissions.py
│   │   ├── beds.py
│   │   ├── units.py
│   │   ├── restraints.py
│   │   ├── users.py
│   │   └── roles.py
│   ├── routers/             # API endpoints
│   │   ├── patients.py
│   │   ├── admissions.py
│   │   ├── beds.py
│   │   ├── units.py
│   │   ├── restraints.py
│   │   └── user.py
│   ├── schemas/             # Pydantic validation models
│   │   ├── patients.py
│   │   ├── admissions.py
│   │   ├── beds.py
│   │   ├── units.py
│   │   ├── restraints.py
│   │   └── users.py
│   └── utils/               # Utilities
│       ├── database.py      # Database configuration
│       └── security.py      # JWT and password hashing
├── migrations/              # Alembic database migrations
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (create locally)
├── .gitignore              # Git ignore rules
└── readme.md               # This file
```

## Environment Setup

### Development

The app is configured with CORS enabled for localhost. Database echo is disabled for optimal performance.

### Production

Before deploying to production:

1. Update `CORS_ORIGINS` in `main.py` to your domain
2. Set `echo=False` in database configuration (already done)
3. Use a strong `SECRET_KEY` for JWT
4. Set `allow_origins` to specific domains only
5. Use environment-specific configurations

## Testing

Run the included test suite:

```bash
cd app
pytest tests/
```

## Common Issues

### MySQL Connection Error
- Ensure MySQL is running: `sudo service mysql start`
- Check database credentials in `.env` file
- Verify database exists: `mysql -u root -p -e "SHOW DATABASES;"`

### Port Already in Use
```bash
# Change the port when running:
uvicorn main:app --reload --port 8001
```

### Virtual Environment Not Activating
```bash
# Recreate virtual environment
rm -rf venv
python -m venv venv
source venv/bin/activate  # On Linux/Mac
```

## Database Schema

The application automatically creates the following tables on startup:

- `patient` - Patient information
- `admission` - Hospital admissions
- `bed` - Hospital beds
- `unit` - Hospital units/departments
- `restraint` - Treatment records
- `user` - Staff members

## Security

- Passwords are hashed using bcrypt
- JWT tokens for API authentication
- CORS restricted to authorized origins
- SQL injection prevention via SQLAlchemy ORM

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see LICENSE file for details.

## Author

**Rohit Kumar** - [GitHub](https://github.com/rohitkktr)

## Support

For issues and questions, please open an issue on GitHub.

## Changelog

### Version 1.0.0 (Current)
- Initial release
- Complete CRUD operations for all entities
- JWT authentication setup
- MySQL database integration
- API documentation with Swagger UI
