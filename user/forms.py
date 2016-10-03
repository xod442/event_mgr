from flask_wtf import Form
from wtforms import validators, StringField, PasswordField, SelectField
from wtforms.widgets import TextArea
from wtforms.fields.html5 import EmailField
from wtforms.validators import ValidationError
from flask_wtf.file import FileField, FileAllowed
import re

from user.models import User

class RegisterForm(Form):
    e1 = 'Plano-Oct 25, 2016 Location: 660 Data Drive, Plano, TX 75075 9:00 to 5:00PM CST'
    e2 = 'Houston-Oct 27, 2016 Location: Houston, TX 75075 9:00 to 5:00PM CST'
    first_name = StringField('First Name', [validators.DataRequired()])
    last_name = StringField('Last Name', [validators.DataRequired()])
    email = EmailField('Email address', [
        validators.DataRequired(),
        validators.Email()
        ]
    )
    company = StringField('Company')

    phone = StringField('Phone', [
        validators.DataRequired()
        ]
    )
    job = StringField('Job')

    question = StringField('Question')


    event = SelectField('Events', choices=[
        ('event', 'Please choose an event'),
        (e1, e1),
        (e2, e2),
        ]
    )
