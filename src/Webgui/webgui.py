from flask import Flask,render_template,request
from Interfacer import interfacer
app = Flask(__name__)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('root/404.html'),404

@app.route('/',methods=["GET","POST"])
def index():
    return render_template('index.html')


@app.route('/toolscripts/accountfinder',methods=["POST"])
def accountfinder():
    if request.method == "POST":
        form = request.form
        email = form.get("email")
        response = interfacer.find_accounts(email,"email")
        if response:
            return response,200


if __name__ == "__main__":
    app.run(debug=True,port=5000)