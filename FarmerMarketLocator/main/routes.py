from FarmerMarketLocator import admin,db
import yaml
import random
from flask import render_template,flash,request,Blueprint,redirect,url_for
from FarmerMarketLocator.utils import get_marketlist
from FarmerMarketLocator.models import Comment,User,Market,Favorite,MarketView,CommentView,UserView,FavoriteView

with open("FarmerMarketLocator/FarmerMarketLocator/static/fact_list.yml", "r") as file:
    try:
        fact_data = yaml.safe_load(file)
    except yaml.YAMLError as exception:
        print(exception)

main = Blueprint('main',__name__)

# ----------------MAIN ROUTES---------------------------
#render landing page    
@main.route('/')
def homepage():
    random_fact = random.choice(fact_data["facts"])
    page = request.args.get('page',1,type=int)
    comments = Comment.query.filter_by(flagged=False).order_by(Comment.date_posted.desc()).paginate(page=page,per_page=5)
    return render_template('index.html',random_fact=random_fact,comments=comments)

# handle search form input
# anon user searches allowed
@main.route('/search',methods=['GET','POST'])
def show_search():
    if request.method == 'POST':
        zip = request.form.get('zip')
        markets = get_marketlist(zip)
        flash(f"Search results for zipcode: {zip}", "success")
        return render_template('search.html',market_list=markets)
    return redirect(url_for('main.homepage'))

@main.route('/resources')
def resources():
    return render_template('resource_links.html')



# ------FLASK ADMIN VIEWS--------------

admin.add_view(UserView(User,db.session))
admin.add_view(MarketView(Market,db.session))
admin.add_view(CommentView(Comment,db.session))
admin.add_view(FavoriteView(Favorite,db.session))


