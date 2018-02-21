from app import Login
from app.model import User
import re

@Login.user_loader
def load_user(id):
	return User.query.get(int(id))

escape_dict = {
	"\"" : "&quot",
	"\'" : "&apos",
	"&" : "&amp",
	"<" : "&lt",
	">" : "&gt",
	"\n" : "<br>",
	r" " : "&nbsp",
	"\t": "&nbsp&nbsp&nbsp&nbsp"
}
rx = re.compile("|".join(map(re.escape, escape_dict)))

def convert_to_html(text):
	#simple
	return rx.sub(lambda x : escape_dict[x.group(0)], text)