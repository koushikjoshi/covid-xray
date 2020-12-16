from flask import Blueprint,jsonify,request,Response,redirect,render_template
from werkzeug.utils import secure_filename
from . import db
from .models import mlInput,dataInput,FileMaker1
import urllib
import cv2
import tensorflow as tf
import numpy as np
from PIL import Image
from skimage import io
from skimage import img_as_ubyte
main = Blueprint("main", __name__ ,static_folder="../frontend/build", static_url_path="/")
CATEGORIES = ["covid positive", "not covid positive"]
new_model = tf.keras.models.load_model("final_model.model")
def prepare(filepath):
    IMG_SIZE = 224
    image = img_as_ubyte(io.imread(filepath))
    image = np.asarray(image, dtype="uint8")
    new_array = cv2.resize(image, (IMG_SIZE, IMG_SIZE))
    
    print(new_array.shape)
    if len(new_array.shape) > 2 and image.shape[2] == 4:
        new_array = cv2.cvtColor(new_array, cv2.COLOR_BGRA2RGB)
    return new_array.reshape(-1, IMG_SIZE, IMG_SIZE, 3)


@main.route('/upload',methods=['GET','POST'])
def upload():

    pic = request.files['pic']
    if not pic:
        return 'No pic uploaded!', 400

    filename = secure_filename(pic.filename)
    print("pic:",pic)
    mimetype = pic.mimetype
    if not filename or not mimetype:
        return 'Bad upload!', 400
    
    img = FileMaker1( img_name=filename,img=pic.read(), mimetype=mimetype)
    db.session.add(img)
    db.session.commit()
    print()
    prediction = new_model.predict([prepare('http://127.0.0.1:5000/'+str(img.img_name))])
    result = CATEGORIES[int(prediction[0][0])]
    img = 'http://127.0.0.1:5000/'+str(img.img_name)


    return render_template("result.html", result=result, url=img )
   

@main.route("/api")
def imgs():
    imgs_list = FileMaker1.query.all()
    images = []
    for image in imgs_list:
        images.append({"name":image.img_name, "image_id":image.id, "url":"http://127.0.0.1:5000/"+str(image.img_name)})
    return jsonify({"images":images})

@main.route('/<int:id>')
def get_img(id):

    img = FileMaker1.query.filter_by(id=id).first()
    
    print(img.mimetype)
    if not img:
        return 'Img Not Found!', 404
  
   
    return Response(img.img,  mimetype=img.mimetype)
@main.route('/<string:name>')
def img_api(name):
    img = FileMaker1.query.filter_by(img_name= name).first()
    if not img:
        return 'Img Not Found!', 404
  
   
    return Response(img.img,  mimetype=img.mimetype)

@main.route('/daata')
def daata():
    daata_list = mlInput.query.all()
    daata = []

    for data in daata_list:
        daata.append({"input1": data.input1, "input2": data.input2})


    return jsonify({'daata': daata})

@main.route('/add_data',methods=["POST"])
def add_data():
    ml_data = request.get_json()

    new_data = mlInput(input1=ml_data['input1'], input2=ml_data['input2'])

    db.session.add(new_data)
    db.session.commit()

    return "done",201

@main.route('/deleteAllData')
def remove():
    db.session.query(FileMaker1).delete()
    db.session.commit() 
    return "All entries deleted", 200

@main.route("/")
def index():
    return render_template("test.html")