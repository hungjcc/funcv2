from flask import Flask, render_template,request,redirect,url_for
import pypyodbc
from credential import username, password, server, database

app = Flask(__name__)

conn_str = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

#Database setup
def init_db():
    conn = pypyodbc.connect(conn_str)
    cursor = conn.cursor()
    # SQL Server does not support "CREATE TABLE IF NOT EXISTS" or SQLite types.
    # Use OBJECT_ID check and SQL Server-compatible types/identity.
    cursor.execute("""
        IF OBJECT_ID('dbo.users', 'U') IS NULL
        BEGIN
            CREATE TABLE dbo.users (
                id INT IDENTITY(1,1) PRIMARY KEY,
                name NVARCHAR(255) NOT NULL,
                age INT NOT NULL
            )
        END
    """)
    conn.commit()
    conn.close()

#Get all users from the database
def get_users():
    conn = pypyodbc.connect(conn_str)
    cursor=conn.cursor()
    cursor.execute('SELECT * FROM dbo.users')
    users = cursor.fetchall()
    conn.close()
    return users

#Add a users to the database
def add_user(name, age):
    conn = pypyodbc.connect(conn_str)
    cursor=conn.cursor()
    cursor.execute('INSERT into dbo.users (name, age) VALUES (?, ?)',(name, age) )
    conn.commit()
    conn.close()

#update a user in the database
def update_user(user_id, name, age):
    conn = pypyodbc.connect(conn_str)
    cursor=conn.cursor()
    cursor.execute('UPDATE dbo.users SET name=?, age=? WHERE id=?', (name, age, user_id))
    conn.commit()
    conn.close()

#delete a user from the database
def delete_user(user_id):
    conn = pypyodbc.connect(conn_str)
    cursor=conn.cursor()
    cursor.execute('DELETE FROM dbo.users WHERE id=?', (user_id,))
    conn.commit()
    conn.close()

@app.route('/')
def index():
    users = get_users()
    return render_template('index.html', users=users)

@app.route('/add_user', methods=['POST'])
def add_user_route():
    name = request.form['name']
    age = request.form['age']
    add_user(name, age)
    return redirect(url_for('index'))

@app.route('/update_user/<int:user_id>', methods=['GET', 'POST'])
def update_user_route(user_id):
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        update_user(user_id, name, age)
        return redirect(url_for('index'))
    # pre-fill form with existing user data
    conn = pypyodbc.connect(conn_str)
    cursor=conn.cursor()
    cursor.execute('SELECT * FROM dbo.users WHERE id=?', (user_id,))    
    user = cursor.fetchone()
    conn.close()
    return render_template('update_user.html', user=user)

@app.route('/delete_user/<int:user_id>', methods=['GET'])
def delete_user_route(user_id):
    delete_user(user_id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True) 
