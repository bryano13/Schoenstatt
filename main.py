#!/usr/bin/python3
from flask import Flask, render_template
from flask import request
from flask_mail import Mail, Message
import json

from flask import jsonify

app = Flask(__name__)

with open("out_file.txt", "r") as my_file:
    tienda = my_file.read()
d = {}
for i in range(len(tienda)):
    line_list = tienda.split("\n")
for index, line in enumerate(line_list):
    if "_" in line:
        item_list = line.split("_")
        for index, col in enumerate(item_list):
            if col == item_list[-1]:
                col = item_list[-1][:-4]
                price_list = col.split("-")
                item_list[index] = ".".join(price_list)
            elif "-" in col:
                col_list = col.split("-")
                item_list[index] = " ".join(col_list)
            item_list[index] = str(item_list[index].capitalize())
        if len(line) <= 1:
            pass
        else:
            d[line] = item_list
sort_d = sorted(d.items(), key=lambda x: x[1][-1], reverse=False)

# creating a list of pictures for the slides section on home.html
with open("slides.txt", "r") as my_slides:
    slides = my_slides.read()
pic_list = []
for i in range(len(slides)):
    p_list = slides.split("\n")
    pic_list = p_list[:-1]


with open("sample.json", "w") as sampleFile:
    json.dump(pic_list, sampleFile)


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'schoenstatt.cali18@gmail.com'
app.config['MAIL_PASSWORD'] = 'Virgen123!'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)


@app.route('/hello', methods=['GET', 'POST'])
def hello():

    # POST request
    if request.method == 'POST':
        print('Incoming..')
        print(request.get_json())  # parse as JSON
        return 'OK', 200

    # GET request
    else:
        message = {'greeting': 'Hello from Flask!'}
        return jsonify(message)  # serialize and use JSON headers


@app.route('/test')
def test_page():
    # look inside `templates` and serve `index.html`
    return render_template('sample.html')


@app.route('/tienda', methods=['GET', 'POST'])
def tienda1():
    return render_template('tienda.html', my_list=sort_d, lista=line_list)


@app.route('/about_us', methods=['GET', 'POST'])
def about():
    return render_template('about_us.html')


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        email = request.form["email"]
        texto = request.form["text"]
        name = request.form["first"]
        last = request.form["last"]
        phone = request.form["phone"]
        msg = Message(
            'Consulta en página de Schoenstatt',
            sender='schoenstatt.cali18@gmail.com',
            recipients=['schoenstatt.cali18@gmail.com',
                        'erileju123@gmail.com',
                        'erileju123@yahoo.es',
                        'mlyla56@hotmail.com',
                        'clapaorozvi@gmail.com'])
        msg.body = "> email: {}\n> telefono: {}\n> nombre: {} {}\n> mensaje: {}\n".format(
            email, phone, name, last, texto)
        mail.send(msg)
        return render_template(
            'home.html', success="Enviado", pic_list=pic_list)
    return render_template('home.html', pic_list=pic_list)


if __name__ == "__main__":
    app.run(debug=True)
