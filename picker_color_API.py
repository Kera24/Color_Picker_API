from flask import Flask, jsonify
from urllib.request import urlretrieve
from urllib.request import urlopen
import cv2
import numpy as np
from colormap import rgb2hex
import urllib.request

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hi there, My name is Raj Kumar Sah.'

@app.route('/picker/')
@app.route('/picker/src=<path:url>')

def color_picker(url):
    url=url.replace(' ','%20')
    resp = urllib.request.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    anr = (image[:100,:,0]).flatten()#B
    anr_dom = np.bincount(anr).argmax()
    # print(anr_dom)

    ang = (image[:100,:,1]).flatten()#G
    ang_dom = np.bincount(ang).argmax()

    anb = (image[:100,:,2]).flatten()#R
    anb_dom = np.bincount(anb).argmax()

    data = np.reshape(image, (-1,3))
    data = np.float32(data)

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    flags = cv2.KMEANS_RANDOM_CENTERS
    compactness,labels,centers = cv2.kmeans(data,1,None,criteria,10,flags)

    bgr = centers[0].astype(np.int32)



    result = {
        'logo_border': rgb2hex(int(anb_dom),int(ang_dom),int(anr_dom)),
        'dominant_color': rgb2hex(bgr[2],bgr[1],bgr[0])
    }

    # return url

    return jsonify(result)


if __name__=='__main__':
    app.run(debug=True)