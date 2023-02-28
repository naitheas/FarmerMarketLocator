import os
from flask import Blueprint,flash,render_template,url_for,redirect,session,abort
from twilio.rest import Client
from FarmerMarketLocator.models import User
from FarmerMarketLocator.forms import TwilioLoginForm,TwilioVerifyForm
from flask_login import login_user,current_user

verify = Blueprint('verify',__name__)

#twilio API keys/info
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN= os.environ.get('TWILIO_AUTH_TOKEN')
VERIFY_SERVICE_SID= os.environ.get('VERIFY_SERVICE_SID')
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# user account request auth code route
@verify.route('/twilio_login', methods=['GET', 'POST'])
def twilio_login():
    if current_user.is_authenticated:
        return redirect(url_for('main.homepage'))
    form = TwilioLoginForm()
    if form.validate_on_submit():
        # filter query by user email, returns +1phone
        user_phone = User.format_user_phone(form.email.data)
        if user_phone:
            try:
                session['username'] = form.email.data
                send_verification(user_phone)
                return redirect(url_for('verify.generate_verification_code'))
            except:
                abort(405)
        flash('User not found.Please try again','danger')
        return render_template('users/twilio_login.html',form=form)
    return render_template('users/twilio_login.html',form=form)


def send_verification(user_phone):
    client.verify \
        .services(VERIFY_SERVICE_SID) \
        .verifications \
        .create(to=user_phone, channel='sms')

# user account verify sent code route
@verify.route('/verify', methods=['GET', 'POST'])
def generate_verification_code():
    if current_user.is_authenticated:
        return redirect(url_for('main.homepage'))
    form = TwilioVerifyForm()
    email = session['username']
    user = User.query.filter_by(email=email).first_or_404()
    user_phone = User.format_user_phone(email)
    if form.validate_on_submit():
        try:
            verification_code = form.verificationcode.data
            if check_verification_token(user_phone, verification_code):
                login_user(user)
                flash('Login successful, thanks for protecting your account!','success')
                return redirect(url_for('main.homepage'))
            else:
                flash('Invalid or expired verification code. Please try again.','danger')
                return render_template('users/twilio_verify.html',form=form)
        except:
            abort(405)
    return render_template('users/twilio_verify.html',form=form)

def check_verification_token(user_phone, token):
    check = client.verify \
        .services(VERIFY_SERVICE_SID) \
        .verification_checks \
        .create(to=user_phone, code=token)    
    return check.status == 'approved'


