from flask import Flask, request, session, render_template, redirect, url_for, flash
import datetime
import os
from Demo import main as main
import json
import jwt
from functools import wraps


app = Flask(__name__)

app.secret_key = os.urandom(24)
app.config['SECRET_KEY'] = 'thisisthesecretkeyforhousepriceprediction'


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'user' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('login'))
    return wrap


@app.route('/', methods=['GET', 'POST'])
def login():
    """ This is the main Login page. Validates the username and password.
    - Works for any username
    - Password must be 'password'.
    - If Error returns invalid credential
    - On successful move to next page"""

    if request.method == 'POST':
        if request.form['pwd'] == 'password':

            session['user'] = request.form['usr']

            # On success move to useer token page
            return redirect(url_for('usertoken', user=request.form['usr']))

        return render_template('login.html', error="Invalid Credentials")

    if request.method == 'GET':
        # This is the login page.
        return render_template('login.html')


@app.route('/usertoken/<user>', methods=['GET', 'POST'])
@login_required
def usertoken(user):

    """ Generates the user token unique to each individual and auto populates the username and token
    in the corresponding form fields."""

    if request.method == 'GET':
        # Generating token for a given user name and it is valid for only 30 minutes.
        token = jwt.encode({'User': user,
                            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                           app.config['SECRET_KEY'])
        msg = "* User Name and Generated Token are auto populated. Please click submit to continue."

        # Renders  userToken.htm page with auto populated forms.
        return render_template('userToken.html', value=msg, username=user, token=token.decode('UTF-8'))

    # In POST request validate the user token.
    # - Checks for Token Missing, User Name Missing, Invalid User Name, Token is Invalid.
    if request.method == 'POST':

        # Validates if the given user id is same as user if given in login page.
        user_id = request.form['username']
        token = request.form['token']  # Token is taken from html form.

        # User name and token validations.
        if not (user_id and token):
            if not token:
                return render_template('userToken.html', error='Token is Missing!')
            else:
                return render_template('userToken.html', error='User Name is Missing!')
        elif user_id not in session['user']:
            return render_template('userToken.html', error='Invalid User Name!')

        try:
            dt = jwt.decode(token, app.config['SECRET_KEY'])
            # On success go to prediction Page
            return redirect(url_for('prediction'))
        except:
            return render_template('userToken.html', error='Token is Invalid!')


@app.route('/prediction', methods=['GET', 'POST'])
@login_required
def prediction():

    """ This gives the Boston house price prediction for the given predictors. """

    if request.method == 'POST':
        try:
            # Loads the data as json from html form.
            data = json.loads(request.form['featu'])
            # Calling main function which returns the predicted price.
            result = main.main(data)

            # This is validation to see if the run is successful - if not display an error message.
            if not isinstance(result, str):
                res = json.dumps({"Price": result})
                return render_template('Result.html', price=res)
            else:
                return render_template('features.html', error="Error: " + result)
        except:
            err = "Error: Please make sure the sent data is of type json<br> and mentioned " \
                  "features should be of type numeric"
            return render_template('features.html', error=err)

    if request.method == 'GET':
        return render_template('features.html')


@app.route('/logout')
def logout():
    """Log out function which removes the user from session."""
    session.pop('user', None)
    flash("You are logged out!!")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
