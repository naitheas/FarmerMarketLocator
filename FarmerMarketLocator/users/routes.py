import os
from FarmerMarketLocator import db,bcrypt
from flask import render_template,redirect,flash,url_for,request,Blueprint,abort
from FarmerMarketLocator.forms import (EditUserForm,LoginForm,RegisterForm,
            RequestResetForm,ResetPasswordForm)
from flask_login import login_user,logout_user,current_user,login_required
from FarmerMarketLocator.models import User,Comment
from FarmerMarketLocator.utils import send_reset_email


users = Blueprint('users',__name__)

#render registration page
@users.route('/register', methods=["GET","POST"])
def register_user():
    if current_user.is_authenticated:
        return redirect(url_for('main.homepage'))
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                email=form.email.data,
                phone=form.phone.data,
                password=form.password.data
            )
            db.session.commit()
            flash(f'Account created for { user.username }! Please login.','success')
            return redirect(url_for('users.login'))
        except:
            abort(500)
    return render_template('users/register.html',form=form)


#login page for registered users
@users.route('/login', methods=["GET","POST"])
def login():
    # bypass if user is logged in
    if current_user.is_authenticated:
        return redirect(url_for('main.homepage'))
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = User.authenticate(form.email.data,form.password.data)
            if user:
                login_user(user,remember=form.remember.data)
                flash('Login successful.','success')
                # protect against open redirects
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('main.homepage'))
            flash('Invalid credentials.','danger')
        except:
            abort(500)
    return render_template('users/login.html',form=form)



#user logout route
@users.route('/logout')
@login_required
def logout():
    try:
        logout_user()
        flash(f'Logged out.', 'success')
        return redirect(url_for('users.login'))
    except:
        abort(500)
    return redirect(url_for('users.login'))
 

#user request password reset -- sends JSON token to email
@users.route('/reset_password', methods=["GET","POST"])
def reset_request():
     # bypass if user is logged in
    if current_user.is_authenticated:
        return redirect(url_for('main.homepage'))
    form = RequestResetForm()
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email = form.email.data).first()
            send_reset_email(user)
            flash('Password reset instructions sent to email.','success')
            return redirect(url_for('users.login'))
        except:
            abort(500)
    return render_template('users/password_request.html',form=form)

# render user password reset form and update database
# verifies JSON token for access
@users.route('/reset_password/<token>', methods=["GET","POST"])
def verify_reset(token):
     # bypass if user is logged in
    if current_user.is_authenticated:
        return redirect(url_for('main.homepage'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('Invalid or expired token.','danger')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        try:
            hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('UTF-8')
            user.password = hashed_pwd
            db.session.commit()
            flash(f'Password updated for { user.username }! You are now able to log in.','success')
            return redirect(url_for('users.login'))
        except:
            abort(500)
    return render_template('users/password_reset.html',form=form)
# ---------- USER VIEWS-----------
#show user profile w/404 handler
# anon user allowed
@users.route('/users/<int:user_id>')
def user_profile(user_id):
    user = User.query.get_or_404(user_id)
    page = request.args.get('page',1,type=int)
    comments = Comment.query.filter_by(user_id=user_id,flagged=False).order_by(Comment.date_posted.desc()).paginate(page=page,per_page=5)
    return render_template('users/profile_user.html', user=user,comments=comments)

#edit profile route
# user required, must be current user
@users.route('/users/<int:user_id>/edit', methods=['GET','POST'])
@login_required
def edit_profile(user_id):
    if current_user.id != user_id:
        abort(403)
    user = current_user
    form = EditUserForm(obj=user)
    if form.validate_on_submit():
        try:
            form.populate_obj(user)
            db.session.commit()
            flash('Profile updated!','success')
            return redirect(url_for('users.user_profile',user_id=user_id))
        except:
            abort(500)
    return render_template('users/edit_user.html', form=form)

#delete account route
# user required, must be current user
@users.route('/users/delete', methods=['POST'])
@login_required
def delete_user():
    user_to_delete = User.query.filter_by(id= current_user.id).first_or_404()
    try:
        logout_user()
        db.session.delete(user_to_delete)
        db.session.commit()
        flash('Profile deletion successful.','success')
        return redirect(url_for('users.register_user'))  
    except:
        abort(500)
    


