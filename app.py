import configparser, jinja2, requests
from flask import Flask, jsonify
from flask_mail import Mail, Message

app = Flask(__name__)

@app.route('/')
def index():
    data = requests.get('http://52.187.51.158:8082/mongodb/boschxdk03/latestdata').json()
    return jsonify({key:value for key,value in data.items() if key in ['noiselevel','temperature','humidity','millilux']})

@app.route('/alert')
def alert():
    config = configparser.ConfigParser()
    config.read('secret.ini')

    app.config['MAIL_SERVER']   = config['email'].get('server')
    app.config['MAIL_PORT']     = config['email'].getint('port')
    app.config['MAIL_USERNAME'] = config['email'].get('sender')
    app.config['MAIL_PASSWORD'] = config['email'].get('password')
    app.config['MAIL_USE_SSL']  = config['email'].getboolean('ssl')
    app.config['MAIL_USE_TLS']  = config['email'].getboolean('tls')

    mailer = Mail(app)

    data = {
            "subject": "[Alert] Please clean up!",
            "message": "Your trap is full. Please clean it up ASAP!"
            }

    mail = Message(
            subject = data['subject'],
            recipients = config['email'].get('recipients').split(','),
            sender = config['email'].get('sender')
            )

    template = jinja2.Environment(
            trim_blocks = True,
            lstrip_blocks = True,
            autoescape = True,
            loader = jinja2.FileSystemLoader('templates')
            ).get_template('email.html.j2')

    mail.html = template.render(data)

    mailer.send(mail)
    return jsonify({"SENT": "OK"})

