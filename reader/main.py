import requests
from flask import Flask, jsonify, request
import json
import base64


app = Flask(__name__)
  
@app.route("/")
def home():
	return "Hello from the other side  !!!"

@app.route('/callPrediction', methods=['GET', 'POST'])
def callPrediction():
	if request.method == 'GET':
		fileName = request.args.get('fileName')
	else :
		fileName = 'jazz.00001.wav'
	print("********************** File name : " + fileName)
	url = 'http://0.0.0.0:5050/prediction/'	
	fileToPredect = open(fileName, 'rb')	
	fileEncoded = base64.b64encode(fileToPredect.read())
	headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
	req = requests.post(url, json={"file": fileEncoded.decode("utf-8")}, headers=headers)
	return (req.text)	

    

if __name__ == '__main__':
   app.run(debug=True, port=5051, host='0.0.0.0', threaded=True)
   
   
