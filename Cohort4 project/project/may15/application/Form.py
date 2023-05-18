from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class BasicForm(FlaskForm):
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    Email_Address = StringField('Email')
    Username = StringField('Username')
    Password = StringField('Password')
    submit = SubmitField('Add Customer')