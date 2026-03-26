# Global Shipping Management System

A comprehensive web-based logistics dashboard built with Flask and PostgreSQL. This application allows users to register, log in, place shipping orders, calculate estimated costs based on delivery distance and transport methods, and track their shipments in real-time.

## Features

- **User Authentication:** Secure user registration, login, and session management.
- **Order Management:** Place new shipments by providing sender/receiver details and delivery addresses.
- **Dynamic Cost Calculation:** Automatically calculate shipping costs based on distance (km) and selected shipping methods (Sea, Road, Air, Rail).
- **Shipment Tracking:** Generate unique Tracking IDs (e.g., TRK-12345) and track current shipment status and total cost.
- **Interactive UI:** Responsive dashboard built using Bootstrap 5 and FontAwesome icons.

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

2. **Set up a Virtual Environment (Optional but recommended):**
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

5. **Database Setup (PostgreSQL):**
    - Open `psql` (or your PostgreSQL GUI).
    - Run the SQL script in `database_setup.sql` to create `shipping_db` and required tables.
    - The app loads values from your `.env` file automatically.

6. **Run the Application:**
   ```bash
   python app.py
   ```
   The application will be running at `http://127.0.0.1:5000/`.

## Project Structure

```text
├── Blueprint/               # Future modular routing
├── templates/               # HTML templates
│   ├── index.html           # Main dashboard UI
│   ├── login.html           # User login page
│   └── signup.html          # User registration page
├── app.py                   # Main Flask application and server routes
├── database_setup.sql       # Database schema creation and initial reference data
└── README.md                # Project documentation
```

## Potential Improvements (Roadmap)

- **Security:** Implement password hashing (e.g., Werkzeug) for enhanced user security.
- **Configuration:** Keep database configurations and secret keys in environment variables (`.env`).
- **Database Optimization:** Utilize a database connection pool or an ORM like SQLAlchemy for better performance.
- **Code Structuring:** Separate routing logic into Flask Blueprints for improved scalability.

## License

This project is open-source and available under the [MIT License](LICENSE).