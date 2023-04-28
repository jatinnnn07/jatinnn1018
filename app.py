from flask import Flask, render_template, request, redirect, url_for
import sqlite3

conn = sqlite3.connect('expenses.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS expenses (id INTEGER PRIMARY KEY, description TEXT, amount INTEGER, date TEXT)''')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')



@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        description = request.form['description']
        amount = request.form['amount']
        date = request.form['date']
        conn = sqlite3.connect('expenses.db')
        c = conn.cursor()
        c.execute("INSERT INTO expenses (description, amount, date) VALUES (?, ?, ?)", (description, amount, date))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    else:
        
        return render_template('add.html')


@app.route('/view')
def view():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("SELECT * FROM expenses ORDER BY date")

    data = c.fetchall()
  # Calculate total expenses
    total_expenses = sum([row[2] for row in data])

    conn.close()
    return render_template('view.html', data=data, total_expenses=total_expenses)


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_term = request.form['search_term']
        conn = sqlite3.connect('expenses.db')
        c = conn.cursor()
        c.execute("SELECT * FROM expenses WHERE description LIKE ?", ('%'+search_term+'%',))


        data = c.fetchall()
        conn.close()
        return render_template('search_result.html', data=data, search_term=search_term)
    else:
        return render_template('search.html')


@app.route('/search_result')
def search_result():
    search_term = request.args.get('search_term')
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("SELECT * FROM expenses WHERE description LIKE ?", ('%'+search_term+'%',))
    data = c.fetchall()
    conn.close()
    return render_template('search_result.html', data=data, search_term=search_term)


@app.route('/delete', methods=['POST'])
def delete():
    description = request.form['description']
    search_term = request.form.get('search_term', '')
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("DELETE FROM expenses WHERE description = ?", (description,))
    conn.commit()
    c.execute("SELECT * FROM expenses WHERE description LIKE ?", ('%'+search_term+'%',))
    data = c.fetchall()
    conn.close()
    return redirect(url_for('view', search_term=search_term))



@app.route('/delete_description')
def delete_form():
    return render_template('delete.html')
    


if __name__ == '__main__':
    app.run(debug=True)
