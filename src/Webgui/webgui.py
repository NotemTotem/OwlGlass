from flask import Flask,render_template

app = Flask(__name__)

#Global csrf protection
from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect(app)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('root/404.html'),404

@app.route('/',methods=["GET","POST"])
def index():
    return render_template('index.html')


@app.route('/toolscripts/accountfinder',methods=["POST"])

if __name__ == "__main__":
    app.run(debug=True,port=5000)