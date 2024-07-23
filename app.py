from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import logging

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configuración de la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)
logging.basicConfig(level=logging.DEBUG)

# Ruta de inicio de sesión
@app.route('/', methods=['GET', 'POST'])
def login():
    msg = ""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            msg = 'Please fill out the form!'
            return render_template('login.html', msg=msg)
        
        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            sql = 'SELECT * FROM usuarios WHERE correo = %s AND clave = %s'
            cursor.execute(sql, (email, password))
            account = cursor.fetchone()
            
            if account:
                session['loggedin'] = True
                session['id'] = account['id']
                session['username'] = account['correo']
                msg = 'Logged in successfully!'
                return render_template('home.html')
            else:
                msg = 'Incorrect email/password!'
        except MySQLdb.Error as e:
            logging.error(f"MySQLdb error: {e}")
            msg = f'Error connecting to the database: {e}'
        except Exception as e:
            logging.error(f"General error: {e}")
            msg = f'Error: {e}'
    
    return render_template('login.html', msg=msg)


# Ruta de registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        
        if not username or not password or not email:
            msg = 'Please fill out the form!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        else:
            try:
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute("INSERT INTO usuarios (nombre, clave, correo) VALUES (%s, %s, %s)", (username, password, email))
                mysql.connection.commit()
                flash('Registration successful', 'success')
                return redirect(url_for('login'))
            except MySQLdb.Error as e:
                logging.error(f"MySQLdb error during registration: {e}")
                msg = f'Error connecting to the database: {e}'
            except Exception as e:
                logging.error(f"General error during registration: {e}")
                msg = f'Error: {e}'
    
    return render_template('index.html', msg=msg)

# Ruta de inicio (home)


    return redirect(url_for('login'))
@app.route('/home')
def home():
    if 'loggedin' in session:
        return render_template('home.html', username=session['nombre'])
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
