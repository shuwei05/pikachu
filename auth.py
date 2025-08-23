from flask import Blueprint ,  render_template ,request , flash ,redirect, url_for
from .models import User , Stall
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from datetime import datetime

auth = Blueprint('auth',__name__)

@auth.route('/Usign', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        user_name = request.form.get('user_name')
        password1 = request.form.get('password') 
        password2 = request.form.get('password2')

        if len(email) < 4:
            flash('Email must be greater than 3 characters', category='error')
        elif len(user_name) < 4:
            flash('Username must be greater than 3 characters', category='error')   
        elif len(password1) < 7:
            flash('Password must be at least 7 characters', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match', category='error')    
        else:
            new_user = User(email=email, user_name=user_name, password=generate_password_hash(password1,method='pbkdf2:sha256')) 
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))
            # Ensure user is added to the database with format given

        
        pass
    return render_template('Usign.html', text='Signup Page')

@auth.route('/Ssign', methods=['GET', 'POST'])
def Ssignup():
    if request.method == 'POST':
        stallname = request.form.get('stallname','')
        stallowner = request.form.get('stallowner','')
        email = request.form.get('email','')
        password1 = request.form.get('password1','') 
        password2 = request.form.get('password2','')
        openhour_str = request.form.get('openhour', '00:00')
        closehour_str = request.form.get('closehour', '00:00')

        openhour = datetime.strptime(openhour_str, "%H:%M").time()
        closehour = datetime.strptime(closehour_str, "%H:%M").time()

        if len(email) < 4:
            flash('Email must be greater than 3 characters', category='error')
        elif len(stallname) < 2:
            flash('Username must be greater than 3 characters', category='error')  
        elif len(stallowner) < 2: 
            flash('Stall owner name must be greater than 3 characters', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match', category='error') 
        elif openhour >= closehour:
            flash('Open hour must be earlier than close hour', category='error')
        else:
            new_stall = Stall(
            stallname=stallname,
            stallowner=stallowner,
            email=email,
            password=generate_password_hash(password1, method='pbkdf2:sha256'),
            openhour = datetime.strptime(openhour_str, "%H:%M").time(),
            closehour = datetime.strptime(closehour_str, "%H:%M").time()
            )
            db.session.add(new_stall)
            db.session.commit()
            flash('Stall Account Created!', category='success')
            return redirect(url_for('views.home'))
        
    return render_template('Ssign.html', text='Signup Page')

@auth.route('/login',  methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
    return render_template('login.html', text='Login Page')

@auth.route('/logout')  
def logout():
    return render_template('logout.html', text='Logout Page')


