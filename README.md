# DataForge 🛠️

A full-stack web application that allows developers and data analysts to define custom data schemas and instantly generate realistic mock data for testing, prototyping, and analysis.

## 🚀 Features

* **Custom Schema Builder:** Dynamically define table structures with over 15 distinct data types (Names, Emails, UUIDs, Dates, Addresses, etc.).
* **Multi-Format Export:** Generate and download up to 10,000 rows of mock data instantly in either **CSV** or **JSON** formats.
* **Secure Authentication:** Token-based user authentication ensures that users can securely save, manage, and update their personal schemas across sessions.
* **Responsive UI:** A clean, dark-themed user interface built entirely with Vanilla JavaScript and Tailwind CSS.

## 💻 Tech Stack

### Backend:

* Python 3
* Django & Django REST Framework (DRF)
* `Faker` library (for generating highly realistic synthetic data)
* SQLite (Development Database)

### Frontend:

* HTML5 / CSS3
* Vanilla JavaScript (ES6+)
* Tailwind CSS (via CDN)

## 🛠️ Local Installation & Setup

If you want to run this project locally, follow these steps:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/YOUR_USERNAME/dataforge.git
   cd dataforge
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python -m venv .venv

   # On Windows:
   .venv\Scripts\activate

   # On macOS/Linux:
   source .venv/bin/activate
   ```

3. **Install the required dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Apply database migrations:**

   ```bash
   python manage.py migrate
   ```

5. **Run the development server:**

   ```bash
   python manage.py runserver
   ```

6. **Open the application:**

   Navigate to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

---

## 🔌 API Endpoints Reference

The backend exposes a RESTful API. Authenticated users (via Token Auth) can interact with the following core endpoints:

* `POST /api/register/` – Register a new user account.
* `POST /api/login/` – Authenticate and receive an access token.
* `GET /api/schemas/` – Retrieve all schemas owned by the authenticated user.
* `POST /api/schemas/` – Create a new data schema.
* `GET /api/schemas/<id>/download/?format=csv|json` – Trigger data generation and file download.
