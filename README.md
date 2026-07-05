# Astera

An asynchronous, database-driven Python backend application designed for structured data and task management. This project demonstrates clean coding practices, modern asynchronous database drivers, and structured architectural patterns.

## 🛠️ Tech Stack & Libraries
* **Language:** Python 3.10+
* **Database:** PostgreSQL
* **ORM:** SQLAlchemy 2.0 (Asynchronous ORM)
* **Database Driver:** `asyncpg` (High-performance async driver for PostgreSQL)
* **Architecture:** Repository Pattern

## 🏗️ Architectural Features
* **Asynchronous Execution:** Built from the ground up using `asyncio` and async database operations to handle concurrent processes efficiently without blocking.
* **Repository Pattern:** Implements a clean separation of concerns. Business logic is completely decoupled from the data access layer (database queries), making the codebase highly maintainable and scalable.
* **Session Management:** Utilizes SQLAlchemy's `async_sessionmaker` for reliable and secure database transaction management.

## 📁 Project Structure Brief
* `database/` — Contains database connection configuration, session makers, and engine setups.
* `models/` — SQLAlchemy models defining the PostgreSQL database schema and relationships.
* `repositories/` — The data access layer handling all CRUD operations and database interactions using asynchronous queries.

## 🚀 How to Run Locally

1. **Clone the repository:**
```bash
   git clone [https://github.com/oleg-cpu/Astera.git](https://github.com/oleg-cpu/Astera.git)
   cd Astera

2. **Set up a virtual environment**
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

3. **Install dependencies**
Make sure you have your database drivers and SQLAlchemy installed.

4. Configure your Database connection string in the database config files to point to your local PostgreSQL instance.
