# Global Shipping Management System

A comprehensive web-based logistics dashboard built with Flask and MySQL. This application allows users to register, log in, place shipping orders, calculate estimated costs based on delivery distance and transport methods, and track their shipments in real-time.

## Features

- **User Authentication:** Secure user registration, login, and session management.
- **Order Management:** Place new shipments by providing sender/receiver details and delivery addresses.
- **Dynamic Cost Calculation:** Automatically calculate shipping costs based on distance (km) and selected shipping methods (Sea, Road, Air, Rail).
- **Shipment Tracking:** Generate unique Tracking IDs (e.g., TRK-12345) and track current shipment status and total cost.
- **Interactive UI:** Responsive dashboard built using Bootstrap 5 and FontAwesome icons.

## Tech Stack

- **Backend:** Python, Flask
- **Database:** MySQL
- **Frontend:** HTML5, CSS3, JavaScript (Fetch API), Bootstrap 5

## Prerequisites

- Python 3.8+
- MySQL Server

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
   pip install flask mysql-connector-python
   ```

4. **Database Setup:**
   - Open your MySQL command-line tool or MySQL Workbench.
   - Run the SQL script provided in `database_setup.sql` to create the database (`shipping_db`) and necessary tables, including the initial shipping rates.
   - **Important:** Ensure you update the database connection credentials in `app.py` (line 17) to match your local MySQL configuration:
     ```python
     password='your_mysql_password'
     ```

5. **Run the Application:**
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
- **Configuration:** Migrate database configurations and secret keys to environment variables (`.env`).
- **Database Optimization:** Utilize a database connection pool or an ORM like SQLAlchemy for better performance.
- **Code Structuring:** Separate routing logic into Flask Blueprints for improved scalability.

## License

This project is open-source and available under the [MIT License](LICENSE).