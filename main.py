import flask
from reviews import ReviewsResource
# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = flask.Flask(__name__)
reviews_resource = ReviewsResource()
all_reviews = reviews_resource.get_reviews()

@app.get("/")
def hello():
    """Return a friendly HTTP greeting."""
    return "Hello Review Management!!!\n"

@app.get("/reviews")
def get_all_reviews():
    return all_reviews

@app.get("/recipe/<id>")
def get_recipe_reviews(id):
    # return("bruh ")
    result = []
    for each in all_reviews:
        if each["recipe_id"] == int(id):
            result.append(each)
    return result

@app.get("/user/<id>")
def get_user_reviews(id):
    # return("bruh ")
    result = []
    for each in all_reviews:
        if each["user_id"] == id:
            result.append(each)
    return result


if __name__ == "__main__":
    # Used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host="localhost", port=8080, debug=True)