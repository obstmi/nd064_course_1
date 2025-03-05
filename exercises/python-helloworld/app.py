import json, logging
from flask import Flask
app = Flask(__name__)

# Lösung 1 für den Start mittels 'flask run': Entferne vorhandene Flask-Logger-Handler
# for handler in app.logger.handlers:
#     app.logger.removeHandler(handler)

# Lösung 2: für den Start mittels 'flask run': Setze das Logging mit basicConfig so frühzeitig, so dass Flask diese Konfigutation übernimmt
# logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
# logging.basicConfig(filename='app.log',level=logging.DEBUG)

@app.route("/")
def hello():
    app.logger.debug('Main request successfull')
    return "Hello World!"

@app.route('/status')
def status():
    response = app.response_class(
            response=json.dumps({"result":"OK - healthy"}),
            status=200,
            mimetype='application/json'
    )
    return response

@app.route('/metrics')
def metrics():
    response = app.response_class(
            response=json.dumps({"status":"success","code":0,"data":{"UserCount":140,"UserCountActive":23}}),
            status=200,
            mimetype='application/json'
    )
    return response

if __name__ == "__main__":
    # Stream logs to a file, and set the default log level to DEBUG
    # => klappt nur, bei Start über 'python3 app.py', da die Logging-Instanz vor der Flask-Initialisierung gesetzt wird
    logging.basicConfig(filename='app.log',level=logging.DEBUG)  
    app.run(host='127.0.0.1') # anstatt host='0.0.0.0'
