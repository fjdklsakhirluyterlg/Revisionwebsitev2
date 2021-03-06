# import cv2
import math
from flask import Flask, render_template, url_for, request, redirect, send_from_directory, send_file, flash, jsonify, Blueprint, Response
from flask_sqlalchemy import SQLAlchemy
import requests
import smtplib
import ssl
from email.message import EmailMessage
from itertools import permutations
import os
import random
from dataclasses import dataclass
from math import asin, cos, radians, sin, sqrt, tan
from bs4 import BeautifulSoup
from flask_restful import Resource, Api
from datetime import datetime
# from ctypes import cdll

app = Flask(__name__)
api = Api(app)

@app.errorhandler(500)
def internal_server_error(e):
    return f"Something went wrong : {e}", 500

@app.errorhandler(405)
def method_not_allowed(e):

    if request.path.startswith('/api/'):
        
        return jsonify(message="Method Not Allowed"), 405
    else:
        return "wrong method!"

@app.errorhandler(404)
def page_not_found(e):
    return f"Sorry could not find {request.path}"

# what is url_map

# @app.add_template_filter()

blogs = Blueprint('blogs',__name__)
app.register_blueprint(blogs)

DB_NAME = "database.db"

app.config['SQLALCHEMY_DATABASE_URI'] =f'sqlite:///{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'there'}

api.add_resource(HelloWorld, '/api/test')

class GBPTOEUR(Resource):
    def get(self):
        x = get_ecenomic_stuff()[0]
        return {'GBP': x}

api.add_resource(GBPTOEUR, '/api/convert/EURTOGBP')

class ftse100(Resource):
    def get(self):
        x = get_ecenomic_stuff()[1]
        return {'FTSE100': x}

api.add_resource(ftse100, '/api/ecenomics/ftse100')

class APIrickroll(Resource):
    def get(self):
        return {'Rick astley': 'Never gonna give you up'}

api.add_resource(APIrickroll, '/api/test/dQw4w9WgXcQ')

class Banana(Resource):
    def get(self):
        return {'food': {'banana': 'yellow', 'chicken': 'meat'}, 'cities': ['london', 'new york', 'shanghai', 'dehli']}

api.add_resource(Banana, '/api/test/food')

class Randomz(Resource):
    def get(self):
        def randoms():
            r = lambda: random.randint(0,255)
            return ['#%02X%02X%02X' % (r(),r(),r())]
        
        def fortune():
            list = ['You will make at least 5 pounds', 'You will watch mr beast in the next week', 'You will quit your job', 'Your next phone will be able to run Genshin impact']
            return random.choice(list)
        
        def fact():
            list = ['Take an angle A, find out what sin(A)^2 + cos(A)^2 is', 'There are more than 6 million parts in an A380', 'Francium is the most reactive element in the world', 'Jeff Bezos could but 2 million tesla model y', 'Japan has the highest debt to GDP ratio in the world with 234%', 'Monaco should score 1.04 on the Human Development Index (HDI), a scale from 0 - 1']
            return random.choice(list)
        
        x = random.randint(0 ,1000)
        y = randoms()
        z = fortune()
        a = fact()

        return {'number': x, 'hex colour': y, 'fortune': z, 'fact': a}

api.add_resource(Randomz, '/api/random')

class top_bbc_news(Resource):
    def get(self):
        lst = get_top_bbc_news()
        link = get_top_bbc_links()
        res_dct = {i + 1: {'headline': lst[i], 'link': f"https://www.bbc.co.uk{link[i]}"} for i in range(0, len(lst))}
        return res_dct

api.add_resource(top_bbc_news, "/api/news/bbc/top")

