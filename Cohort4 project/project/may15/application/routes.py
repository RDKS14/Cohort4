from application import app
from flask import render_template, g, flash, redirect, url_for, request, session
import pymysql
from application.Form import BasicForm



def connect_db():
    return pymysql.connect(
        user = 'root', password = 'password', database = 'Cohort4',
        autocommit = True, charset = 'utf8mb4',
        cursorclass = pymysql.cursors.DictCursor)



def get_db():
    '''Opens a new database connection per request.'''
    if not hasattr(g, 'db'):
        g.db = connect_db()
    return g.db

@app.teardown_appcontext
def close_db(error):
    '''Closes the database connection at the end of request.'''
    if hasattr(g, 'db'):
        g.db.close()


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    message = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        #cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor = get_db().cursor()
        cursor.execute('SELECT * FROM Customer WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['Customer_id']
            session['Username'] = account['Username']
            # Redirect to home page
            return redirect(url_for('products1'))
        else:
            # Account doesn't exist or username/password incorrect
            msg = 'Incorrect username/password!'
    return render_template('login.html', msg='')


@app.route('/adminlogin', methods=['GET', 'POST'])
def adminlogin():
    # Output message if something goes wrong...
    message = ''
    app.logger.info("in adminlogin")
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        app.logger.info(username,password)
        # Check if account exists using MySQL
        #cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor = get_db().cursor()
        cursor.execute('SELECT * FROM admin WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        app.logger.info(account)
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['Admin_id']
            session['Username'] = account['Username']
            session['Admin'] = True
            # Redirect to home page
            return redirect(url_for('products1'))
        else:
            # Account doesn't exist or username/password incorrect
            message = "incorrect username/password!"
    return render_template('adminlogin.html', msg=message)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for ('products1'))

@app.route('/')
def home_page():
    return render_template('home.html', title='Skys The Limit Store')

@app.route('/registercust',  methods = ['GET','POST'])
def registercust():
    """ Second form.
    """
    message = ""
    form = BasicForm() # create form instance
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        Email_Address = form.Email_Address.data
        Username = form.Username.data
        Password = form.Password.data
        app.logger.info(f" {first_name} {last_name} {Email_Address} {Username} {Password} being added.")
        try:
            cursor = get_db().cursor()
            sql = "INSERT INTO `customer` (first_name, last_name, Email_Address, Username, Password) " \
                  "VALUES (%s, %s, %s, %s, %s)"
            app.logger.info(sql)
            cursor.execute(sql, (first_name.upper(), last_name.upper(), Email_Address, Username.upper(), Password ))
            message = "Registration successful please log in"
            app.logger.info(message)
            flash(message)
            return redirect(url_for('products1'))
        except Exception as e:
            message = f"error in insert operation: {e}"
            flash(message)
    return render_template('form1.html', message=message, form=form)

@app.route('/products', methods=['GET', 'POST'])
def products1():
    """ Display Products Page    """
    cursor = get_db().cursor()
    cursor.execute("SELECT Product_id, image, Product_name, Gender, Price from products order by Product_id asc")
    result = cursor.fetchall()
    app.logger.info(result)
    return render_template(
                'products.html',
                title="Products Page",
                description="Check out our great products",
                records=result
    )

@app.route('/products/<int:id>')
def product_display(id):
    app.logger.info(id)
    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM products WHERE Product_id=%s ", id)
    result = cursor.fetchone()
    app.logger.info(result)
    return render_template(
                'item.html',
                title="Third database query - using products template, passing parameter to query",
                description=f"Another db query with parameter from url: Product_id={id}.",
                record=result
    )

@app.route('/product/delete/<int:id>')
def customer_delete(id):
    """ Fourth route. Param for deleting from Actor table
    """
    app.logger.info(id)
    cursor = get_db().cursor()
    cursor.execute("DELETE FROM customer WHERE customer_id=%s ",id)
    message=f"Deleted product id {id}"
    app.logger.info(message)
    flash(message)
    return redirect(url_for('home'))

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    """ Admin Inventory Page    """
    cursor = get_db().cursor()
    cursor.execute("SELECT Product_id, Product_name, Gender, Price, Quantity_Small, Quantity_Medium, Quantity_Large, Quantity_Xlarge from products order by Product_id asc")
    result = cursor.fetchall()
    app.logger.info(result)
    return render_template(
                'admin.html',
                title="Admin Page",
                description="Stock Inventory",
                records=result
    )

@app.route('/about')
def about():
    return render_template(
        'about.html',
        title="About Us",
        description="We are a group of 4 brought together from different regions of Sky Home Service",
        names=['Barrie', 'Rob', 'Sean', 'Zee']
    )



