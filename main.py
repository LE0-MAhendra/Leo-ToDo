from flask import Flask, render_template, request, redirect, flash, url_for, session
from sqlalchemy import create_engine, text
from datetime import datetime
now = datetime.now()
app = Flask(__name__, static_url_path="/static")
app.secret_key = '123'
engine = create_engine('sqlite:///TODO.db')
connection = engine.connect()
create_table_query = text(
    "CREATE TABLE IF NOT EXISTS userdata(id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, email TEXT, password TEXT)"
)
connection.execute(create_table_query)
mylist = ["hello kaka "]


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/main', methods=['GET', 'POST'])
def main():
    result = connection.execute(text("SELECT * FROM userTodos"))
    return render_template('main.html', items=result, name=session['user'])


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['name']
        password = request.form['password']
        user_query = text("SELECT * FROM userdata WHERE username = :username")
        result = connection.execute(
            user_query, {'username': username}).fetchone()

        if result:
            stored_password = result[3]
            if password == stored_password:
                session['user'] = username
                session['logged_in'] = True
                create_table_todoquery = text(
                    "CREATE TABLE IF NOT EXISTS userTodos(id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, time TEXT, description TEXT, status BOOLEAN)"
                )
                connection.execute(create_table_todoquery)
                return redirect(url_for('main'))
            else:
                flash("wrong Password")
        else:
            flash("wrong username")

    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['name']
        email = request.form['email']
        password = request.form['password']
        existing_usernames = connection.execute(
            text("SELECT username FROM userdata")).fetchall()
        existing_emails = connection.execute(
            text("SELECT email FROM userdata")).fetchall()
        if (username,) in existing_usernames:
            flash("username already exists.")
        elif (email,) in existing_emails:
            flash(
                "email already exists.", "success")
        else:
            insert_query = text(
                "INSERT INTO userdata(username, email, password) VALUES (:username, :email, :password)")
            connection.execute(
                insert_query, {'username': username, 'email': email, 'password': password})
            connection.commit()

        return redirect(url_for('login'))

    return render_template('signup.html')


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == "POST":
        title = request.form['title']
        time = now.strftime("%d/%m/%Y %H:%M:%S")
        description = request.form['description']
        status = True

        insert_query = text(
            "INSERT INTO userTodos (title, time, description, status) VALUES (:title, :time, :description, :status)")
        connection.execute(
            insert_query, {'title': title, 'time': time, 'description': description, 'status': status})
        connection.commit()

        return redirect(url_for('main'))

    return render_template('main.html')


@app.route('/update/<id>')
def update(id):
    select_query = text("SELECT status FROM userTodos WHERE id = :id")
    result = connection.execute(select_query, {'id': id}).fetchone()

    if result is None:
        return redirect(url_for('main'))

    current_status = result[0]
    new_status = not current_status

    update_query = text("UPDATE userTodos SET status = :status WHERE id = :id")
    values = {'status': new_status, 'id': id}
    connection.execute(update_query, values)
    connection.commit()

    return redirect(url_for('main'))


@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    connection.execute(text("DELETE FROM userTodos WHERE id = {0}".format(id)))
    connection.commit()
    return redirect(url_for('main'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
