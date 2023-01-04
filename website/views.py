from operator import truediv
from . import db,mail
from .models import bookingdb
from .models import User,Data
from .models import Data
from .models import galleryImageUpload
from flask import Blueprint, render_template, request,redirect, flash,url_for
from sqlalchemy import create_engine
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_login import login_user,LoginManager, login_required, logout_user, current_user
import base64
import io
import re
from types import new_class
from werkzeug.security import generate_password_hash,check_password_hash
from flask import Blueprint,render_template,request,flash,jsonify,redirect,url_for
from distutils.log import debug
from email import message
from sre_constants import SUCCESS
from flask import Flask,render_template,request

from flask_mail import Mail,Message

def render_picture(data):
    render_pic=base64.b64encode(data).decode('ascii')
    return render_pic


views = Blueprint('views', __name__)
 
#login


class RegisterForm(FlaskForm):
    username=StringField(validators=[InputRequired(),Length(min=4,max=20)],render_kw={"placeholder":"username"})
    password=PasswordField(validators=[InputRequired(),Length(min=4,max=20)],render_kw={"placeholder":"password"})
    submit=SubmitField("Register")

    def validate_username(self, username):
        existing_user_username=User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError("The username already exists. Please enter different username")

class LoginForm(FlaskForm):
    username=StringField(validators=[InputRequired(),Length(min=4,max=20)],render_kw={"placeholder":"username"})
    password=PasswordField(validators=[InputRequired(),Length(min=4,max=20)],render_kw={"placeholder":"password"})
    submit=SubmitField("Login")

@views.route("/")
def index():
    return render_template("home.html",user=current_user)


@views.route("/home")
def home():
    return render_template("home.html",user=current_user)

@views.route("/services")
def services():
    return render_template("services.html",user=current_user)



@views.route("/gallery")
def gallery():
    all_data=galleryImageUpload.query.all()
    return render_template("gallery.html",user=current_user,data=all_data)


@views.route("/login",methods=['get','post'])
def login():
    form= LoginForm()
    return render_template("login.html",form=form,user=current_user)

@views.route("/register",methods=['get','post'])
def register():
    form=RegisterForm()
    return render_template("register.html",form=form,user=current_user)

@views.route("/registerForm",methods=['get','post'])
def registerForm():
    if request.method=='POST':
        form=RegisterForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            print(user)
            if user:
                flash("Username alreay exists!! Try another name")
                return redirect(url_for('views.register',user=current_user))
            else:
                new_user=User(username=form.username.data, password=form.password.data, usertype="user")
                db.session.add(new_user)
                db.session.commit()
                user = User.query.filter_by(username=form.username.data).first()
                login_user(user,remember=True)
                return redirect(url_for('views.home',user=current_user))
        return render_template("register.html",form=form,user=current_user)


@views.route("/loginForm",methods=['get','post'])
def loginForm():
    if request.method=='POST':
        form=LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user:
                if(user.password == form.password.data):
                    login_user(user,remember=True)
                    if(user.usertype == "user"):
                        return redirect(url_for('views.home',user=current_user))
                    else:
                        return redirect(url_for('views.galleryAdmin',user=current_user))
                else:
                    flash("Invalid Password")
                    return redirect(url_for('views.login',user=current_user))
            else:
                flash("Username not found!!")
                return redirect(url_for('views.login',user=current_user))
        return render_template("register.html",form=form,user=current_user)

@views.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.login',user=current_user))

@views.route("/package")
def package():
    return render_template("package.html",user=current_user)


@views.route("/booking",methods=['GET','POST'])
@login_required
def booking():
    email=''
    if request.method=='POST':
        email=request.form['email']
        # print(email)
        # print("Hello")
    all_data=bookingdb.query.filter_by(username=current_user.username)
    print(current_user.username)
    return render_template("booking.html",user=current_user,data=all_data,email=email)
    

