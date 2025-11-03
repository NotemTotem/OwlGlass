from flask import Flask,render_template,request,make_response
from Interfacer import interfacer
from forms import AccountfinderForm, dnslookupForm, port_scanner_form, fuzzer_form
app = Flask(__name__)
#Disabling csrf protection as this is a local webserver
app.config['WTF_CSRF_ENABLED'] = False

@app.errorhandler(404)
def page_not_found(e):
    return render_template('root/404.html'),404

@app.route('/',methods=["GET","POST"])
def index():
    return render_template('index.html')


@app.route('/about',methods=["GET"])
def about():
    return render_template('about.html')


@app.route('/toolscripts/accountfinder',methods=["GET","POST"])
def accountfinder():
    form = AccountfinderForm()
    #Validating form upon submission
    if form.validate_on_submit():
        target = form.target.data
        cap = form.cap.data
        response = interfacer.find_accounts(target,cap)
        response_formatted = []
        for i in response:
            response_formatted.append(i.replace('\n','<br>'))
        response_formatted = ''.join(response_formatted)
        return render_template('toolscripts/accountfinder.html',form=form,response=response_formatted)


    # if request.method == "POST":
    #     form = request.form
    #     email = form.get("email")
    #     response = interfacer.find_accounts(email,"email")
    #     if response:
    #         return response,200
    return render_template('toolscripts/accountfinder.html',form=form)

@app.route('/toolscripts/dnslookup', methods=["GET", "POST"])
def dnslookup(): #oiafnhoiawhfoihaw
    form = dnslookupForm()
    if form.validate_on_submit():
        target = form.target.data
        dns_record_types = form.my_choices.data
        response = interfacer.dns_lookup(target, dns_record_types)
        response_formatted = []
        for i in response:
            response_formatted.append(i.replace('\n','<br>'))
        response_formatted = ''.join(response_formatted)


        return render_template('toolscripts/dnslookup.html', form=form, response=response_formatted)
    return render_template('toolscripts/dnslookup.html', form=form)


@app.route('/toolscripts/portscan', methods=["GET", "POST"])
def port_scanner():
    form = port_scanner_form()

    if form.validate_on_submit():
        target= form.target.data
        ports= form.ports.data
        print(target, ports)
        response = interfacer.scan_ports(target, ports)
        response_formatted = []
        for i in response:
            response_formatted.append(i.replace('\n','<br>'))
        response_formatted = ''.join(response_formatted)

        return render_template ('toolscripts/portscan.html',form=form,response=response_formatted)

    return render_template('toolscripts/portscan.html', form=form)

@app.route('/toolscripts/subdomainfuzz', methods=["GET", "POST"])
def sub_fuzzer():
    form = fuzzer_form()

    if form.validate_on_submit():
        target = form.target.data
        recursion_depth = form.depth.data
        port= form.port.data
        print(target, port)
        response = interfacer.fuzz_subs(target, recursion_depth, port)
        response_formatted = []
        for i in response:
            response_formatted.append(i.replace('\n','<br>'))
        response_formatted = ''.join(response_formatted)

        return render_template ('toolscripts/subdomainfuzz.html',form=form,response=response_formatted)

    return render_template('toolscripts/subdomainfuzz.html', form=form)

@app.route('/toolscripts/vhostfuzz', methods=["GET", "POST"])
def vhost_fuzzer():
    form = fuzzer_form()

    if form.validate_on_submit():
        target = form.target.data
        recursion_depth = form.depth.data
        port= form.port.data
        print(target, port)
        response = interfacer.fuzz_vhosts(target, recursion_depth, port)
        response_formatted = []
        for i in response:
            response_formatted.append(i.replace('\n','<br>'))
        response_formatted = ''.join(response_formatted)

        return render_template ('toolscripts/vhostfuzz.html',form=form,response=response_formatted)

    return render_template('toolscripts/vhostfuzz.html', form=form)

@app.route('/toolscripts/directoryfuzz', methods=["GET", "POST"])
def dir_fuzzer():
    form = fuzzer_form()

    if form.validate_on_submit():
        target = form.target.data
        recursion_depth = form.depth.data
        port= form.port.data
        print(target, port)
        response = interfacer.fuzz_dirs(target, recursion_depth, port)
        response_formatted = []
        for i in response:
            response_formatted.append(i.replace('\n','<br>'))
        response_formatted = ''.join(response_formatted)

        return render_template ('toolscripts/directoryfuzz.html',form=form,response=response_formatted)

    return render_template('toolscripts/directoryfuzz.html', form=form)


@app.route('/lessons/introduction')
def lesson_introduction():
    return render_template('lessons/introduction_lesson.html')
@app.route('/lessons/accountfinder')
def lesson_accountfinder():
    return render_template('lessons/accountfinder_lesson.html')
@app.route('/lessons/portscan')
def lesson_portscan():
    return render_template('lessons/port_scanning_lesson.html')
@app.route('/lessons/subfuz')
def lesson_subvfuz():
    return render_template('lessons/subdomain_vhost_lesson.html')
@app.route('/lessons/dirfuzz')
def lesson_dirfuzz():
    return render_template('lessons/directory_fuzzing_lesson.html')
@app.route('/lessons/dns')
def lesson_dns():
    return render_template('lessons/dns_lesson.html')
@app.route('/lessons/whereto')
def lesson_whereto():
    return render_template('lessons/whereto_lesson.html')
@app.route('/test')
def test():
    return "2223232132"
if __name__ == "__main__":
    app.run(debug=True,port=5000)
