from app import Login
from app.model import User
@Login.user_loader
def load_user(id):
	return User.query.get(int(id))