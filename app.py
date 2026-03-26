from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import random

load_dotenv()

app = Flask(__name__)

# --- REQUIRED FOR LOGIN SESSIONS ---
# This secret key allows the server to "remember" who is logged in.
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'shipping_secret_key_123')

# --- DATABASE CONFIGURATION ---
def get_db_connection():
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_name = os.getenv('DB_NAME')

    missing = [
        key for key, value in {
            'DB_HOST': db_host,
            'DB_PORT': db_port,
            'DB_USER': db_user,
            'DB_PASSWORD': db_password,
            'DB_NAME': db_name,
        }.items() if not value
    ]

    if missing:
        raise RuntimeError(f"Missing required environment variables: {', '.join(missing)}")

    return psycopg2.connect(
        host=db_host,
        port=int(db_port),
        user=db_user,
        password=db_password,
        dbname=db_name,
        sslmode=os.getenv('DB_SSLMODE', 'prefer'),
        connect_timeout=int(os.getenv('DB_CONNECT_TIMEOUT', '10'))
    )

# --- ROUTE 1: LOGIN PAGE ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    # If the user clicks "Sign In" button (POST)
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Check if this user exists in the database
        cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            # SUCCESS: Save user info in browser session
            session['user_id'] = user['user_id']
            session['user_name'] = user['full_name']
            return redirect(url_for('dashboard'))
        else:
            # FAILURE: Show error message
            flash("Invalid Email or Password!")
            return redirect(url_for('login'))

    # If the user just opens the page (GET)
    return render_template('login.html')

# --- ROUTE 2: SIGNUP PAGE ---
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['fullname']
        email = request.form['email']
        password = request.form['password']
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            # Create the new user in the database
            cursor.execute("INSERT INTO users (full_name, email, password) VALUES (%s, %s, %s)", (name, email, password))
            conn.commit()
            
            flash("Account created! Please login.")
            return redirect(url_for('login'))
        except psycopg2.IntegrityError:
            if conn:
                conn.rollback()
            flash("Error: Email already exists!")
            return redirect(url_for('signup'))
        except psycopg2.Error:
            if conn:
                conn.rollback()
            flash("Database connection error. Please try again.")
            return redirect(url_for('signup'))
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    return render_template('signup.html')

# --- ROUTE 3: LOGOUT ---
@app.route('/logout')
def logout():
    session.clear() # Clear the session (log out)
    return redirect(url_for('login'))

# --- ROUTE 4: DASHBOARD (HOME) ---
@app.route('/')
def dashboard():
    # SECURITY CHECK: If user is NOT logged in, send them to login page
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # If logged in, show the dashboard with their name
    return render_template('index.html', username=session['user_name'])

# --- LOGIC: PLACE ORDER ---
@app.route('/place_order', methods=['POST'])
def place_order():
    # SECURITY CHECK
    if 'user_id' not in session: 
        return jsonify({'status': 'error', 'message': 'Not logged in'})

    try:
        data = request.get_json()
        name = data['name']
        address = data['address']
        distance = float(data['distance'])
        method_id = int(data['method_id'])

        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # 1. Calculate Cost based on method
        cursor.execute("SELECT * FROM shipping_methods WHERE method_id = %s", (method_id,))
        method = cursor.fetchone()
        total_cost = distance * float(method['cost_per_km'])

        # 2. Save Order Info
        cursor.execute(
            "INSERT INTO orders (customer_name, address) VALUES (%s, %s) RETURNING order_id",
            (name, address)
        )
        order_id = cursor.fetchone()['order_id']

        # 3. Save Shipment Info
        cursor.execute(
            "INSERT INTO shipments (order_id, method_id, distance_km, total_cost) VALUES (%s, %s, %s, %s) RETURNING shipment_id",
            (order_id, method_id, distance, total_cost)
        )
        shipment_id = cursor.fetchone()['shipment_id']

        # 4. Generate Tracking ID
        tracking_id = "TRK-" + str(random.randint(10000, 99999))
        cursor.execute(
            "INSERT INTO tracking (tracking_id, shipment_id, current_status) VALUES (%s, %s, %s)",
            (tracking_id, shipment_id, 'Order Placed')
        )

        conn.commit()
        
        # 5. VERIFY the tracking ID was actually inserted before returning it
        cursor.execute("SELECT tracking_id FROM tracking WHERE tracking_id = %s", (tracking_id,))
        verify = cursor.fetchone()
        cursor.close()
        conn.close()

        if verify:
            return jsonify({'status': 'success', 'tracking_id': tracking_id, 'cost': total_cost})
        else:
            # Tracking ID wasn't inserted - network/database issue
            return jsonify({'status': 'error', 'message': 'Tracking ID failed to save. Please try again.'})
    except Exception as e:
        print(f"ERROR in place_order: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'status': 'error', 'message': f'Database error: {str(e)}'})

# --- LOGIC: TRACK ORDER ---
@app.route('/track_shipment', methods=['POST'])
def track_shipment():
    try:
        data = request.get_json()
        tracking_id = data.get('tracking_id', '').strip().upper()  # Normalize input
        
        if not tracking_id:
            return jsonify({'status': 'error', 'message': 'Tracking ID is required'})
        
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Join tables to get status + cost + customer name
        query = """
            SELECT t.current_status, s.total_cost, o.customer_name
            FROM tracking t
            JOIN shipments s ON t.shipment_id = s.shipment_id
            JOIN orders o ON s.order_id = o.order_id
            WHERE UPPER(t.tracking_id) = %s
        """
        cursor.execute(query, (tracking_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        if result: 
            return jsonify({'status': 'found', 'data': result})
        else: 
            return jsonify({'status': 'not_found', 'message': f'No shipment found for tracking ID: {tracking_id}'})
    except Exception as e:
        print(f"ERROR in track_shipment: {str(e)}")
        return jsonify({'status': 'error', 'message': f'Database error: {str(e)}'})

if __name__ == '__main__':
    app.run(debug=True)