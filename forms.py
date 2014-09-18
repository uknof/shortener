from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField, BooleanField, SubmitField, validators

class AddForm(Form):
  specific = BooleanField("Meeting specific")
  number = TextField("Meeting number")
  custom = TextField("Custom")
  notes = TextField("Notes")
  dest = TextField("Destination URL", [validators.Required("Destination URL required")])
  submit = SubmitField("Add")

class LoginForm(Form):
  username = TextField("Username")
  password = TextField("Password")
  submit = SubmitField("Login")
  
