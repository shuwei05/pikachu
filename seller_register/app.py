from flask import Flask, render_template, redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import SubmitField, HiddenField

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///seller_info_db"
app.config["SECRET_KEY"] = '868392913afea5d2c99531d7'
seller_info_db = SQLAlchemy(app)

@app.route("/map",methods = ["GET"])
def map_page():
    seller_coordinates = seller_info_db.session.query(Seller_Info.latitude,Seller_Info.longitude).all()
    coordinates = []
    for coordinate in seller_coordinates:
        coordinates.append(list(coordinate))
    return render_template("map.html",coordinates=coordinates)

@app.route("/seller_register",methods=["GET","POST"])
def seller_register_page():
    seller_register_form = Seller_Register_Form()
    if seller_register_form.validate_on_submit():
        seller_to_create = Seller_Info(latitude = seller_register_form.latitude.data,
                                       longitude = seller_register_form.longitude.data)
        
        #checking for whether got same location
        existing_location = Seller_Info.query.filter_by(latitude = seller_register_form.latitude.data,
                                       longitude = seller_register_form.longitude.data).first()
        if existing_location:
            print("same location") #command prompt see; considering use flash to tell user resubmit again
            return render_template("Ssign.html",seller_register_form=seller_register_form)
         
        #show in command prompt the value when added
        print("Submit")
        print(seller_register_form.latitude.data,
              seller_register_form.longitude.data)

        seller_info_db.session.add(seller_to_create)
        seller_info_db.session.commit()
        return redirect(url_for("map_page"))
    
    else: 
        #show in command prompt the value when failed
        print("Failed Submitted")
    
    return render_template("Ssign.html",seller_register_form=seller_register_form)

class Seller_Info(seller_info_db.Model):
    #stall_name; stall_owner_name; email; password; confirm_password; operation hours; stall description; stall_img; stall_bg_img
    id = seller_info_db.Column(seller_info_db.Integer(),primary_key=True)
    latitude = seller_info_db.Column(seller_info_db.Float(),nullable=False) #remove unique bcs not unique
    longitude = seller_info_db.Column(seller_info_db.Float(),nullable=False)

    #show in command prompt the value
    def __repr__(self):
        return f'Seller_Info({self.latitude},{self.longitude})'
    
class Seller_Register_Form(FlaskForm):
    latitude = HiddenField(label="latitude")
    longitude = HiddenField(label="longitude")
    submit = SubmitField(label="Submit")