def get_ecenomic_stuff():
    stuff = []
    # GBP TO EUR
    URL = "https://www.bbc.co.uk/news/topics/cx250jmk4e7t/pound-sterling-gbp"
    response = requests.get(URL)

    soup = BeautifulSoup(response.content, "html.parser")
    result = soup.find_all("div", class_="gel-paragon nw-c-md-currency-summary__value")
    stuff.append(result[0].text)

    # FTSE 100

    URL2 = "https://www.bbc.co.uk/news/topics/c9qdqqkgz27t/ftse-100"
    response2 = requests.get(URL2)

    soup2 = BeautifulSoup(response2.content, "html.parser")
    result2 = soup2.find_all("div", class_="gel-paragon nw-c-md-market-summary__value")
    stuff.append(result2[0].text)

    # S&P 500
    URL3 = "https://www.bbc.co.uk/news/topics/c4dldd02yp3t/sp-500"
    response3 = requests.get(URL3)

    soup3 = BeautifulSoup(response3.content, "html.parser")
    result3 = soup3.find_all("div", class_="gel-paragon nw-c-md-market-summary__value")
    stuff.append(result3[0].text)

    # GOOGLE FINANCE SCRAPING AAPL
    URL4 = "https://www.google.com/finance/quote/AAPL:NASDAQ"
    response4 = requests.get(URL4)

    soup4 = BeautifulSoup(response4.content, "html.parser")
    result4 = soup4.find_all("div", class_="YMlKec fxKbKc")
    stuff.append(result4[0].text)

    # GOOGLE FINANCE TSLA

    URL5 = "https://www.google.com/finance/quote/TSLA:NASDAQ"
    response5 = requests.get(URL5)

    soup5 = BeautifulSoup(response5.content, "html.parser")
    result5 = soup5.find_all("div", class_="P6K39c")
    stuff.append(result5[0].text)

    return stuff

def get_user_ip_address():
    if 'X-Forwarded-For' in request.headers:
        ip_address = str(request.headers['X-Forwarded-For'])
    else:
        ip_address = str(request.environ.get('HTTP_X_REAL_IP',
                         request.remote_addr))

    if ip_address == '127.0.0.1':
        ip_address = requests.get('http://ipecho.net/plain')
        if ip_address.status_code != 200:
            ip_address = requests.get('http://ip.42.pl/raw')
        ip_address = ip_address.text
    ip_address = ip_address.split(",")[0]
    return ip_address

def get_loc_from_ip(ip):
    x = requests.get(f"https://ipinfo.io/{ip}")
    a = x["city"]
    b = x["region"]
    c = x["country"]
    d = x["loc"]
    e = x["org"]
    f = x["postal"]
    
    z = [a, b, c, d, e, f]
    return z
    
    

class Vector:

  def __init__(self, x, y, z):
    self.x = x
    self.y = y
    self.z = z

  def magnitude(self):

    return sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

  def __add__(self, V):

    return Vector(self.x + V.x, self.y + V.y, self.z + V.z)

  # Method to subtract 2 Vectors
  def __sub__(self, V):

    return Vector(self.x - V.x, self.y - V.y, self.z - V.z)

  # Method to calculate the dot product of two Vectors
  def __xor__(self, V):

    return self.x * V.x + self.y * V.y + self.z * V.z

  # Method to calculate the cross product of 2 Vectors
  def __mul__(self, V):

    return Vector(self.y * V.z - self.z * V.y,
          self.z * V.x - self.x * V.z,
          self.x * V.y - self.y * V.x)

  # Method to define the representation of the Vector
  def __repr__(self):

    out = str(self.x) + "i "

    if self.y >= 0:
      out += "+ "
    out += str(self.y) + "j "
    if self.z >= 0:
      out += "+ "
    out += str(self.z) + "k"

    return out
@dataclass
class Position:
    name: str
    lon: float = 0.0
    lat: float = 0.0

    def distance_to(self, other):
        r = 6371  # Earth radius in kilometers
        lam_1, lam_2 = radians(self.lon), radians(other.lon)
        phi_1, phi_2 = radians(self.lat), radians(other.lat)
        h = (sin((phi_2 - phi_1) / 2)**2
             + cos(phi_1) * cos(phi_2) * sin((lam_2 - lam_1) / 2)**2)
        return 2 * r * asin(sqrt(h))


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)

db.create_all()

class Emaillist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    emailadd = db.Column(db.String(1000), unique=True)

class Readinglist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    list = db.Column(db.String(1000))
    author = db.Column(db.String(1000))
    summary = db.Column(db.String(1000), unique=True)
    pages = db.Column(db.Integer)

