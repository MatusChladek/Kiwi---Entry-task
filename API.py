from flask import Flask
from flask import request,jsonify

from requests_html import HTMLSession
from datetime import datetime

s = HTMLSession()

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True

@app.route('/ping')
def ping():
  return 'pong'


from flask import request, jsonify
import connections
import https_req

@app.route('/search', methods=['GET'])
def search():
  date_from = request.args.get('date_from')
  #date_to = request.args.get('date_to')
  src = request.args.get('src')
  dst = request.args.get('dst')


  results = https_req.return_route(src,dst,date_from)
  return jsonify(results)

if __name__ == '__main__':
   app.run()





