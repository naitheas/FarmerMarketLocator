import os,requests
from sqlalchemy.exc import IntegrityError
from flask import abort,flash,url_for
from flask_mail import Message
from FarmerMarketLocator import mail,db
from FarmerMarketLocator.models import Market
from FarmerMarketLocator.errors import MyCustomZipcode404

def get_marketlist(zip):
    # generate marketlist from zip input
    try:
        resp = requests.get(f'http://search.ams.usda.gov/farmersmarkets/v1/data.svc/zipSearch?zip={zip}')
        data = resp.json()
        markets = data['results']
        # manual error catch for JSON reponse
        if markets[0]['id'] == 'Error':
            flash(f"Failed results for zipcode: {zip}", "danger")
            raise MyCustomZipcode404
        # add name and ID to db for persisting data
        # does not populate on single market search
        add_market(markets)
        return markets
    except:
        raise MyCustomZipcode404
    
def add_market(markets):
    # isolate market name and id to add to db
    for market in markets:
        market_id = market['id']
        market_name = market['marketname'][4:]
        new_market = Market(id = market_id,
        name = market_name)
        market = Market.query.filter_by(id=market_id).first()
        if market:
            pass
        # if no market, adds market name and id to database for persisting data 
        else:
            try:
                db.session.add(new_market)
                db.session.commit()
                print("****** Added to session. ******")
            except IntegrityError:
                print("Error adding market.")

def request_market(market_id):
    # Find specific market information for profile,return error if not found
    # or error occured in request
    try:
        resp = requests.get(f'http://search.ams.usda.gov/farmersmarkets/v1/data.svc/mktDetail?id={market_id}')
        data = resp.json()
        market ={
            'id' : market_id,
            'address' : data['marketdetails']['Address'],
            'googlelink' :data['marketdetails']['GoogleLink'],
            'products' : (data['marketdetails']['Products'].replace(";",",")),
            'schedule':(data['marketdetails']['Schedule'].replace("<br>","")),
            'mapCoords':get_coords(data['marketdetails']['Address'])
        }
        return market
    except:
        abort(500)  


def send_reset_email(user):
    # send JSON token to user email with default expiring timer
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                sender='noreply@farmermarketlocator.com',
                recipients=[user.email])
    msg.body = f'''To reset your password, visit the link below:
        {url_for('users.verify_reset',token=token,_external=True)}

    If you did not make this request, please ignore this email and no changes will be made.
    '''
    mail.send(msg)


# MAPQUEST API CALLS FROM ZIP FORM SEARCH-------------------------
mapKey = os.environ.get('mapKey')
mapSecret = os.environ.get('mapSecret')
MAP_BASE_URL = "http://www.mapquestapi.com/geocoding/v1"
def get_coords(address):
    # make API call with market address to generate map icon by coordinates
    # returns error if no response
    try:
        res = requests.get(f"{MAP_BASE_URL}/address",
                    params={'key': mapKey, 'location': address})
        data = res.json()
        lat = data['results'][0]['locations'][0]['latLng']['lat']
        lng = data['results'][0]['locations'][0]['latLng']['lng']
        mapUrl = f'https://www.mapquestapi.com/staticmap/v5/map?locations={lat},{lng}&zoom=16&size=400,400&defaultMarker=marker-start&key={mapKey}'
        coords = {'lat':lat,
                  'lng': lng,
                  'map':mapUrl}
        return coords
    except:
        abort(500)