class Cars(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    brand = db.Column(db.String(150))
    top_speed = db.Column(db.Integer)
    horsepower = db.Column(db.Integer)
    length = db.Column(db.Integer)
    width = db.Column(db.Integer)
    rating = db.Column(db.Float)

db.create_all()

class Tag(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(20))
    @property
    def serialize(self):
        return {
        'id': self.id,
        'name': self.name     
        }

tag_blog = db.Table('tag_blog',
    db.Column('tag_id',db.Integer,db.ForeignKey('tag.id'), primary_key=True),
    db.Column('blog_id', db.Integer,db.ForeignKey('blog.id'),primary_key=True)
)

class Blog(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(50),nullable=False)
    content=db.Column(db.Text,nullable=False)
    feature_image= db.Column(db.String,nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    tags=db.relationship('Tag',secondary=tag_blog,backref=db.backref('blogs_associated',lazy="dynamic"))
 
    @property
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'feature_image': self.feature_image,
            'created_at': self.created_at,
        }

class Help(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(1000))
    topic = db.Column(db.String(1000))
    question = db.Column(db.String(1000))
    awnser = db.Column(db.String(1000))
    # FUTURE ME: REMEBER TO MAKE THIS SO THAT WHEN SOMEONE SEARCHES FOR HELP ON SOMETHING THEY GET CORRECT AWNSER BACK, IE: ?topic:chemistry&q="electron" GOES TO {"electron": "A subatomic particle with a negative charge and orbits the nuclues in shells"}

db.create_all()

def fib(num): 
    result = []
    count = 0
    n1 = 0
    n2 = 1
    while count < int(num):
       result.append(n1)
       nth = n1 + n2
       n1 = n2
       n2 = nth
       count += 1
    return result


# DO THIS
# 
# 
# 
def collatz(num):
    x = []
    while num > 1:
        if num % 2 == 0:
            num = num / 2
            x.append(num)
        else:
            num = num*3 + 1
            x.append(num)
    
    return x
# 
# 
# 

def get_day_of_the_year():
    days = 0
    year = datetime.now().year
    if year % 4 == 0 and year % 100 != 0 or year % 400 == 0:
        days = 366
    else:
        days = 365
    days_passed_year = datetime.now().timetuple().tm_yday
    return jsonify(time=datetime.now() , days_total=days , days_passed=days_passed_year , days_to_go=(days-days_passed_year) )


def send_email(address):
    try:
        sender_email = "drive.banerjee.armaan@gmail.com"
        receiver_email = address
        password = "ixsrblyncyrupttv"
        message = EmailMessage()
        subject = "HI there"
        body = f"Hello there, you have been emailed from me, your email adress is {address}"
        x = get_ecenomic_stuff()
        l = x[0]
        body2 = f"The GBP is worth ???{l}"
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject

        html = f"""
        <html>
            <body>
                <h1>{subject}</h1>
                <br>
                <p>{body}</p>
                <p>{body2}</p>
                <img src="./hello.jpeg" alt="hello image">
            </body>
        </html>
        """

        message.add_alternative(html, subtype="html")

        context = ssl.create_default_context()


        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())

        return "Success"
    except Exception as e:
        return e

def is_integer_num(n):
    if isinstance(n, int):
        return True
    if isinstance(n, float):
        return n.is_integer()
    return False

def bmi(weigth, height):
    x = weigth / height ** 2
    return x

def area_based_on_sides(sides, length):
    if sides == 1:
        area = math.pi * length**2
        return area
    elif sides == 2:
        return length
    elif sides == 3:
        s = (length * 3) / 2
        a = s*(s-length)*(s-length)*(s-length)
        return a**0.5
    elif sides == 4:
        return length**2
    elif sides == 5:
        x = (5*(5 + 2*(5**0.5)))
        return (1/4)*x*length**2
    elif sides == 6:
        x = 3*(3**0.5)
        return (x/2) * length**2
    elif sides % 2 == 1:
        x = (sides/4)*length**2
        a = 1/(tan(180/sides))
        return x*a
    elif sides == 8:
        x = 2*(1 + 2**0.5)*length**2
    elif sides == 10:
        x = (5/2)*length**2
        a = (5 + 2*(5**0.5))**0.5
        return x*a
    else:
        return math.pi*length**2
    

def coefficient(x,y):
    x_1 = x[0]
    x_2 = x[1]
    x_3 = x[2]
    y_1 = y[0]
    y_2 = y[1]
    y_3 = y[2]

    a = y_1/((x_1-x_2)*(x_1-x_3)) + y_2/((x_2-x_1)*(x_2-x_3)) + y_3/((x_3-x_1)*(x_3-x_2))

    b = (-y_1*(x_2+x_3)/((x_1-x_2)*(x_1-x_3))
         -y_2*(x_1+x_3)/((x_2-x_1)*(x_2-x_3))
         -y_3*(x_1+x_2)/((x_3-x_1)*(x_3-x_2)))

    c = (y_1*x_2*x_3/((x_1-x_2)*(x_1-x_3))
        +y_2*x_1*x_3/((x_2-x_1)*(x_2-x_3))
        +y_3*x_1*x_2/((x_3-x_1)*(x_3-x_2)))

    return a,b,c

