from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField, BooleanField, SubmitField, PasswordField, validators

class AddForm(Form):
  notes = TextField("Notes")
  dest = TextField("Destination URL", [validators.Required("Destination URL required")])
  submit = SubmitField("Shorten")

class LoginForm(Form):
  username = TextField("Username")
  password = PasswordField("Password")
  submit = SubmitField("Login")