@views.route("/bookingForm",methods=['GET','POST'])
@login_required
def bookingForm():
    if request.method == 'POST':
        name=request.form['name']
        email=request.form['email']
        address=request.form['address']
        date=request.form['date']
        phne=request.form['phne']
        wemail=request.form['wemail']
        username=current_user.username
        status="Pending"
        from datetime import datetime
        import datetime

        Db_date=bookingdb.query.filter_by(date=date,status="Accepted").first()
        t_date= datetime.date.today()
        cur=datetime.datetime.strptime(date,'%Y-%m-%d')
        c_date=cur.date()
        # print(c_date)
        # print("dvdcdc",wemail)
        if(c_date<t_date):
            flash("Enter correct date")
        else:
            my_data=bookingdb(name,email,address,phne,date,username,status,wemail)
            db.session.add(my_data)
            db.session.commit()
            flash("Data send to admin...Wait for admin's response")
        return redirect(url_for('views.booking',user=current_user))

# admin

@views.route("/bookingAdmin")
def bookingAdmin():
    all_data=bookingdb.query.all()
    return render_template("bookingAdmin.html",data=all_data,user=current_user)


@views.route("/packageAdmin")
def packageAdmin():
    return render_template("packageAdmin.html",user=current_user)


@views.route("/galleryAdmin")
def galleryAdmin():
    all_data=galleryImageUpload.query.all()
    return render_template("galleryAdmin.html",data=all_data,user=current_user)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg' ,'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit(".",1)[1].lower() in ALLOWED_EXTENSIONS

@views.route("/galleryImage",methods=['post'])
@login_required
def galleryImage():
    if request.method == 'POST':
        file = request.files['inputFile']

        if file.filename == '':
            flash("Please select an image")
            return redirect(url_for('views.galleryAdmin',user=current_user))
        
        if file and allowed_file(file.filename):
            name = file.filename
            data = file.read()
            final_pic=base64.b64encode(data).decode('ascii')
            upload = galleryImageUpload(name , final_pic)
            db.session.add(upload)
            db.session.commit()
            return redirect(url_for('views.galleryAdmin',user=current_user))
        else:
            flash("Only images are allowed")
            return redirect(url_for('views.galleryAdmin',user=current_user))
 
#accepting and rejecting orders

@views.route("/acceptConcept/<id>")
def acceptConcept(id):
    my_data=bookingdb.query.get(id)
    subject="Worker Verification"
    msg="Your request have been Accepted by Helpcenter"
    msg1="You have a work now "
    # msg=my_data.email,my_data.name
    msg3=my_data.email
    # print(msg3)
    message=Message(subject,sender="kiruthickkumark.20cse@kongu.edu",recipients=[my_data.email])
    message1=Message(subject,sender="kiruthickkumark.20cse@kongu.edu",recipients=[my_data.wemail])
    message1.body=msg1
    message.body=msg
    mail.send(message)
    mail.send(message1)
    # mail.send(message1)
    success ="message send"
    my_data.status="Accepted"
    db.session.commit()
    return redirect(url_for('views.bookingAdmin',user=current_user,success=success))

@views.route("/rejectConcept/<id>")
def rejectConcept(id):
    my_data=bookingdb.query.get(id)
    my_data.status="Rejected"
    db.session.commit()
    return redirect(url_for('views.bookingAdmin',user=current_user))

@views.route("/cancelConcept/<id>")
def cancelConcept(id):
    my_data=bookingdb.query.get(id)
    my_data.status="Canceled"
    db.session.commit()
    return redirect(url_for('views.booking',user=current_user))