def generate??from_random(n):
    ins = 0
    total = 0
    for i in range(n):
        x = random.randint(0, 1)
        y = random.randint(0, 1)
        distance = x**2 + y**2
        if distance <= 1:
            ins += 1
        total +=1
    
    return 4*ins/total

def get_top_bbc_news():
    URL = "https://www.bbc.co.uk/news"

    response  = requests.get(URL)

    soup = BeautifulSoup(response.content, "html.parser")
    result = soup.find_all("span", "gs-c-promo-heading__title gel-pica-bold")

    x = []

    for i in result:
        x.append(i.text)

    return x[-10:]

# def cpp_generate_??():
    # lib = cdll.LoadLibrary('./c++/runner.o')
    # print(lib)

# cpp_generate_??()

def get_top_bbc_links():
    URL = "https://www.bbc.co.uk/news"
    response2  = requests.get(URL)
    z = []

    soup2 = BeautifulSoup(response2.content, "html.parser")
    result2 = soup2.find_all("a", {'class': "gs-c-promo-heading nw-o-link gs-o-bullet__text gs-o-faux-block-link__overlay-link gel-pica-bold gs-u-pl-@xs"})

    for i in result2:
        x = i.get("href")
        z.append(x)
    
    return z

def get_world_covid():
    URL = "https://www.worldometers.info/coronavirus/"

    x = []

    response = requests.get(URL)
    soup = BeautifulSoup(response.content, "html.parser")

    result = soup.find_all("div", "maincounter-number")
    x.append(result[0].text)
    x.append(result[1].text)
    x.append(result[2].text)
    return x

def get_country_covid(country):
    x = []
    URL = f"https://www.worldometers.info/coronavirus/country/{country}"
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, "html.parser")

    result = soup.find_all("div", "maincounter-number")
    x.append(result[0].text)
    x.append(result[1].text)
    x.append(result[2].text)
    return x


@app.route('/')
def hello_world():
    return render_template("index.html")

@app.route('/bitcoin')
def get_bitcoin():
    response = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
    data = response.json()

    x = data["bpi"]["GBP"]["rate"]
    return f"<p>The bitcoin price is {x}</p>"

@app.route('/tfl')
def get_tfl():
    def is_tube_on():
        liste = ["District", "Central", "Circle", "Piccadilly", "Bakerloo", "Hammersmith-City", "Jubilee", "Metropolitan", "Victoria", "Northern"]
        bad = []
        status_bad = []
        r = []

        for line in liste:
            reply = requests.get("https://api.tfl.gov.uk/Line/" + line + "/Status")

            data = reply.json()

            Status = (data[0]["lineStatuses"][0]["statusSeverityDescription"])

            if Status != "Good Service":
                bad.append(line)
                status_bad.append(Status)
        
        for l in bad:
            response = requests.get(f"https://api.tfl.gov.uk/Line/{l}/Status")

            d = response.json()

            reason = (d[0]["lineStatuses"][0]["reason"])
            r.append(reason)
        
        return r
    
    return f'<p>The following are problematic: {is_tube_on()}</p>'

@app.route('/physics')
def physics():
    return '<h1> Physics</h1> <p style="text-align:center"> Welcome to the physics homepage, here you can learn about physics</p>'

@app.route('/longitudinal-waves-and-transverse-waves')
def explain_waves():
    x = "<p> A longitudinal wave is when the osicalltions are parralel to the wave motion</p><p>A transverse wave is when the osciallations are perpendicular to the wave motion<p>"
    di = "<div style='background-color: #5c32a8'><p> A longitudinal wave is faster than a transverse wave, this is because there is less firction</p><p> A longitudinal wave can also travel in solids, liquids and gasses because it does not depend on the shear strength of the medium it is travelling in, if that medium is like a liquid then ti does not have enough shear strength to support the oscillations, and so transverse waves cannot travel in liquids or gasses</p><p> However, longitudinal waves cannot travel throguh vacuums because there is no particles to bump into each other</p></div>"
    return f"{x}{di}"

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/testphp')
def test_php():
    return render_template('testphp.html')

