from flask import Flask
from requests_html import HTMLSession
from datetime import datetime
from flask import request, jsonify, render_template
import connections
import https_req
from forms import SearchForm
from flask_wtf import Form

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['SECRET_KEY'] = 'any secret string'

# homepage render

@app.route('/')
def template_test():
   return render_template('template.html', welcome='Hello world')


@app.route('/a', methods=['GET', 'POST'])
def index():
    search = SearchForm(request.form)
    #if request.method == 'POST':
    #    return search_results(search)
 
    return render_template('index.html', form=search)


@app.route('/ping')
def ping():
  return 'pong'

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