# @views.route('/workerdata',methods=['GET','POST'])
# @login_required
# def workerdata():
#     # if request.method =='POST':
    #     cusid=request.form['cusid']
    #     username=request.form['uname']
        # firstname =request.form('fname')
        # email=request.form('email')
        # address=request.form('address')
        # work=request.form('work')
        # houseno=request.form('houseno')
        # pincode=request.form('pincode')
        # city=request.form('city')
        # distric=request.form('distric')
        # state=request.form('state')
        # file1 = request.files['image1']
        # data1 = file1.read()
        # render_file1 = render_picture(data1)
        # subject="WORKER VERFICATION"
        # msg="NOW YOU WAS HELPCENTER WORKER"
        # from .models import Data
        # data=Data.query.filter_by(cusid=cusid).first()
        # if data:
        #     flash("alredy")
        #     print("already")
        
        # else:
        #     from .import db 
        #     data =Data(cusid=cusid,username=username,firstname=firstname,houseno=houseno,address=address,work=work,data1 = data1, rendered_data1 = render_file1,email=email,pincode=pincode,state=state,city=city,distric=distric)
        #     db.session.add(data)
        #     db.session.commit()
        #     flash("Data is successfully added")
        #     message=Message(subject,sender="kiruthickkumark.20cse@kongu.edu",recipients=[email])
        #     message.body=msg
        #     mail.send(message)
        #     success ="message send"
        # return render_template("workerdata.html")
@views.route('/getinfo',methods=['GET','POST'])
def getinfo():
    if(request.method=='POST'):
        work=request.form.get('work')
        pincode=request.form.get('pincode')
        city=request.form.get('city')
        distric=request.form.get('distric')
        state=request.form.get('state')
        status="Accepted"
        new_data =Data.query.filter_by(work=work,city=city,distric=distric,state=state,status =status).all()
        if new_data:
            return redirect(f'/workers/{work}/{status}')
        else:
            flash("No services is available")
            # print("no data is w")
            return render_template('get.html',user=current_user)
    return render_template('get.html',user=current_user)
@views.route('/workers/<string:work>/<string:status>')
def pay(work,status):
    new_data =Data.query.filter_by(work=work,status=status).all()
    if new_data:
        return render_template('workers.html',new_data=new_data,user=current_user)
    
    else:
        return render_template('get.html',new_data=new_data,user=current_user)  

@views.route('/book')
def book():
    return render_template('book.html')
@views.route('/location')
def location():
    return render_template('map.html')
# @views.route('/workerdata',methods=['GET','POST'])
# def workerdata():
#     if request.method =='POST':
#         cusid=request.form.get('cusid')
#         username=request.form.get('uname')
#         firstname =request.form.get('fname')
#         email=request.form.get('email')

#         address=request.form.get('address')
#         work=request.form.get('work')
#         houseno=request.form.get('houseno')
#         pincode=request.form.get('pincode')
#         city=request.form.get('city')
#         distric=request.form.get('distric')
#         state=request.form.get('state')
#         file1 = request.files['image1']
#         data1 = file1.read()
#         render_file1 = render_picture(data1)
#         subject="WORKER VERFICATION"
#         msg="NOW YOU WAS HELPCENTER WORKER"
#         from .models import Data
#         data=Data.query.filter_by(cusid=cusid).first()
#         if data:
#             flash("alredy")
#             print("already")
#             return render_template("workerdata.html",data=current_user)
        
#         else:
#             from .import db 
#             data =Data(cusid=cusid,username=username,firstname=firstname,houseno=houseno,address=address,work=work,data1 = data1, rendered_data1 = render_file1,email=email,pincode=pincode,state=state,city=city,distric=distric)
#             db.session.add(data)
#             db.session.commit()
#             flash("Data is successfully added")
#             message=Message(subject,sender="kiruthickkumark.20cse@kongu.edu",recipients=[email])
#             message.body=msg
#             mail.send(message)
#             success ="message send"
#             return render_template("workerdata.html",success=success)
#     return render_template("workerdata.html",data=current_user)

@views.route("/workerdata")
def workerdata():
    all_data=Data.query.filter_by(username=current_user.username)
    print(current_user.username)
    return render_template("workerdata.html",user=current_user,data=all_data)
    

