# Global Shipping Management System

This is a Flask + PostgreSQL web app for basic shipping management. It lets users sign up, log in, place shipment orders, estimate delivery cost by method and distance, and track shipments.

## Features

- **User Authentication:** Registration, login, logout, and session handling.
- **Order Management:** Create shipment orders with customer and address details.
- **Cost Calculation:** Cost is calculated from distance and selected shipping method.
- **Shipment Tracking:** Generates tracking IDs (for example, TRK-12345) and shows shipment status.
- **UI:** Bootstrap-based interface for order placement and tracking.

## Tech Stack

- **Backend:** Python, Flask
- **Database:** PostgreSQL
- **Frontend:** HTML5, CSS3, JavaScript (Fetch API), Bootstrap 5

## Prerequisites

- Python 3.8+
- PostgreSQL Server

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/shipping-management.git
   cd shipping-management
   ```

2. **Set up a virtual environment (optional):**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` file in the project root:**
   ```env
   FLASK_SECRET_KEY=replace_with_a_strong_secret
   DB_HOST=localhost
   DB_PORT=5432
   DB_USER=postgres
   DB_PASSWORD=your_postgres_password
   DB_NAME=shipping_db
   DB_SSLMODE=prefer
   DB_CONNECT_TIMEOUT=10
   ```

5. **Database setup (PostgreSQL):**
   - Open `psql` (or any PostgreSQL client).
   - Run `database_setup.sql`.
   - The app reads DB settings from `.env`.

6. **Run the Application:**
   ```bash
   python app.py
   ```
   The application will be running at `http://127.0.0.1:5000/`.

## Project Structure

```text
├── Blueprint/               # Notes for folder layout
├── templates/               # HTML templates
│   ├── index.html           # Dashboard page
│   ├── login.html           # User login page
│   └── signup.html          # User registration page
├── app.py                   # Flask routes and backend logic
├── database_setup.sql       # Schema and seed data
└── README.md                # Project documentation
```

## Potential Improvements (Roadmap)

- **Security:** Store passwords as hashes.
- **Configuration:** Keep secrets and DB config in environment variables.
- **Performance:** Add connection pooling or use an ORM like SQLAlchemy.
- **Structure:** Move routes into Flask Blueprints as the app grows.

## License

This project is open-source and available under the [MIT License](LICENSE).