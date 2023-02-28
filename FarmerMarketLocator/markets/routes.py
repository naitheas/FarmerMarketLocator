from flask import render_template,redirect,flash,Blueprint,abort
from flask_login import login_required,current_user
from FarmerMarketLocator.utils import *
from FarmerMarketLocator.models import Market,Favorite,Comment
from FarmerMarketLocator.forms import CommentForm

markets = Blueprint('markets',__name__)

#MARKET ROUTES-------------------------------------------------------

#show market profile, api call for specific market by ID
# anon user searches allowed
# if user logged in, favorite toggle option is visible
@markets.route('/market/<int:market_id>',methods=['GET','POST'])
def show_market(market_id):
    req_market = request_market(market_id)
    market = Market.query.filter_by(id=market_id).first_or_404()
    comments = Comment.query.filter_by(flagged=False,market_id=market_id).order_by(Comment.date_posted.desc())
    if current_user.is_authenticated:
        favorites = Favorite.check_user_favorites(user_id=current_user.id,market_id=market.id)
        return render_template('markets/profile_market.html',market=market,
                                mkt_info=req_market,comments=comments,favorites=favorites)
    return render_template('markets/profile_market.html',market=market,
                                mkt_info=req_market,comments=comments)

# user account required to add to user favorite list
@markets.route('/market/<int:market_id>/favorite',methods=['POST'])
@login_required
def toggle_favorite_market(market_id):
    favorite = Favorite.check_user_favorites(current_user.id,market_id)
    if favorite is False:
        try:
            Favorite.add_user_favorite(current_user.id,market_id)
            flash('Added market to your favorites!','success')
            return redirect(url_for('markets.show_market',market_id=market_id))
        except:
            abort(500)
    else:
        try:
            Favorite.remove_user_favorite(current_user.id,market_id)
            flash('Removed market from your favorites.','success')
            return redirect(url_for('markets.show_market',market_id=market_id))
        except:
            abort(500)
# user account required to add comments to market profiles
@markets.route('/market/<int:market_id>/comments', methods=['GET','POST'])
@login_required
def add_comment(market_id):
    market = Market.query.get_or_404(market_id)
    form = CommentForm()
    if form.validate_on_submit():
        try:
            Comment.add_user_comment(form,market_id)
            flash('Comment added to market page!','success')
            return redirect(url_for('markets.show_market',market_id=market_id))
        except:
            abort(500)   
    return render_template('markets/add_market_comment.html',market=market, form=form)
