from datetime import datetime
from FarmerMarketLocator import db, login_manager,bcrypt
from flask_admin.contrib.sqla import ModelView
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app,abort
from flask_login import UserMixin,current_user


DEFAULT_IMG="/static/images/user.png"

@login_manager.user_loader
def load_user(user_id):
    # creates current_user
    return User.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized():
    # redirect for unauthorized users
    abort(403)
    


class User(db.Model,UserMixin): 
    """User in the system."""
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20),nullable=False,unique=True)
    email = db.Column(db.String(35),nullable=False,unique=True)
    phone = db.Column(db.VARCHAR(12),nullable=False)
    password = db.Column(db.Text,nullable=False)
    image_url = db.Column(db.Text,nullable=False,default=DEFAULT_IMG)
    bio = db.Column(db.Text)
    location = db.Column(db.Text)
    is_admin = db.Column(db.Boolean,default=False,nullable=False)
    favorites = db.relationship('Favorite',backref='user',lazy=True)
    comments = db.relationship('Comment',backref='user',lazy=True)
  
    
    def __repr__(self):
        return f'<{self.id}:{self.username}>'  
    
    def get_reset_token(self,expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'],expires_sec)
        return s.dumps({'user_id':self.id}).decode('utf8')
    
 
    @classmethod
    def format_user_phone(cls,email):
        user = User.query.filter_by(email=email).first_or_404()
        return f'+1{user.phone}'
    
        
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)
    

    @classmethod
    def signup(cls, username, email, phone, password):
        # Sign up user.Hashes password and adds user to system
        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')
        user = User(
            username=username,
            email=email,
            phone=phone,
            password=hashed_pwd,
        )
        db.session.add(user)
        return user
    @classmethod
    def authenticate(cls, email, password):
        # verify user account login with hashed database information
        user = cls.query.filter_by(email=email).first_or_404()
        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user
        return False

  
class Market(db.Model):
    __tablename__ = 'markets'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.Text,nullable=False)
    comments = db.relationship('Comment',backref='market',lazy=True)
    favorites = db.relationship('Favorite',backref='markets',lazy=True)

    def __repr__(self):
        return f'<Market - #{self.id}:{self.name}>'


class Favorite(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id', ondelete='CASCADE'),nullable=False,primary_key=True)
    market_id = db.Column(db.Integer,db.ForeignKey('markets.id', ondelete='CASCADE'),nullable=False,primary_key=True)
    
    def __repr__(self):
        return f'<Favorite -{self.id},Market:{self.market_id},User:{self.user_id}>'
    
    
    @classmethod
    def check_user_favorites(cls,user_id,market_id):
    # check if user has market information in favorite list, returns boolean
    # method used to toggle favorite button style and verify if add/remove from database
        favorite = cls.query.filter_by(user_id=user_id,market_id=market_id).first()
        if favorite:
            return True
        else:
            return False

    @staticmethod
    def add_user_favorite(user_id,market_id):
        # add market information to user favorite list,updates database
        new_fav=Favorite(
            user_id= user_id,
            market_id = market_id
            )
        db.session.add(new_fav)
        db.session.commit()
        return new_fav

    @staticmethod 
    def remove_user_favorite(user_id,market_id):
        # remove market information to user favorite list,updates database
        favorite = Favorite.query.filter_by(user_id=user_id,market_id=market_id).first()
        db.session.delete(favorite)
        db.session.commit()


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    content = db.Column(db.String(150),nullable=False)
    date_posted = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id',ondelete='CASCADE'),nullable=False)
    market_id = db.Column(db.Integer,db.ForeignKey('markets.id',ondelete='CASCADE'),nullable=False)
    flagged = db.Column(db.Boolean,default=False,nullable=False)

    def __repr__(self):
        return f'<Comment - #{self.id},{self.user_id},{self.market_id},{self.content}>'

    def add_user_comment(form,market_id):
        # add user account comments to market profiles,updates database
        user_id = current_user.id
        comment = Comment(
            content=form.content.data,
            user_id = user_id,
            market_id=market_id
            )
        db.session.add(comment)
        db.session.commit()
        return comment

    @classmethod
    def add_comment_flag(cls,comment_id):
        # flagged user comment as inappropriate,updates database
        comment = cls.query.filter_by(id=comment_id).first()
        comment.flagged = True
        db.session.commit()
        return comment





# Flask Admin view routes -- user must be logged in and verified to have
# admin role
class CommentView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin
    def inaccessible_callback(self):
        if not current_user.is_admin:
            abort(403)
            
class UserView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin
    def inaccessible_callback(self):
        if not current_user.is_admin:
            abort(403)

class MarketView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin
    def inaccessible_callback(self):
        if not current_user.is_admin:
            abort(403)
	
class FavoriteView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin
    def inaccessible_callback(self):
        if not current_user.is_admin:
            abort(403)


