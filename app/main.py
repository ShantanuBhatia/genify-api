from flask import Flask
from flask import render_template
from api_methods.product_recommender import recommender

app = Flask(__name__)
app.register_blueprint(recommender)


@app.route('/')
def render_frontend():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
