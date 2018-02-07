from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, BooleanField
from wtforms.validators import Length
from wtforms.widgets import TextArea

class SigninForm(FlaskForm):

	username = StringField('Username', validators=[Length(min = 6,max = 20)])
	password = PasswordField('Password', validators=[Length(min= 6, max = 20)])

class PostForm(FlaskForm):

	title = StringField("Title", validators=[Length(min = 6, max = 32)])
	category = SelectField("category")
	content = StringField("Content", widget=TextArea())
	is_md = BooleanField("Markdown")