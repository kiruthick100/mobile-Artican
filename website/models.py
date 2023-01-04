
# from . import db
# from flask_login import UserMixin

# class bookingdb(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name=db.Column(db.String(100))
#     email = db.Column(db.String(100))
#     address = db.Column(db.String(100))
#     phne=db.Column(db.String(30))
#     package=db.Column(db.String(50))
#     date=db.Column(db.String(50))
#     username=db.Column(db.String(100))
#     status=db.Column(db.String(100))
#     def __init__(self,name,email,address,phne,date,username,status):
#         self.name = name
#         self.email = email
#         self.address = address
#         self.phne = phne
#         self.date = date
#         self.username=username
#         self.status=status
       
# class galleryImageUpload(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     filename = db.Column(db.String(500))
#     final_img = db.Column(db.Text(4294000000), nullable=False)

#     def __init__(self,name,final_img):
#         self.filename=name
#         self.final_img=final_img

# class User(db.Model, UserMixin):
#     id=db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(20), nullable=False, unique=True)
#     password = db.Column(db.String(20), nullable=False)
#     usertype = db.Column(db.String(20), nullable=False)

# class Data(db.Model):

#     id=db.Column(db.Integer,primary_key=True)
#     # cusid=db.Column(db.String,unique=True)
#     name=db.Column(db.String(150))
#     # firstname=db.Column(db.String(150))
#     email=db.Column(db.String(150))
#     address=db.Column(db.String(200))
#     # houseno=db.Column(db.String(100))
#     work=db.Column(db.String(100))
#     pincode=db.Column(db.String(100))
#     # state=db.Column(db.String(100))
#     # city=db.Column(db.String(100))
#     # distric=db.Column(db.String(100))
#     date=db.Column(db.String(50))
#     username=db.Column(db.String(100))
#     status=db.Column(db.String(100))

    
#     # data1 = db.Column(db.LargeBinary, nullable=False)
#     # rendered_data1 = db.Column(db.Text, nullable=False)
#     def __init__(self,name,email,address,date,pincode,status,username,work):
#         self.name=name
#         self.pincode=pincode
#         self.work=work
#         # self.state=state
#         # self.city=city 
#         # self.distric=distric
#         # self.houseno=houseno
#         # self.cusid=cusid
#         self.email = email
#         self.address = address
#         self.username=username
#         # self.data1=data1 
#         # self.rendered_data1=rendered_data1
#         self.date=date
#         self.status=status

       
       
from . import db
from flask_login import UserMixin

class bookingdb(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(100))
    email = db.Column(db.String(100))
    address = db.Column(db.String(100))
    phne=db.Column(db.String(30))
    date=db.Column(db.String(50))
    username=db.Column(db.String(100))
    status=db.Column(db.String(100))
    wemail=db.Column(db.String(100))
    def __init__(self,name,email,address,phne,date,username,status,wemail):
        self.name = name
        self.email = email
        self.address = address
        self.phne = phne
        self.date = date
        self.username=username
        self.status=status
        self.wemail=wemail
       
class galleryImageUpload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(500))
    final_img = db.Column(db.Text(4294000000), nullable=False)

    def __init__(self,name,final_img):
        self.filename=name
        self.final_img=final_img

class User(db.Model, UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False)
    usertype = db.Column(db.String(20), nullable=False)

class Data(db.Model):

    id=db.Column(db.Integer,primary_key=True)
    # cusid=db.Column(db.String,unique=True)
    name=db.Column(db.String(150))
    # firstname=db.Column(db.String(150))
    email=db.Column(db.String(150))
    address=db.Column(db.String(200))
    houseno=db.Column(db.String(100))
    work=db.Column(db.String(100))
    pincode=db.Column(db.String(100))
    state=db.Column(db.String(100))
    city=db.Column(db.String(100))
    distric=db.Column(db.String(100))
    date=db.Column(db.String(50))
    username=db.Column(db.String(100))
    status=db.Column(db.String(100))

    
    data1 = db.Column(db.LargeBinary, nullable=False)
    render_data1 = db.Column(db.Text, nullable=False)
    def __init__(self,name,email,address,date,pincode,status,username,work,houseno,state,distric,city,data1,render_data1):
        self.name=name
        self.pincode=pincode
        self.work=work
        self.state=state
        self.city=city 
        self.distric=distric
        self.houseno=houseno
        # self.cusid=cusid
        self.email = email
        self.address = address
        self.username=username
        self.data1=data1 
        self.render_data1=render_data1
        self.date=date
        self.status=status

       