@app.route("/<name>")
def user(name):
    if is_integer_num(name):
        return f"Your int squared = {name**2}"
    else:
        return render_template('name.html', content=f"{name}")

@app.route('/loops')
def loops():
    return render_template('anothertest.html')

@app.route('/snake')
@app.route('/snakegame.html')
def snake():
    return render_template('snakegame.html')

@app.route('/505')
def error():
    return "You stupid bugger, go fix this now"

@app.route('/resonance')
def resonance():
    return render_template('resonance.html')

@app.route('/math/square/<number>')
def square(number):
    try:
        return f"Your number squared is {float(number)**2}"
    except Exception as e:
        return e

@app.route('/math/add/<number>')
def add_num(number):
    try:
        x = [x for x in number]
        return sum(x)
    except:
        return f"Cannot calculate {number} please make it a list"

@app.route('/math/quadfinder/<lofquadpoints>')
def findthisquadeq(lofquadpoints):
    try:
        x = lofquadpoints[:2]
        y = lofquadpoints[3:]
        z = coefficient(x, y)
        aa = z[0]
        bb = z[1]
        cc = z[2]
        return f"{aa}x^2 + {bb}x + {cc}"
    except:
        return "Could not compute"

@app.route('/math/factorial/<number>')
def factorial(number):
    try:
        x = 1
        for i in int(number):
            x = x*i
        return x
    except:
        return "You must try with an integer"  

@app.route('/chemistry/periodic-table')
def periodic_table():
    return render_template("periodictable.html")

#@app.route("/admin/login", methods=["POST", "GET"])
#def login():
    #if request.method == "POST":
        #user = request.form["nm"]
        #return redirect(url_for("admin/user", usr=user))

#@app.route("/admin/<usr>")
#def user(usr):
    #return f"<h1>{usr}</h1>"

@app.route('/minesweeper')
def minesweeper():
    return render_template('minesweeper.html')

@app.get('/todo')
def show_todo():
    todo_list = db.session.query(Todo).all()
    return render_template("todo.html", todo_list=todo_list)

@app.post("/todo/add")
def todo_add():
    title = request.form.get("title")
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("show_todo"))

@app.get("/todo/update/<int:todo_id>")
def update(todo_id):
    # todo = Todo.query.filter_by(id=todo_id).first()
    todo = db.session.query(Todo).filter(Todo.id == todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("show_todo"))

@app.get("/todo/delete/<int:todo_id>")
def deletet(todo_id):
    # todo = Todo.query.filter_by(id=todo_id).first()
    todo = db.session.query(Todo).filter(Todo.id == todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("show_todo"))

@app.route('/books')
def get_books():
    listx = db.session.query(Readinglist).all()
    return render_template("books.html", listy=listx)

@app.route('/books/add')
def add_books():
    titlen = request.form.get("booktitle")
    authorn = request.form.get("bookauthor")
    summaryn = request.form.get("booksummary")
    newbook = Readinglist(list=titlen, summary=summaryn)
    db.session.add(newbook)
    db.session.commit()
    return redirect(url_for("get_books"))

@app.route("/books/delete/<int:bookid>")
def deleteb(bookid):
    book = db.session.query(Readinglist).filter(Readinglist.id == bookid).first()
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for("get_books"))

@app.route('/newsletter')
def show_emails():
    emails = db.session.query(Emaillist.emailadd).all()
    return render_template("newsletter.html", msg=emails)

@app.route("/newsletter/add", methods=["POST", "GET"])
def add_newsletter():
    try:
        if request.method == "POST":
            emails = db.session.query(Emaillist.emailadd).all()
            emailx = request.form.get("newsletter")
            if emailx in emails:
                flash("Already subscribed!", category="error")
            else:
                new_email = Emaillist(emailadd=str(emailx))
                db.session.add(new_email)
                db.session.commit()
                return redirect(url_for("show_emails"))
        else:
            return "What?"
    except Exception as e:
        return f"Could not be carried out because {e}" 

@app.route('/history')
def history():
    return "Coming soon!"

@app.route('/emailer', methods=["POST", "GET"])
def emailer():
    if request.method == "POST":
        try:
            Email = request.form["Email"]
            x = send_email(Email)
            if x == "Success":
                return "Sent the email successfully"
            else:
                return "Somethin went wrong"
        except:
            return f"Did not work properly, are you sure you meant to send it to {Email}"
    else:
        return render_template('emailer.html')
        
