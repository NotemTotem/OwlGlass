from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,SelectField,ValidationError
from wtforms.validators import DataRequired

#Accountfinder form class
class AccountfinderForm(FlaskForm):
    target = StringField("Target",validators=[DataRequired()],render_kw={"placeholder": "Target's username or email"}
)
    target_type = SelectField("Target Type",choices=['username','email'])
    submit = SubmitField("Submit")

    def validate_target(form,field):
        if form.target_type.data == 'email':
            if not('@' in (field.data) and '.' in field.data.split('@')[1] and len(field.data.split('@')[0]) >0):
                raise ValidationError("Not a valid email.")

                 
            