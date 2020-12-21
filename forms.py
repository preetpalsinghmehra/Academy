from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError




# from main import User


class SignUpForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=10, max=30)])
    picture = FileField('Image', validators=[FileAllowed(['jpg', 'png'])])
    mobile = IntegerField('Mobile Number', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    address = StringField('Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = SelectField('State', validators=[DataRequired()],
                        choices=['Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh', 'Goa',
                                 'Gujarat', 'Haryana',
                                 'Himachal Pradesh', 'Jammu and Kashmir', 'Jharkhand', 'Karnataka', 'Kerala',
                                 'Madhya Pradesh',
                                 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Orissa', 'Punjab',
                                 'Rajasthan', 'Sikkim',
                                 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttaranchal', 'Uttar Pradesh', 'West Bengal'])
    zip = IntegerField('Zip', validators=[DataRequired()])
    submit = SubmitField('Sign In')
    '''
    def validate_email(self, email):
        email = Users.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('That email has been taken.Please choose a different email')

    def validate_mobile(self, mobile):
        mobile = Users.query.filter_by(mobile=mobile.data).first()
        if mobile:
            raise ValidationError('That Mobile Number has been taken.Please choose a different Mobile Number')
    '''


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=10, max=30)])
    picture = FileField('Update Profile Image', validators=[FileAllowed(['jpg', 'png'])])
    mobile = IntegerField('Mobile Number', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    address = StringField('Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = SelectField('State', validators=[DataRequired()],
                        choices=['Andra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh', 'Goa',
                                 'Gujarat', 'Haryana',
                                 'Himachal Pradesh', 'Jammu and Kashmir', 'Jharkhand', 'Karnataka', 'Kerala',
                                 'Madhya Pradesh',
                                 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Orissa', 'Punjab',
                                 'Rajasthan', 'Sikkim',
                                 'Tamil Nadu', 'Telagana', 'Tripura', 'Uttaranchal', 'Uttar Pradesh', 'West Bengal'])
    zip = IntegerField('Zip', validators=[DataRequired()])
    submit = SubmitField('Update')


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    '''
    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('There is no account with that email.Please register first.')
    '''


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')


