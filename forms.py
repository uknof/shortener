from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField, BooleanField, SubmitField, validators

class AddForm(Form):
  notes = TextField("Notes")
  dest = TextField("Destination URL", [validators.Required("Destination URL required")])
  submit = SubmitField("Shorten")

class LoginForm(Form):
  username = TextField("Username")
  password = TextField("Password")
  submit = SubmitField("Login")
  
