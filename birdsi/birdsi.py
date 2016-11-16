from flask import Flask, session, redirect, request, url_for, \
	render_template, g
import auth
from APIinterface import getQuery


app = Flask(__name__)
UserManager = auth.UserManager()

### App Config ###
app.config.update(dict(
	DATABASE="birdsi.db",
	DEBUG=True,
	SECRET_KEY='development key',
	USERNAME='admin',
	PASSWORD='default'
))

### Routing ###
@app.route('/')
def index():
	if session.get('id'):
		return redirect(url_for('dashboard'))

	return render_template('index.html')

@app.route('/dashboard', methods = ['GET', 'POST'])
def dashboard():
	if session.get('id'):
		return render_template('dashboard.html')

	return redirect(url_for('login'))

@app.route('/login', methods = ['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		# User has submitted the login form
		email = request.form['email']
		password = request.form['password']
		user = UserManager.login(email, password)
		if user:
			# first element in tuple is id
			session['id'] = user[0]
			return redirect(url_for('dashboard'))
		# Authentication Failed
		error = "Invalid email or password"
		return render_template('login.html', error = error)

	# User is visiting the login page, and has not submitted
	return render_template('login.html', error = error)

@app.route('/register', methods = ['GET', 'POST'])
def register():
	error = None;
	if request.method == 'POST':
		# User has submitted the registration form
		username = request.form['username']
		email = request.form['email']
		email_repeat = request.form['email_repeat']
		password = request.form['password']
		password_repeat = request.form['password_repeat']

		user = UserManager.register(username, email, email_repeat, password,
			password_repeat)
		if user:
			session['id'] = user[0]
			return redirect(url_for('index'))

		# Registration Failed
		error = "Registration failed, please try again"
		return render_template('register.html', error = error)

	# User is visiting the registration page, and has not submitted
	return render_template('register.html', error = error)


@app.route('/logout')
def logout():
	session.pop('id', None)
	return redirect(url_for('index'))

@app.route('/postmethod', methods = ['POST'])
def get_post_javascript_data():
	jsdata = request.form['javascript_data']
	jsdata = getQuery(jsdata)
	return jsdata

if __name__ == '__main__':
	app.run()
