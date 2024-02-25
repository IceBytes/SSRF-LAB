from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'jhdje73hdjdgr84unrjNovaTeam987djeh'  

admin_credentials = {
    'username': 'IcePlatform',
    'password': 'jhdruruhr83Novateam987'
}

users = ['user1', 'user2', 'user3']

def is_local_request():
    referer = request.headers.get('Referer')
    return referer and 'localhost' in referer

def login_required(route_function):
    def wrapper(*args, **kwargs):
        if is_local_request():
            return route_function(*args, **kwargs)
        else:
            if 'username' not in session:
                flash('Please login first', 'danger')
                return redirect(url_for('login'))
            return route_function(*args, **kwargs)
    
    wrapper.__name__ = route_function.__name__  
    return wrapper

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if is_local_request():
    	return redirect(url_for('admin_dashboard'))
    	
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == admin_credentials['username'] and password == admin_credentials['password']:
            session['username'] = username
            flash('Login successful', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid username or password', 'danger')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Logout successful', 'success')
    return redirect(url_for('index'))

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    return render_template('admin_dashboard.html', users=users, flag=session.pop('flag', None))

@app.route('/admin/delete_user/<username>', methods=['GET', 'POST'])
@login_required
def delete_user(username):
    if request.method == 'POST':
        if username in users:
            users.remove(username)
            session['flag'] = 'CTF(Ice_Platform_CTF)'
            return redirect(url_for('admin_dashboard'))
        else:
            flash('User not found', 'danger')

    return render_template('delete_user.html', username=username)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
