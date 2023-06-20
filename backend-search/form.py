"""Form object declaration."""
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
)
from wtforms.validators import DataRequired, Email


""" class ContactForm(FlaskForm):

    title = StringField("Title", [DataRequired()])
    plot = StringField(
        "Plot", [DataRequired()])
    genre = StringField(
        "Genre", [DataRequired()]
    )
    actors = StringField("Actors", [DataRequired()])
    directors = StringField("Directors", [DataRequired()])
    released = StringField("Released", [DataRequired()])
    imdbRating = StringField("ImdbRating", [DataRequired()])
    url = StringField("URL", [DataRequired()])
    movie_completion = StringField("Movie_completion", [DataRequired()])
    submit = SubmitField("Submit") """

class DataProductForm(FlaskForm):
    data_prod_name = StringField("Data Produt Name", [DataRequired()])
    #project_url = StringField("Project URL", [DataRequired()])
    #term_of_use = StringField("Term Of Use", [DataRequired()])
    tags = StringField("Tags", [DataRequired()])
    data_prod_owner = StringField("Data Produt Owner", [DataRequired()])
    data_prod_owner_contact = StringField("Data Produt Owner Contact", [
            Email(message=('Not a valid email address.')),
            DataRequired()
        ])
    res_tech_team = StringField("Responsible Technical Team", [DataRequired()])
    tech_support_contact = StringField("Technical Support Contact", [
            Email(message=('Not a valid email address.')),
            DataRequired()
        ])
    business_unit = StringField("Business Unit", [DataRequired()])
    data_prod_business_description = StringField("Data Produt Business Description", [DataRequired()])
    #security_manage = StringField("Security Management", [DataRequired()])
    #conceptual_model = StringField("Conceptual Model", [DataRequired()])
    #data_model = StringField("Data Model", [DataRequired()])
    #user_dp = StringField("User Data Product", [DataRequired()])
    #status = StringField("Status", [DataRequired()])
    #input_port = StringField("Input Port", [DataRequired()])
    #output_port = StringField("Output Port", [DataRequired()])
    submit = SubmitField("Submit")
 