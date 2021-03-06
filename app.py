from flask import Flask,render_template,request,make_response,abort, redirect, url_for,session,escape
from temp_nltk import url_rize
import pdfkit
import re

app = Flask(__name__)
app.secret_key = 'any random string'


@app.route('/')
def index():
	return render_template('index1.html')

@app.route('/success',methods=['GET','POST'])
def analyze():
	if request.method == 'POST':
		session['key'] = 'Key Points'
		rawtext = request.form['raw']
		typesum = request.form['typesum']
		protext = url_rize(rawtext,typesum)
		session['title'] = protext[1]
		session['para'] = protext[0]
		session['lists'] = protext[2]
		rend = render_template('index2.html',rawe=protext[0],title=protext[1],lists=protext[2],key=session['key'])
		return rend

@app.route('/indexnew')
def indexnew():
	config = pdfkit.configuration(wkhtmltopdf='./bin/wkhtmltopdf')
	render = render_template('pdf.html',para=session['para'],title=session['title'],lists=session['lists'],key=session['key'])
	pdf = pdfkit.from_string(render, False, configuration=config)
	response = make_response(pdf)
	response.headers['Content-Type'] = 'application/pdf'
	response.headers['Content-Disposition'] = 'attachment; filename=summary.pdf'
	return (response)
@app.route('/pdf',methods=['GET','POST'])
def pdf():
	if request.method == 'POST':
	
		return (redirect(url_for('indexnew')))


if __name__ == '__main__':
	app.run()
