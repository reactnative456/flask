import numpy as np
from flask import Flask, request, jsonify
from PIL import Image
import io
import os
from mods.detect_age_from_ID import calculate_age


app = Flask(__name__)
@app.route('/detect_age', methods=['POST'])
def process_image_api():
    # Get the image file from the request
    file = request.files['image']

    # Read the image file and convert it to a numpy array
    img = np.array(Image.open(io.BytesIO(file.read())))

    # process the image

    age = calculate_age(img)
    try:
        os.remove('temp.png')
    except:
        pass

    if age == 0:
        final_output = {'ID verified':False,'Status':'Fake ID detected' ,'Age':None}    
    elif age == -1:
        final_output = {'ID verified':False,'Status':'Card is invalid' ,'Age':None}
    elif age == -2:
        final_output = {'ID verified':False,'Status':'Card is expired' ,'Age':None}
    else:
        final_output = {'ID verified':True,'Status':'Age found in card' ,'Age':int(age)}

    return jsonify(final_output)

@app.route('/about', methods=['GET'])
def about_image_api():
    return jsonify({"about":'Age detection api by REX'})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)