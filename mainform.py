from flask_wtf import FlaskForm
from wtforms import TextField, StringField, SubmitField, TextAreaField, RadioField, IntegerField, DateField
from wtforms import validators, ValidationError


class MainForm(FlaskForm):
    firstname = StringField("First Name:", [validators.DataRequired("Please enter your first name")])
    lastname = StringField("Last Name:", [validators.DataRequired("Please enter your second name")])
    address = TextAreaField("Address:", [validators.DataRequired("Please enter your address")])
    suburb = StringField('Suburb', [validators.DataRequired("Please enter your address")])
    postcode = StringField('Postcode', [validators.DataRequired("Please enter the postcode")])
    phoneNumber = StringField('Suburb', [validators.DataRequired("Please enter your phone number")])
    email = StringField("Email", [validators.DataRequired("Please enter your email address."),
                                validators.Email("Please enter a correct address.")])
    birthdate=DateField("Birthdate",[validators.DataRequired("Please enter the birth date.")] , format='%Y-%m-%d')
    gender = RadioField('Gender', choices = [('Male','Male'),('Female','Female'), ('Other', 'Other')])
    bio = TextAreaField('Biography', [validators.DataRequired("Please enter your email address.")])
    submit = SubmitField('Submit')