@app.route('/math/fibonacci', methods=["POST", "GET"])
def fibonnaci():
    if request.method == "POST":
        x = request.form["Fibnum"]
        y = fib(x)
        return render_template('fibonacci.html', fibnums=y)
    else:
        return render_template('fibonacci.html')

@app.route('/math/permutate', methods=["POST", "GET"])
def permutate():
    if request.method == "POST":
        y = request.form["permutations"]
        haha = list(permutations(y))
        return render_template("permutations.html", permutations=haha, len=len(haha))
    else:
        return render_template('permutations.html')

@app.route('/math/permutate/unique', methods=["POST", "GET"])
def unique_permutate():
    if request.method == "POST":
        li = []
        y = request.form["permutations"]
        haha = list(permutations(y))
        for perm in haha:
            if perm in li:
                pass
            else:
                li.append(perm[::-1])
        
        return render_template("permutations.html", permutations=li, len=len(li))
    else:
        return render_template('permutations.html')

# @app.route("/files/get")
# def send_randomfile():
#         x = os.listdir("/Users/mohuasen/prev/all/Armaan/PDFS")
#         file = random.choice(x)
#         try:
#             return send_file(file)
        # except Exception as e:
            # return e

@app.get("/blog")
def blog_home():
    return "A blog"

@app.errorhandler(404)
def error():
    return "This content doesn't seem to be available, sorry about that"

@app.route("/math/numberguesser")
def number_guesser():
    return render_template('numberguesser.html')

@app.route("/calculators/temperature")
def convert_temp():
    return render_template("temperature.html")

@app.get("/calculators/stopwatch")
def stopwatch():
    return render_template("stopwatch.html")

@app.route("/bloger/add", methods=["POST", "GET"])
def bog_add():
    if request.method == "POST":
        x = request.form["title"]
        cmd = f" cd ./templates && touch {x}.html"
        os.system(cmd)
        y = request.form["content1"]
        z = y.split(". ")
        with open(f"{x}.html") as file:
            file.write('{% extends "baseblog.html" %} \n')
            file.write('{% block title %}' + x + '{% endblock %}')
            file.write('{% block content%}')
            for i in z:
                file.write(f"<p>{i}</p>")
            file.write("{% endblock %}")
            file.close()
    return render_template("blogadd.html")

@app.route("/about")
def about():
    return "Hi there this is a website"

@app.route("/calculators/location")
def calc_location():
    if request.method == "POST":
        x = request.form["O"]
        z = x.split()
        xx = Position("x", z[0], z[1])
        y = request.form["N"]
        a = y.split()
        aa = Position("y", a[0], a[1])
        s = xx.distance_to(aa)
        return render_template("locations.html", d=s)
    else:
        return(render_template("locations.html"))

@app.route("/ecenomics/ftse100")
def ret_ftse100():
    b = get_ecenomic_stuff()
    return f"Ftse currently at {b[1]} points"

@app.route("/ecenomics/sandp500")
def ret_sandp500():
    b = get_ecenomic_stuff()
    return f"S&P 500 surrently at {b[2]} points"

@app.route("/ecenomics/TSLA")
def TSLA():
    b = get_ecenomic_stuff()
    return f"Tesla market cap: ${b[4]}"

@app.route("/admin/views")
def how_many_views_page():
    with open("views.txt", "r+") as views:
        x = views.read()
        x += 1
        views.write(x)
    return f"this page has been viewd {x} times"

@app.route("/physics/vectors")
def vector_stuff():
    pass 
    # Can't be bothered to do the webpage for now

@app.route("/covid")
def covid():
    return 0

@app.route("/physics/gold-leaf-electroscope")
def gold_leaf_electroscope():
    return 0

@app.route("/chemistry/group1")
def alkaline_earth_matals():
    return 0

@app.route("/chemistyr/reaction-with-water")
def reaction_with_water():
    return 0

@app.route("/docs")
def docs():
    return "This is the official  documentation"

@app.route("/conway-game-life")
def conway_game_of_life():
    return "I am working on it"

# @app.route("/stream")
# def stream():
#     video = cv2.VideoCapture(0)
#     def generator(webcam):
#         while True:
#             success, image = video.read()
#             if success:
#                 ret, jpeg = cv2.imencode('.jpg', image)
#                 frame = jpeg.tobytes()
#                 yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    
#     return Response(generator(video),mimetype='multipart/x-mixed-replace; boundary=frame')
# STUPID VERCEL THINKA OPEN-CV IS TOO LARGE

