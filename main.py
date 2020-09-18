from flask import Flask, render_template, url_for

app = Flask(__name__)

posts = [

    {'title': 'Book',
     'author': 'Corey',
     'content': 'Words',
     'date_posted': '04/05/2020'},

    {'title': 'Whale',
     'author': 'Jamie',
     'content': 'Letters',
     'date_posted': '06/05/2020'},

    {'title': 'Car',
     'author': 'Ty',
     'content': 'Paragraphs',
     'date_posted': '04/07/2020'},

    {'title': 'Stuff',
     'author': 'Nexus',
     'content': 'Graphs',
     'date_posted': '08/05/2020'},
]


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html", title='About')


@app.route("/posts")
def notable():
    return render_template("html.html", posts=posts, title='Post')


@app.route("/webcam")
def webcam():
    return render_template("webcam.html", title='Webcam')


@app.route("/notify")
def notify():
    return render_template("notify.html", title='Notify')


if __name__ == "__main__":
    app.run(debug=True)
