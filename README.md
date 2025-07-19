# Phimart - E-commerce API

Phimart is a RESTful e-commerce API built using Django REST Framework (DRF). It provides endpoints for managing products, categories, orders, and carts. The project also implements JWT authentication using Djoser and includes API documentation with Swagger.

## Features
- Product and category management
- Cart and order functionality
- JWT authentication using Djoser
- API documentation using Swagger (drf_yasg)

## Technologies Used
- **Django** - Backend framework
- **Django REST Framework (DRF)** - API development
- **Djoser** - Authentication
- **Simple JWT** - JWT authentication
- **drf-yasg** - API documentation (Swagger)
- **PostgreSQL** (or SQLite) - Database

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/nazmulh24/Phi_Mart.git
   cd phimart
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser:**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

## API Documentation
Swagger documentation is available at:
```
http://127.0.0.1:8000/swagger/
```

ReDoc documentation is available at:
```
http://127.0.0.1:8000/redoc/
```

## Environment Variables
Create a `.env` file in the root directory and add the following:
```ini
#--> Database Configuration
user=postgres.loiykfdzrtgzmqspmnvt 
password=GrMTCAnhmi8arM6P 
host=aws-0-ap-southeast-1.pooler.supabase.com
port=5432
dbname=postgres

#--> Cloudinary Configuration
cloud_name=dlkq5sjum
api_key=813361344897553
api_secret=wSQnOJSehmaz5gdx9bQY88EhiHo
#
CLOUDINARY_URL=cloudinary://813361344897553:**********@dlkq5sjum

```

## License
This project is licensed under the MIT License.

---
### Author
[Nazmul Hossain](https://github.com/nazmulh24)
