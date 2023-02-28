from flask import Blueprint,render_template,flash

errors = Blueprint('errors',__name__)

class MyCustomZipcode404(Exception):
    pass

# ERROR PAGES
# page not found
@errors.app_errorhandler(404)
def error_404(error):
    flash('Not Found.','danger')
    message= f'Page not found or has moved.'
    return render_template('errors/error.html',message=message), 404
# not authorized error
@errors.app_errorhandler(403) 
def error_403(error):
    flash('Not Authorized.','danger')
    message= f"You don't have permission to do that. Please login or sign-up and try again."
    return render_template('errors/error.html',message=message), 403
# internal error
@errors.app_errorhandler(500)
def error_500(error):
    flash('Something went wrong.','danger')
    message=f'Please try again later.'
    return render_template('errors/error.html',message=message), 500
#method not allowed
@errors.app_errorhandler(405)
def error_405(error):
    flash('Error.','danger')
    message=f'Method not allowed.'
    return render_template('errors/error.html',message=message), 405
#custom error for zipcode not found
@errors.app_errorhandler(MyCustomZipcode404)
def zipcode_not_found(error):
    message=f"Failed results for zipcode. Please try a different one."
    return render_template('errors/error.html',message=message), 404