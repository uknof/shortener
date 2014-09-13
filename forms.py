from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField, BooleanField, SubmitField, validators
 
class ContactForm(Form):
  name = TextField("Name")
  email = TextField("Email")
  subject = TextField("Subject")
  message = TextAreaField("Message")
  submit = SubmitField("Send")

class AddForm(Form):
  specific = BooleanField("specific")
  number = TextField("number")
  dest = TextField("dest", [validators.Required("Destination URL required")])
  submit = SubmitField("Add")
