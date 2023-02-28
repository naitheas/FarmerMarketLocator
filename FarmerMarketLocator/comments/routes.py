from FarmerMarketLocator import db
from FarmerMarketLocator.models import Comment
from FarmerMarketLocator.forms import EditCommentForm
from flask import flash,redirect,render_template,Blueprint,abort,url_for
from flask_login import login_required,current_user


comments = Blueprint('comments',__name__)


# edit/update user comment, login required, user must be comment author
@comments.route('/comments/<int:comment_id>/edit', methods=['GET','POST'])
@login_required
def edit_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first_or_404()
    if current_user.id != comment.user_id:
        abort(403)
    form = EditCommentForm(obj=comment)
    if form.validate_on_submit():
        try:
            form.populate_obj(comment)
            db.session.commit()
            flash('Comment updated.', 'success')
            return redirect(url_for('markets.show_market',market_id=comment.market_id))   
        except:
            abort(405)
    return render_template('markets/edit_mkt_comment.html', comment=comment, form=form)

#delete user comment,login required, user must be comment author
@comments.route('/comments/<int:comment_id>/delete', methods=["POST"])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first_or_404()
    if current_user.id != comment.user_id:
        abort(403)
    try:
        db.session.delete(comment)
        db.session.commit()
        flash("Comment deletion successful.","success")
        return redirect(url_for('markets.show_market',market_id=comment.market_id))
    except:
        abort(405)

# user flag comment,login required, user cannot be comment author
@comments.route('/comments/<int:comment_id>/flag', methods=["POST"])
@login_required
def flag_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first_or_404()
    if current_user.id == comment.user_id:
        abort(403)
    try:        
        Comment.add_comment_flag(comment_id)
        flash('Comment flagged for review.', 'success')
        return redirect(url_for('markets.show_market',market_id=comment.market_id))   
    except:
        abort(405)




