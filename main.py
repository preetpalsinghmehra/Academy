import os
import secrets
from flask import Flask, render_template, flash, redirect, url_for, request
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, current_user, logout_user, LoginManager, login_required
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_mail import Mail, Message
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from forms import SignUpForm, LoginForm, UpdateForm, RequestResetForm, ResetPasswordForm

app = Flask(__name__)

#  configurations
app.config['SECRET_KEY'] = b'Qxv\xf3\x8d\x91@\xa6\xc8h\xec\xb3\x03\xf9\x9a\xd8'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
db = SQLAlchemy(app)
mail = Mail(app)
admin = Admin(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    image_file = db.Column(db.String(100), nullable=False, default='default.jpg')
    email = db.Column(db.String(30), unique=True, nullable=False)
    mobile = db.Column(db.Integer, unique=True, nullable=False)
    password = db.Column(db.Text(20), nullable=False)
    address = db.Column(db.String(100), unique=False, nullable=False)
    city = db.Column(db.String(20), unique=False, nullable=False)
    state = db.Column(db.String(20), unique=False, nullable=False)
    zip = db.Column(db.Integer, unique=False, nullable=False)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)

        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


class Questions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ques = db.Column(db.Text, nullable=False)
    ch1 = db.Column(db.String, nullable=False)
    ch2 = db.Column(db.String, nullable=False)
    ch3 = db.Column(db.String, nullable=False)
    ch4 = db.Column(db.String, nullable=False)
    ans = db.Column(db.String, nullable=False)


class Contact(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=False, nullable=False)
    email = db.Column(db.String(30), unique=False, nullable=False)
    title = db.Column(db.String(50), unique=False, nullable=False)
    message = db.Column(db.String(100), unique=False, nullable=False)


admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Contact, db.session))
admin.add_view(ModelView(Questions, db.session))


@app.route('/', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('demotest'))
    form = SignUpForm()
    if form.validate_on_submit():
        if request.method == 'POST':
            name = form.name.data
            picture = form.picture.data
            email = form.email.data
            mobile = form.mobile.data
            password = generate_password_hash(form.password.data)
            address = form.address.data
            state = form.state.data
            city = form.city.data
            zip = form.zip.data
            user = User(name=name, email=email, mobile=mobile,
                        password=password, address=address,
                        state=state, city=city, zip=zip)
            db.session.add(user)
            db.session.commit()
        flash(f'Account has been created for {form.name.data}!!', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('demotest'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('demotest'))
        else:
            flash('Login Unsuccessful!! Please Check Your Email & Password!', 'danger')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('signup'))


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset', sender='noreply@demo', recipients=[user.email])
    msg.body = f'''Please click on the link to reset your password!:
    {url_for('reset_token', token=token, _external=True)}
    If you did not make this request then simply ignore this email & no changes will be made'''
    mail.send(msg)


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('signup'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent to reset your password', 'info')
        return redirect(url_for('login'))
    return render_template('request_reset.html', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('signup'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        password = generate_password_hash(form.password.data)
        user.password = password
        db.session.commit()
        flash('Yor password has been updated!', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', form=form)


'''
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    form_picture.save(picture_path)

    return picture_fn
'''


@app.route('/account')
@login_required
def account():
    image_file = url_for('static', filename='/profile_pics' + current_user.image_file)
    return render_template('account.html', image_file=image_file)


@app.route('/updateinfo', methods=['GET', 'POST'])
@login_required
def updateinfo():
    form = UpdateForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.name = form.name.data
        current_user.email = form.email.data
        current_user.mobile = form.mobile.data
        current_user.address = form.address.data
        current_user.city = form.city.data
        current_user.state = form.state.data
        current_user.zip = form.zip.data
        db.session.commit()
        flash('Your Profile has been Updated!!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.email.data = current_user.email
        form.mobile.data = current_user.mobile
        form.address.data = current_user.address
        form.city.data = current_user.city
        form.state.data = current_user.state
        form.zip.data = current_user.zip
    return render_template('updateinfo.html', form=form)


'''
@app.route('/')
def home():
    return render_template('home.html')
'''


@app.route('/enroll')
def enroll():
    return render_template('howtoenroll.html')


@app.route('/syllabus')
def syllabus():
    return render_template('syllabus.html')


@app.route('/demotest', methods=['POST', 'GET'])
@login_required
def demotest():
    questions = Questions.query.all()
    correct = 0
    for q in questions:
        #name = str(q.id)
        answered = request.form[f'{q.id}']
        print(answered)
        if q.ans == answered:
            correct = correct + 1
    print(correct)
    return render_template('demotest.html', questions=questions)


@app.route('/result')
def result():
    return render_template('result.html')


@app.route('/contact', methods=['POST', 'GET'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        title = request.form['title']
        message = request.form['message']
        contacts = Contact(name=name, email=email, title=title, message=message)
        db.session.add(contacts)
        db.session.commit()
        flash('Your mesage has been sent.We will contact you soon!', 'info')
        return redirect(url_for('contact'))
    return render_template('contactus.html')


if __name__ == '__main__':
    app.run(debug=True)
