from flask import Flask, request, redirect, render_template
import cgi
import os


app = Flask(__name__)
app.config['DEBUG'] = True



@app.route("/")
def index():
    return render_template('signup.html')

@app.route("/welcome", methods=['GET'])
def welcome_user():
    username = request.args.get('username')
    return render_template('welcome.html', username=username, title="Welcome")


def is_blank(entry):
    return bool(entry and entry.strip())

def is_space(entry):
    if " " in entry:
        return True
    else:
        return False

def len_ok(entry):
    if 2 < len(entry) < 21:
        return False
    else:
        return True

def spec_char(entry):
    if "@" or "." in entry:
        return False
    else:
        return True

@app.route('/', methods=['POST'])
def entry_check():

    username = request.form['username']
    password = request.form['password']
    verifypass = request.form['verifypass']
    email = request.form['email']

    username_error = ''
    password_error = ''
    verifypass_error = ''
    email_error = ''

    if not is_blank(username):
        username_error = 'Username field was left blank'
        username = ''
    else:
        if is_space(username) or len_ok(username):
            username_error = 'Username not valid! Please make sure there are no spaces and it is between 3-20 characters.'
            username = ''

    if not is_blank(password):
        password_error = 'Password field was left blank'
        password = ''
    else:
       if is_space(password) or len_ok(password):
            password_error = 'Password not valid! Please make sure there are no spaces and it is between 3-20 characters.'
            password = ''

    if not is_blank(verifypass):
        verifypass_error = 'Verify Password field was left blank'
        varifypass = ''
    else:
        if password != verifypass:
            verifypass_error = 'Passwords do not match! Please renter both.'
            verifypass = ''
            password = ''

    if is_blank(email):
        pass
    elif not is_space(email) or not len_ok(email) or not spec_char(email):
        email_error = 'Email format invalid! Please make sure there are no spaces and it is between 3-20 characters.'
        email = ''
    else:
        if not spec_char(email):
            email_error = 'Email format invalid! Please be sure email include a . and @.'
            email= ''

    if not username_error and not password_error and not verifypass_error and not email_error:
        return redirect('/welcome?username={0}'.format(username))
   
    else:
        return render_template('signup.html',
            username_error=username_error,
            password_error=password_error,
            verifypass_error=verifypass_error,
            email_error=email_error,
            email=email,
            password=password,
            username=username)


app.run()