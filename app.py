from flask import Flask, render_template,request,redirect,url_for,session
from flask_mysqldb import MySQL
from flask_session import Session

app = Flask(__name__)


# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Gautham.JR49'
app.config['MYSQL_DB'] = 'inventory_management'

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
# Initialize MySQL
mysql = MySQL(app)



# Define the home page route
@app.route('/')
def home():
    return render_template('homepage.html')


@app.route('/admin')
def admin():
    return render_template('/admin/dashboard.html')
@app.route('/dashboard2')
def dashboard2():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM products")  # Example query to fetch products
    products = cur.fetchall()
    cur.close()
    return render_template('/admin/dashboard.html', products=products)

# Add more routes as needed




@app.route('/admin/products',methods=['GET','POST'])
def Products():
    if request.method=='POST':   
        productname=request.form['productname']
        quantity=request.form['quantity']
        price=request.form['price']
        description=request.form['description']
    

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO products (name,quantity,price,description,released) VALUES (%s, %s, %s, %s,current_date)", (productname, quantity, price, description))
        mysql.connection.commit()
        cursor.close()
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM products")  # Example query to fetch products
    products= cur.fetchall()
    cur.close()

    return render_template('/admin/Product1t.html',products=products)


@app.route('/admin/orders')
def orders():
    return render_template('/admin/orders.html',orders=orders)


@app.route('/admin/customers')
def customers():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users")  # Example query to fetch products
    customers = cur.fetchall()
    cur.close()
    return render_template('/admin/users1.html', customers=customers)


# Define the about page route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name=request.form['name']
        phone=request.form['phone']
        email = request.form['email']
        password = request.form['password']


        # Insert user data into the database (you can customize this logic)
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO users (name, phone,email, password) VALUES (%s, %s, %s, %s)", (name, phone, email, password))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for('login'))

    return render_template('signup.html')  # Create a signup form template


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['email']
        password = request.form['password']
        session['name']=username

        # Authenticate user (you can customize this logic)
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT role FROM users WHERE email = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        cursor.close()

        if user[0] =='customer':
            # Set session variables (you can use Flask-Session or other session management libraries)
            # Example: session['user_id'] = user['id']
            return redirect(url_for('home'))
        elif user[0] =='admin':
            return redirect(url_for('admin'))
        else:
            return "Invalid credentials. Please try again."

    return render_template('login.html')  # Create a login form template

@app.route('/product')
def product():
    return render_template('product.html')

@app.route('/sales')
def sales():
    return render_template('sales.html')

@app.route('/purchase')
def purchase():
    return render_template('purchase.html')

@app.route('/expence')
def expence():
    return render_template('expence.html')

@app.route('/shipping')
def shipping():
    return render_template('shipping.html')

@app.route('/Return')
def Return():
    return render_template('Return.html')

@app.route('/users')
def users():
    return render_template('users.html')

@app.route('/logout',methods=['GET','POST'])
def logout():
    if request.method == 'POST':
        session.pop("name",None)
        return redirect('/')
    return render_template('logout.html')


if __name__ == '__main__':
    app.run(debug=True)


