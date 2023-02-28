from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField,PasswordField,SubmitField,TextAreaField,BooleanField,ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo
from FarmerMarketLocator.models import User

# source:https://stackoverflow.com/questions/50762446/formatting-phone-numbers-for-presentation-and-database-entry-using-flask
class PhoneField(StringField):
    def process_formdata(self, valuelist):
        self.data = [v.replace('-', '').replace('(','').replace(')','') for v in valuelist]
        super().process_formdata(self.data)

class RegisterForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(message="Username required."),Length(min=5,max=20)]) 
    email = StringField("Email Address",validators=[DataRequired(message="Please enter an valid email."),Email()])
    phone = PhoneField('phone', validators = [
            DataRequired(message="Please enter a valid phone number.")])
    password = PasswordField('Password', validators=[Length(min=6),
            DataRequired(message="Please enter a password at least 6 characters long.")])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password'),DataRequired(message="Passwords must match.")])
    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken. Please try another.')
    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please login.')

class EditUserForm(FlaskForm):
    username = StringField('Username',validators=[Length(min=5,max=20)])
    email = StringField("Email Address",validators=[DataRequired(message="Please enter an valid email."),Email()])
    phone = PhoneField('Phone Number', validators = [DataRequired(message="Please enter a valid phone number.")])
    image_url = StringField('(Optional) Image URL')
    bio = StringField('(Optional) Bio')
    location = StringField('(Optional) Location')
    submit = SubmitField('Update')
    def validate_username(self,username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username already taken. Please try another.')
    def validate_email(self,email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email already registered. Please login.')
            
class LoginForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(message="Please enter account email."),Email()])
    password = PasswordField('Password', validators=[DataRequired(message="Please enter account password.")])
    remember = BooleanField('Remember Me')

class CommentForm(FlaskForm):
    content = TextAreaField('Enter comment below',validators=[DataRequired(message="Comment may contain up to 150 characters."),Length(max=150)])
    submit = SubmitField('Submit Comment')

class EditCommentForm(FlaskForm):
    content = TextAreaField('Update comment below',validators=[DataRequired(message="Comment may contain up to 150 characters."),Length(max=150)])
    submit = SubmitField('Edit Comment')

class RequestResetForm(FlaskForm):
    email = StringField("Email Address",validators=[DataRequired(message="Please enter an valid email."),Email()])
    submit = SubmitField("Request Password Reset")
    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('No account with that email. Please register first.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[Length(min=6)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Reset Password")

class TwilioLoginForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(message="Please enter account email."),Email()])
    submit = SubmitField('Request verification code')

class TwilioVerifyForm(FlaskForm):
    verificationcode = StringField('Enter verification code',validators=[DataRequired(message="Please enter code sent to your phone number.")])
    submit = SubmitField('Submit Code')