from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Sample data for parking lots and users (you can replace this with a database)
parking_lots = [
    {
        'id': 1,
        'name': 'Parking Lot 1',
        'location': '123 Main St',
        'capacity': 100,
        'price_per_hour': 5.0,
    },
    {
        'id': 2,
        'name': 'Parking Lot 2',
        'location': '456 Elm St',
        'capacity': 50,
        'price_per_hour': 7.0,
    },
]

users = [
    {'id': 1, 'username': 'admin', 'role': 'admin'},
    {'id': 2, 'username': 'user1', 'role': 'staff'},
    {'id': 3, 'username': 'user2', 'role': 'customer'},
]

@app.route('/')
def index():
    return render_template('index.html', parking_lots=parking_lots, users=users)

@app.route('/add_parking_lot', methods=['GET', 'POST'])
def add_parking_lot():
    if request.method == 'POST':
        # Handle form submission to add a parking lot
        new_lot = {
            'id': len(parking_lots) + 1,
            'name': request.form['name'],
            'location': request.form['location'],
            'capacity': int(request.form['capacity']),
            'price_per_hour': float(request.form['price_per_hour']),
        }
        parking_lots.append(new_lot)
        return redirect(url_for('index'))
    return render_template('add_parking_lot.html')

@app.route('/edit_parking_lot/<int:lot_id>', methods=['GET', 'POST'])
def edit_parking_lot(lot_id):
    lot = next((lot for lot in parking_lots if lot['id'] == lot_id), None)
    if lot is None:
        return 'Parking Lot not found', 404

    if request.method == 'POST':
        # Handle form submission to edit a parking lot
        lot['name'] = request.form['name']
        lot['location'] = request.form['location']
        lot['capacity'] = int(request.form['capacity'])
        lot['price_per_hour'] = float(request.form['price_per_hour'])
        return redirect(url_for('index'))

    return render_template('edit_parking_lot.html', lot=lot)

@app.route('/delete_parking_lot/<int:lot_id>')
def delete_parking_lot(lot_id):
    lot = next((lot for lot in parking_lots if lot['id'] == lot_id), None)
    if lot is None:
        return 'Parking Lot not found', 404

    parking_lots.remove(lot)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
