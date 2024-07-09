from flask import Flask, render_template, request, redirect, url_for
import json
import os
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/residents')
def residents():
    with open('data/residents.json') as f:
        residents = json.load(f)
    current_month = datetime.now().strftime('%B %Y')
    return render_template('residents.html', residents=residents, current_month=current_month)

@app.route('/events')
def events():
    return render_template('events.html')

@app.route('/add_resident', methods=['GET', 'POST'])
def add_resident():
    if request.method == 'POST':
        try:
            flat = request.form['flat']
            name = request.form['name']
            new_resident = {
                "flat": flat,
                "occupancy_type": request.form['occupancy_type'],
                "occupant_name": request.form['occupant_name'],
                "occupant_contact": request.form['occupant_contact'],
                "owner": request.form['owner'],
                "owner_contact": request.form['owner_contact'],
                "maintainence": request.form['maintainence'],
                "default_amount": request.form['default_amount'],
                "pending_months": []
            }
            if os.path.exists('data/residents.json'):
                with open('data/residents.json', 'r+') as f:
                    residents = json.load(f)
                    if any(resident['flat'] == flat for resident in residents):
                        return redirect(url_for('home'))  # Redirect to home if flat already exists
                    residents.append(new_resident)
                    f.seek(0)
                    json.dump(residents, f, indent=4)
            else:
                with open('data/residents.json', 'w') as f:
                    json.dump([new_resident], f, indent=4)
            return redirect(url_for('residents'))
        except KeyError as e:
            return f"Missing form key: {e}", 400
    return render_template('add_resident.html')

@app.route('/edit_resident/<int:index>', methods=['GET', 'POST'])
def edit_resident(index):
    if request.method == 'POST':
        with open('data/residents.json', 'r+') as f:
            residents = json.load(f)
            residents[index]['occupant_name'] = request.form['occupant_name']
            residents[index]['occupant_contact'] = request.form['occupant_contact']
            residents[index]['owner'] = request.form['owner']
            residents[index]['owner_contact'] = request.form['owner_contact']
            residents[index]['maintainence'] = request.form['maintainence']
            residents[index]['default_amount'] = request.form['default_amount']
            f.seek(0)
            json.dump(residents, f, indent=4)
        return redirect(url_for('residents'))
    else:
        with open('data/residents.json') as f:
            residents = json.load(f)
        resident = residents[index]
        return render_template('edit_resident.html', resident=resident, index=index)

@app.route('/default_amount/<int:index>', methods=['GET', 'POST'])
def default_amount(index):
    if request.method == 'POST':
        month = request.form['month']
        year = request.form['year']
        amount = request.form['amount']
        with open('data/residents.json', 'r+') as f:
            residents = json.load(f)
            if 'pending_months' not in residents[index]:
                residents[index]['pending_months'] = []
            residents[index]['pending_months'].append((month, year, amount))
            f.seek(0)
            json.dump(residents, f, indent=4)
        return redirect(url_for('default_amount', index=index))
    else:
        with open('data/residents.json') as f:
            residents = json.load(f)
        resident = residents[index]
        return render_template('default_amount.html', resident=resident, index=index)

if __name__ == '__main__':
    app.run(debug=True)
