from flask import Flask, render_template, request, redirect, url_for, flash, session, Response
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import json
import csv
from datetime import datetime  # Correct import

app = Flask(__name__)
app.secret_key = 'your_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Define user loader
class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == 'jfrowsadmin' and password == 'jfrowsadmin':  # Replace with your actual admin password
            user = User(id=1)  # Assigning an ID to the user
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials')
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def home():
    return render_template('home.html', name=current_user.id)

@app.route('/residents')
@login_required
def residents():
    with open('data/residents.json', 'r') as f:
        residents = json.load(f)
    
    # Get current month and year
    current_month = datetime.now().strftime('%B %Y')
    return render_template('residents.html', residents=residents, current_month=current_month)

@app.route('/add_resident', methods=['GET', 'POST'])
@login_required
def add_resident():
    if request.method == 'POST':
        new_resident = {
            'flat': request.form['flat'],
            'occupancy_type': request.form['occupancy_type'],
            'occupant_name': request.form['occupant_name'],
            'occupant_contact': request.form['occupant_contact'],
            'owner': request.form['owner'],
            'owner_contact': request.form['owner_contact'],
            'maintenance': request.form['maintenance'],
            'defaulted_amount': request.form['defaulted_amount']
        }
        with open('data/residents.json', 'r') as f:
            residents = json.load(f)
        residents.append(new_resident)
        with open('data/residents.json', 'w') as f:
            json.dump(residents, f, indent=4)
        return redirect(url_for('residents'))
    
    return render_template('add_resident.html')

@app.route('/edit_resident/<int:index>', methods=['GET', 'POST'])
@login_required
def edit_resident(index):
    with open('data/residents.json', 'r') as f:
        residents = json.load(f)

    if request.method == 'POST':
        residents[index]['flat'] = request.form['flat']
        residents[index]['occupancy_type'] = request.form['occupancy_type']
        residents[index]['occupant_name'] = request.form['occupant_name']
        residents[index]['occupant_contact'] = request.form['occupant_contact']
        residents[index]['owner'] = request.form['owner']
        residents[index]['owner_contact'] = request.form['owner_contact']
        residents[index]['maintenance'] = request.form['maintenance']
        residents[index]['defaulted_amount'] = request.form['defaulted_amount']

        with open('data/residents.json', 'w') as f:
            json.dump(residents, f, indent=4)
        
        return redirect(url_for('residents'))

    return render_template('edit_resident.html', resident=residents[index], index=index)



if __name__ == '__main__':
    app.run(debug=True)

