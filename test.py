from flask import Flask,make_response


app = Flask(__name__)

@app.route('/set')
def setCookie():
    res = make_response('Setting cookie')
    res.set_cookie('token','jwtt')
    return res

@app.route('/get')
def getCookie():
    req = 
    return ''

if __name__ == '__main__':
    app.run(debug = True)