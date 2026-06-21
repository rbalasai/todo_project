from flask import Flask, render_template, request, redirect, url_for
import sqlite3


app = Flask(__name__)
DB_Name = "TODO.db"


def init_db():
    """ Create the table todos if it doesn't exits. """
    with sqlite3.connect(DB_Name) as conn:
        cursor = conn.cursor()
        cursor.execute('''
                CREATE TABLE IF NOT EXISTS todos(
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       task TEXT NOT NULL
                )
        ''')
        conn.commit()


init_db()


#------routes------


@app.route('/')
def index():
    """ READ: Fetch all tasks and display them. """
    with sqlite3.connect(DB_Name) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * from todos")
        tasks = cursor.fetchall()
        conn.commit()
    return render_template('index.html', tasks=tasks)


@app.route('/add', methods=['POST'])
def add():
    """Create: Add a new task to DB"""
    task_content = request.form.get('task')
    if task_content:
        with sqlite3.connect(DB_Name) as conn:
            cursor = conn.cursor()
            cursor.execute('Insert into todos (task) values(?)', (task_content,))
            conn.commit()
    return redirect(url_for('index'))


@app.route('/update/<int:id>' , methods=['POST'])
def update(id):
    """UPDATE: Modify an existing task's data."""
    new_content = request.form.get('new-task')
    if new_content:
        with sqlite3.connect(DB_Name) as conn:
            cursor = conn.cursor()
            cursor.execute("Update todos SET task=? where id=?", (new_content, id))
            conn.commit()
    return redirect(url_for('index'))


@app.route('/delete/<int:id>')
def delete(id):
    """DELETE: Deleting an existing task's data."""
    with sqlite3.connect(DB_Name) as conn:
        cursor = conn.cursor()
        cursor.execute("delete from todos where id=?", (id,))
        conn.commit()
    return redirect(url_for('index'))




if __name__ == '__main__':
    app.run(debug=True)