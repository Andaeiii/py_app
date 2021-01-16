from flask import Flask, render_template
app = Flask(__name__)

# @ - decorators to add extra functions to application...
# to set the environment variables...
# ----------------------------------------use the set keyword...
# set FLASK_APP=main.py
# set FLASK_DEBUG=1


@app.route("/")
@app.route('/home')  # homepage redirects here too...
def homepage():
    return render_template('home.html')


@app.route("/about")
def about():
    return '<h1>this is our about page </h1>'


@app.route("/multi-html")
def multiHtml():
    return '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Document</title>
        </head>
        <body>
        <h1>This is a multi-line page... </h1>
        <p>
            plus its not advisable to place multiline html files within your page that way.... not advisable at all... 
        </p>
            
        </body>
        </html>
    '''


# if you dont want to use the environment variables...
if __name__ == '__main__':
    app.run(debug=True)
