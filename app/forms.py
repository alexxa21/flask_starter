from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired, FileField
from wtforms.fields import StringField, TextAreaField, IntegerField, DecimalField, SelectField
from wtforms.validators import InputRequired, ValidationError


class PropertyForm(FlaskForm):
    title = StringField('Property Title', validators=[InputRequired()])
    description = TextAreaField('Description', validators=[InputRequired()])
    rooms = StringField('No. of Rooms', validators=[InputRequired()])
    bathrooms = StringField('No. of Bathrooms', validators=[InputRequired()])
    price = StringField('Price', validators=[InputRequired()])
    property = SelectField('Property Type',validators=[InputRequired()], choices=[('House', 'House'), ('Apartment', 'Apt')])
    location = StringField('Location', validators=[InputRequired()])
    photo = FileField('Photo Upload', validators= [FileRequired(), FileAllowed(['jpg','png','Images'])])
