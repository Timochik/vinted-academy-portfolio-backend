Vinted Marketplace Backend (FastAPI + PostgreSQL)

A simplified backend inspired by the Vinted marketplace, built using FastAPI, SQLAlchemy, and PostgreSQL.

This project demonstrates the fundamental backend engineering skills relevant for the Vinted Engineering Academy, including:

REST API design

User authentication with JWT

Secure password hashing (bcrypt)

SQLAlchemy ORM modeling

Filtering, searching, and pagination

Protected routes & ownership logic

Dockerized PostgreSQL

Clean project architecture

🚀 Features
🔐 User Authentication

Register new users

Secure password hashing (bcrypt)

Login using OAuth2 password flow

JWT tokens with user ID and expiration

Token-based protected routes

🛍️ Item Management

Create an item (authorized users only)

Get all items

Get a single item by ID

Update item (only by owner)

Delete item (only by owner)

🔎 Advanced Search & Filtering

Filter by:

min_price

max_price

condition

search (text search in title)

Pagination: skip + limit

🗂️ Categories

Create categories

List categories

Items reference categories via FK

📂 Project Structure
vinted_backend_project/
│── main.py            # FastAPI routes & application
│── models.py          # SQLAlchemy ORM models
│── schemas.py         # Pydantic request/response models
│── security.py        # Auth logic, JWT, hashing
│── database.py        # DB engine and session
│── deps.py            # Shared dependencies (get_db)
│── requirements.txt   # Project dependencies
│── README.md          # Documentation

🛢️ Database Setup (PostgreSQL + Docker)

This project uses PostgreSQL 14.

Start PostgreSQL in Docker:
docker run --name vinted-postgres \
  -e POSTGRES_PASSWORD=1234 \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_DB=vinted_marketplace \
  -p 5433:5432 \
  -d postgres:14

Database URL
postgresql://postgres:1234@localhost:5433/vinted_marketplace

▶️ Running the Backend
1. Install dependencies
pip install -r requirements.txt

2. Start the application
uvicorn main:app --reload

3. Open Swagger documentation

👉 http://127.0.0.1:8000/docs

This gives you:

Interactive API testing

"Authorize" button for JWT

Exploration of models & endpoints

🔐 Authentication Flow
1. Register
POST /register

2. Login
POST /token


Response example:

{
  "access_token": "<JWT>",
  "token_type": "bearer"
}

3. Authorize in Swagger

Click Authorize → paste token → now protected routes work.

🛍️ Item Creation Example
POST /items


Request body:

{
  "title": "Vintage Denim Jacket",
  "description": "Classic blue denim jacket, size M.",
  "price": 39.99,
  "condition": "good",
  "category_id": 1,
  "photo_url": "https://example.com/jacket.jpg"
}


Automatically handled:

owner_id assigned from JWT

created_at / updated_at timestamps

is_active=True

📦 Pagination
GET /items/paginated?skip=10&limit=5

🔎 Filtering
GET /items/filter?min_price=20&max_price=100&condition=good&search=denim

🧪 Testing

Manual testing performed via Swagger UI:

✔ Authentication

✔ CRUD operations

✔ Ownership protection

✔ Pagination

✔ Filtering

✔ Categories

🎯 What This Project Demonstrates

This backend showcases the ability to:

Architect a clean FastAPI project

Implement secure authentication with JWT

Build real-world item CRUD features

Work with relational models using SQLAlchemy

Implement search, filtering, and pagination

Use Docker for database management

Handle protected routes and authorization

Build API documentation automatically

Perfect foundation for a backend-focused internship or academy application (e.g., Vinted Engineering Academy).

📝 Future Improvements (Out of scope due to time constraints)

If more time was available:

Image upload support (S3 or local folder)

Item listing status (active, reserved, sold)

User profile endpoints

Admin-level category management

Docker Compose for full stack

Automated testing (pytest)

Rate limiting for login

Async SQLAlchemy

👨‍💻 Author

Tymofii Svyrhun
Backend Developer / Vinted Academy Applicant
Vytautas Magnus University – Informatics Systems
📧 Email: ttimofej983@gmail.com