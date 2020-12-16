from . import db

class mlInput(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    input1 = db.Column(db.String(50))
    input2 = db.Column(db.String(50))

class dataInput(db.Model):
     id = db.Column(db.Integer, primary_key = True)
     input3 = db.Column(db.String(50))
     input4 = db.Column(db.String(50))

# class FileMaker(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     img_name = db.Column(db.String(50))
#     img = db.Column(db.String(50), unique=True)
#     mimetype = db.Column(db.String(500))
class FileMaker1(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img_name = db.Column(db.String(50))
    img = db.Column(db.String(50), unique=True)
    mimetype = db.Column(db.String(500))