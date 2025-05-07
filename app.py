from flask import Flask, render_template, request, redirect, url_for, flash
from db import reserve_table, add_menu_item, get_menu_items, delete_menu_item, add_order, get_orders

app = Flask(__name__)
app.secret_key = "supersecret"  # Needed for flashing messages

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/reservation', methods=['GET', 'POST'])
def reservation():
    if request.method == 'POST':
        name = request.form['name']
        table = request.form['table']
        time = request.form['time']
        result = reserve_table(name, table, time)
        flash(result)
        return redirect(url_for('reservation'))
    return render_template('reservation.html')

@app.route('/menu', methods=['GET', 'POST'])
def menu():
    if request.method == 'POST':
        item = request.form['item']
        price = request.form['price']
        add_menu_item(item, price)
        flash('Item added!')
        return redirect(url_for('menu'))
    items = get_menu_items()
    return render_template('menu.html', items=items)

@app.route('/delete_item/<int:item_id>')
def delete_item(item_id):
    delete_menu_item(item_id)
    flash("Item deleted.")
    return redirect(url_for('menu'))

@app.route('/order', methods=['GET', 'POST'])
def order():
    if request.method == 'POST':
        table = request.form['table']
        item = request.form['item_id']
        qty = request.form['quantity']
        add_order(table, item, qty)
        flash("Order placed.")
        return redirect(url_for('order'))
    items = get_menu_items()
    return render_template('order.html', items=items)

@app.route('/billing', methods=['GET', 'POST'])
def billing():
    bill = None
    if request.method == 'POST':
        table = request.form['table']
        rows = get_orders(table)
        total = sum(r[3] for r in rows)
        bill = {"rows": rows, "total": total}
    return render_template('billing.html', bill=bill)

if __name__ == '__main__':
    app.run(debug=True)
