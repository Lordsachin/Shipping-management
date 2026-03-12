from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
import mysql.connector
import random

app = Flask(__name__)

# --- REQUIRED FOR LOGIN SESSIONS ---
# This secret key allows the server to "remember" who is logged in.
app.secret_key = 'shipping_secret_key_123' 

# --- DATABASE CONFIGURATION ---
def get_db_connection():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        # 👇 UPDATE THIS LINE WITH YOUR REAL MYSQL PASSWORD 👇
        password='sk.2006', 
        database='shipping_db'
    )
    return conn

# --- ROUTE 1: LOGIN PAGE ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    # If the user clicks "Sign In" button (POST)
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Check if this user exists in the database
        cursor.execute("SELECT * FROM Users WHERE Email = %s AND Password = %s", (email, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            # SUCCESS: Save user info in browser session
            session['user_id'] = user['User_ID']
            session['user_name'] = user['Full_Name']
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

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            # Create the new user in the database
            cursor.execute("INSERT INTO Users (Full_Name, Email, Password) VALUES (%s, %s, %s)", (name, email, password))
            conn.commit()
            conn.close()
            
            flash("Account created! Please login.")
            return redirect(url_for('login'))
        except Exception as e:
            flash("Error: Email already exists!")
            return redirect(url_for('signup'))

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
        cursor = conn.cursor(dictionary=True)
        
        # 1. Calculate Cost based on method
        cursor.execute("SELECT * FROM Shipping_Methods WHERE Method_ID = %s", (method_id,))
        method = cursor.fetchone()
        total_cost = distance * float(method['Cost_per_km'])

        # 2. Save Order Info
        cursor.execute("INSERT INTO Orders (Customer_Name, Address) VALUES (%s, %s)", (name, address))
        order_id = cursor.lastrowid

        # 3. Save Shipment Info
        cursor.execute("INSERT INTO Shipments (Order_ID, Method_ID, Distance_km, Total_Cost) VALUES (%s, %s, %s, %s)", (order_id, method_id, distance, total_cost))
        shipment_id = cursor.lastrowid

        # 4. Generate Tracking ID
        tracking_id = "TRK-" + str(random.randint(10000, 99999))
        cursor.execute("INSERT INTO Tracking (Tracking_ID, Shipment_ID, Current_Status) VALUES (%s, %s, %s)", (tracking_id, shipment_id, 'Order Placed'))

        conn.commit()
        conn.close()

        return jsonify({'status': 'success', 'tracking_id': tracking_id, 'cost': total_cost})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

# --- LOGIC: TRACK ORDER ---
@app.route('/track_shipment', methods=['POST'])
def track_shipment():
    try:
        data = request.get_json()
        tracking_id = data['tracking_id']
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Join tables to get status + cost + customer name
        query = """
            SELECT T.Current_Status, S.Total_Cost, O.Customer_Name 
            FROM Tracking T
            JOIN Shipments S ON T.Shipment_ID = S.Shipment_ID
            JOIN Orders O ON S.Order_ID = O.Order_ID
            WHERE T.Tracking_ID = %s
        """
        cursor.execute(query, (tracking_id,))
        result = cursor.fetchone()
        conn.close()

        if result: 
            return jsonify({'status': 'found', 'data': result})
        else: 
            return jsonify({'status': 'not_found'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True)