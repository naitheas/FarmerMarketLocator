from FarmerMarketLocator import admin,db
import random
from flask import render_template,flash,request,Blueprint,redirect,url_for
from FarmerMarketLocator.utils import get_marketlist
from FarmerMarketLocator.models import Comment,User,Market,Favorite,MarketView,CommentView,UserView,FavoriteView

main = Blueprint('main',__name__)
# ----------------MAIN ROUTES---------------------------
#render landing page    
@main.route('/')
def homepage():
    random_fact = random.choice(facts)
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
        flash(f"Search results for zipcode:{zip}", "success")
        return render_template('search.html',market_list=markets)
    return redirect(url_for('main.homepage'))




facts = ["Proximity to farmers markets is associated with lower body mass index.",
"There are 3.5 times as many farmers over the age of 65 as there are farmers under the age of 35.",
" Farmers markets provide one of the only low-barrier entry points for new farmers, allowing them to start small as they learn and test the market.",
"75% of direct marketing farmers use organic practices to grow and raise food.",
"California has the most farmers markets!",
"40 acres of farmland are lost to development every hour!",]


    # FLASK ADMIN VIEWS

admin.add_view(UserView(User,db.session))
admin.add_view(MarketView(Market,db.session))
admin.add_view(CommentView(Comment,db.session))
admin.add_view(FavoriteView(Favorite,db.session))


