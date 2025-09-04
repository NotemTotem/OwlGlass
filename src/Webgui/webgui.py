from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return("A webpage lives here. Please go away!")

if __name__ == "__main__":
    app.run(debug=True,port=5000)