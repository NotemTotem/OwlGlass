from flask import Flask,render_template,request,make_response
from Interfacer import interfacer
from forms import AccountfinderForm
app = Flask(__name__)
#Disabling csrf protection as this is a local webserver
app.config['WTF_CSRF_ENABLED'] = False

@app.errorhandler(404)
def page_not_found(e):
    return render_template('root/404.html'),404

@app.route('/',methods=["GET","POST"])
def index():
    return render_template('index.html')


@app.route('/toolscripts/accountfinder',methods=["GET","POST"])
def accountfinder():
    form = AccountfinderForm()
    #Validating form upon submission
    if form.validate_on_submit():
        response = make_response('1234')    
        response.headers['HX-Trigger'] = 'Successful'
        print("target:",form.target.data)
        print("target_type",form.target_type.data)
        return response


    # if request.method == "POST":
    #     form = request.form
    #     email = form.get("email")
    #     response = interfacer.find_accounts(email,"email")
    #     if response:
    #         return response,200
    return render_template('toolscripts/accountfinder.html',form=form)
@app.route('/test')
def test():
    return "2223232132"
if __name__ == "__main__":
    app.run(debug=True,port=5000)