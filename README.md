# Capstone-Project
Farmers Market Locator is an web application that can be used to locate a farmers market based off the user's zipcode input. This application allows an account user to favorite their markets for quick reference.
Features: Responsive web design, two-step authentication, authenticated user routes,pagination, user password resets, blueprinting
Front End: BootStrap,FontAwesome, Javascript
Back End: Python, Flask, SQLAlchemy, BCrypt, WTForms, Flask Mail, Flask Login, Flask Admin, PyJWT
Database: PostgreSQL


<h3>API List</h3><hr>
<a href="https://search.ams.usda.gov/farmersmarkets/v1/svcdesc.html" target="_blank">USDA</a> |
<a href="https://www.twilio.com/docs/verify/api" target="_blank">Twilio</a> |
<a href="https://developer.mapquest.com/documentation/geocoding-api/" target="_blank">Mapquest</a>


<h3>To Run</h3><hr>
Use flask from within the primary directory folder, FMLocator

Terminal commands ----

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt

flask run