@views.route("/workerdataFormForm",methods=['GET','POST'])
@login_required
def workerdataForm():
    if request.method == 'POST':
        name=request.form['name']
        email=request.form['email']
        address=request.form['address']
        date=request.form['date']
        houseno=request.form['houseno']
        state=request.form['state']
        city=request.form['city']
        distric=request.form['distric']
        file1 = request.files['image1']
        data1 = file1.read()
        render_data1 = render_picture(data1)
        # phne=request.form['phne']
        username=current_user.username
        work=request.form['work']
        pincode=request.form['pincode']
        status="Pending"
        from datetime import datetime
        import datetime
        Db_date=Data.query.filter_by(date=date,status="Accepted").first()
        t_date= datetime.date.today()
        cur=datetime.datetime.strptime(date,'%Y-%m-%d')
        c_date=cur.date()
        # print(c_date)
        # if(Db_date):
        #     flash("Date is already booked!!")

        # if(c_date<t_date):
        #     flash("Enter valid datas!!")
        my_data=Data(name,email,address,date,pincode,status,username,work,houseno,state,distric,city,data1,render_data1)
        db.session.add(my_data)
        db.session.commit()
        flash("Data send to admin...Wait for Admin's response")
        return redirect(url_for('views.workerdata',user=current_user))

        return redirect(url_for('views.workerdata',user=current_user))

# admin

@views.route("/workerdataAdmin")
def workerdataAdmin():
    all_data=Data.query.all()
    return render_template("workerdataAdmin.html",data=all_data,user=current_user)

@views.route("/acceptConceptdata/<id>")
def acceptConceptdata(id):
    my_data=Data.query.get(id)
    print(my_data.email)
    subject="Worker Verification"
    msg="Your request has been accepted by Helpcenter"
    # msg1="YOUR REQUEST HAS BEEEN ACCPECTED BY HELPHERCENTER"
    # msg=my_data.email,my_data.name
    message=Message(subject,sender="kiruthickkumark.20cse@kongu.edu",recipients=[my_data.email])
    # m=Message(subject,sender="kiruthickkumark.20cse@kongu.edu",recipients="kavinkirushnar.20cse@kongu.edu")
    message.body=msg
    # m.body=msg1
    mail.send(message)
    success ="message send"
    
    my_data.status="Accepted"
    db.session.commit()
    return redirect(url_for('views.workerdataAdmin',user=current_user,success=success))

@views.route("/rejectConceptdata/<id>")
def rejectConceptdata(id):
    my_data=Data.query.get(id)
    subject="Worker Verification"
    msg="Your request has been Rejected by Helpcenter"
    # msg=my_data.email,my_data.name
    message=Message(subject,sender="kiruthickkumark.20cse@kongu.edu",recipients=[my_data.email])
    message.body=msg
    mail.send(message)
    success ="message send"
    
    my_data.status="Rejected"
    db.session.commit()
    return redirect(url_for('views.workerdataAdmin',user=current_user,success=success))

@views.route("/cancelConceptdata/<id>")
def cancelConceptdata(id):
    my_data=Data.query.get(id)
    my_data.status="Canceled"
    db.session.commit()
    return redirect(url_for('views.workerdata',user=current_user))

@views.route("/update",methods=['GET','POST'])
def update():
        if request.method == 'POST':
            name=request.form['name']
            status=request.form['status']
            email=request.form['email']
            if(name==current_user.username):
                
                # position = request.form['position']
                #  conn.execute('UPDATE items SET done = 0 WHERE id = ?', (id,))
                employee = Data.query.filter_by(id=1).all()
                name=name
                email=email
                address=employee.address
                date=employee.date
                houseno=employee.houseno
                state=employee.state
                city=employee.city
                pincode=employee.pincode
                username=employee.username
                work=employee.work
                distric=employee.distric
                # file1 = employee.file1
                data1 = employee.data1
                render_data1 = employee.render_data1
                status=status
                db.session.delete(employee)
                db.session.commit()
                print(email)
                        


                employee = Data(name,email,address,date,pincode,status,username,work,houseno,state,distric,city,data1,render_data1)
    
                db.session.add(employee)
                db.session.commit()
                return render_template('update.html',user=current_user,employee=current_user)
            print(current_user.username)
            print("hello")
            return render_template('update.html', user=current_user,employee=current_user)
        return render_template('update.html', user=current_user,employee=current_user)