@app.route("/ip-address")
def ip_address():
    x = get_user_ip_address()
    return f"Your ip address is {x}"

@app.route("/api/day-of-the-year")
def day_of_year():
    x = get_day_of_the_year()
    return x

@app.route("/api/test/simpleparams")
def with_parameters():
    name = request.args.get('name')
    age = request.args.get('age', default=4)
    return jsonify(message="My name is " + name + " and I am " + str(age) + " years old")

@app.route("/api/test/question")
def test_of_question():
    x = ''
    subject = request.args.get("subject")
    topic = request.args.get("topic")
    question = request.args.get("q")
    if question.lower() == "help":
        x = "Please go to /docs"
    else:
        x = 'test'
    return jsonify({subject: {topic: {question: x}}})

@app.route("/api/sendemail")
def api_email():
    adress = request.args.get("adress")
    x = send_email(adress)
    return jsonify(status=x)

@app.route("/api/math/fibonacci")
def api_fibonacci():
    num = request.args.get("limit")
    try:
        x = fib(int(num))
        dict = {}
        for i in range(len(x)):
            dict[i] = x[i]
        return jsonify(dict, x)
    except:
        return jsonify(error='Must be integer')

@app.route("/api/math/generatepi")
def show_gen_??():
    num = int(request.args.get("accuracy"))
    x = generate??from_random(num)
    ?? = math.pi
    difference = ?? - x
    percentoff = 100 - (x / ??)*100
    return jsonify(guess=x, actual=??, difference=difference, percenterror = percentoff, tip='Try 1000')

@app.route("/api/test/numberguesser")
def number_guesser_api():
    num = int(request.args.get("guess"))
    x = random.randint(0, 100)
    if num == x:
        return jsonify(number=num, correct=True)
    else:
        return jsonify(number=num, correct=False, actual=x)

@app.route("/api/math/collatz")
def collatz_api():
    num = int(request.args.get("number"))
    try:
        x = collatz(num)
        dict = {}
        for i in range(len(x)):
            dict[i] = x[i]
        return jsonify(dict, x)
    except:
        return jsonify(message="Must be an integer")
    

# @app.before_request
# def before():
#     # return "This is executed BEFORE each request."

@blogs.route('/add_blog',methods=["POST"])
def create_blog():
    data = request.get_json()
 
    new_blog=Blog(title=data["title"],content=data["content"],feature_image=data["feature_image"])
 
    for tag in data["tags"]:
        present_tag=Tag.query.filter_by(name=tag).first()
        if(present_tag):
            present_tag.blogs_associated.append(new_blog)
        else:
            new_tag=Tag(name=tag)
            new_tag.blogs_associated.append(new_blog)
            db.session.add(new_tag)
            
 
    db.session.add(new_blog)
    db.session.commit()
 
    blog_id = getattr(new_blog, "id")
    return jsonify({"id": blog_id})


@blogs.route('/blogs',methods=["GET"])
def get_all_blogs():
    blogs= Blog.query.all()
    serialized_data = []
    for blog in blogs:
        serialized_data.append(blog.serialize)
 
    return jsonify({"all_blogs": serialized_data})

@blogs.route('/blog/<int:id>',methods=["GET"])
def get_single_blog(id):
    blog = Blog.query.filter_by(id=id).first()
    serialized_blog = blog.serialize
    serialized_blog["tags"] = []
 
    for tag in blog.tags:
        serialized_blog["tags"].append(tag.serialize)
 
    return jsonify({"single_blog": serialized_blog})

@blogs.route('/update_blog/<int:id>', methods=["PUT"])
def update_blog(id):
    data = request.get_json()
    blog=Blog.query.filter_by(id=id).first_or_404()
 
    blog.title = data["title"]
    blog.content=data["content"]
    blog.feature_image=data["feature_image"]
 
    updated_blog = blog.serialize
 
    db.session.commit()
    return jsonify({"blog_id": blog.id})

@blogs.route('/delete_blog/<int:id>', methods=["DELETE"])
def delete_blog(id):
    blog = Blog.query.filter_by(id=id).first()
    db.session.delete(blog)
    db.session.commit()
 
    return jsonify("Blog was deleted"),200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5050)