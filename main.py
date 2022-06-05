from app import app
from flask_login import LoginManager


from app import db
def create_app():
    from models import User
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):

        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

from views import *
create_app()
if '__main__' == __name__:
	app.run('0.0.0.0', debug=True)
