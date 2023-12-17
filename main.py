import flask
from reviews import ReviewsResource
from resources.reviews_data_service import ReviewsDataService
import notif
import json
from jose import jwt, JWTError
from flask_http_middleware import MiddlewareManager
from middleware import MetricsMiddleware

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = flask.Flask(__name__)
reviews_resource = ReviewsResource()
all_reviews = reviews_resource.get_reviews()
ds_reviews = ReviewsDataService()


app.wsgi_app = MiddlewareManager(app)
app.wsgi_app.add_middleware(MetricsMiddleware)

SECRET_KEY = "secret"

def authorize_jwt():
    jwt_token = flask.request.headers.get("Authorization")
    if not jwt_token:
        flask.abort(401, "You are unauthorized to access this page")
    try:
        token = jwt_token.split(" ")[1]
        #decode the JWT Token
        decoded_jwt_token = jwt.decode(token,SECRET_KEY, algorithms = ["HS256"])
        user_id = decoded_jwt_token.get("sub")
        return user_id
    except JWTError as e:
        flask.abort(401, f"Invalid token error: {str(e)}")
@app.get("/")
def hello():
    """Return a friendly HTTP greeting."""
    return "Hello Review Management!!!\n"

@app.get("/authorized_reviews")
def authorized_get_all_reviews():
    #ONLY to check JWT Token authorization working
    # authorize with user_id
    user_id = authorize_jwt()
    rev = ds_reviews.get_all_reviews()
    return rev
@app.get("/reviews")
def get_all_reviews():
    #pagination implemented
    page = flask.request.args.get('page', default=1, type=int)
    items_per_page = flask.request.args.get('items_per_page', default=5, type=int)

    start_idx = (page - 1) * items_per_page
    end_idx = start_idx + items_per_page
    rev = ds_reviews.get_all_reviews()
    paginated_reviews = rev[start_idx:end_idx]
    return flask.jsonify(paginated_reviews)

@app.get("/recipe/<id>")
def get_recipe_reviews(id):
    # return("bruh ")
    result = []
    for each in all_reviews:
        if each["recipe_id"] == int(id):
            result.append(each)
    return ds_reviews.get_review_for_recipe(int(id))


@app.get("/recipe/<id>/most-recent")
def get_most_recent_reviews(id):
    return ds_reviews.get_mostrecent_for_recipe(int(id))

@app.get("/recipe/<id>/top-rated")
def get_top_rated_reviews(id):
    return ds_reviews.get_toprated_for_recipe(int(id))

@app.get("/user/<id>")
def get_user_reviews(id):
    return ds_reviews.get_review_for_user(id)



@app.route("/post_review", methods=['POST'])
def post_review():
    """
    Endpoint for posting a new review.
    Expects a JSON payload with the necessary data.
    """
    data = flask.request.get_json()

    # Example of extracting required fields from the JSON payload
    review_id = reviews_resource.generate_next_id()
    recipe_id = data.get('recipe_id')
    user_id = data.get('user_id')
    text = data.get('text')
    rating = data.get('rating')
    date = data.get('date')

    new_review = {
        'review_id': review_id,
        'recipe_id': recipe_id,
        'user_id': user_id,
        'rating': rating,
        'date': date,
        'text': text,
        'upvotes': 0,
        'downvotes': 0,
    }

    reviews_resource.add_review(new_review)
    added_rev = ds_reviews.add_review(recipe_id,user_id,rating,date,text,0,0)
    if added_rev != None:
        return flask.jsonify({'message': 'Review added successfully' + str(added_rev)}), 200
    else:
        return flask.jsonify({'error': 'Could not create review'}), 404

@app.route("/delete_review/<review_id>", methods=['DELETE'])
def delete_review(review_id):

    del_rev = ds_reviews.delete_review(review_id)
    if del_rev != None:
        return flask.jsonify({'message': 'Review deleted successfully' + str(del_rev)}), 200
    else:
        return flask.jsonify({'error': 'Could not create review'}), 404
    
    global all_reviews
    total_reviews = len(all_reviews)
    all_reviews = [review for review in all_reviews if review["review_id"] != int(review_id)]

    if total_reviews != len(all_reviews):
        with open('reviews.json', 'w') as file:
            json.dump(all_reviews, file, indent=2)
        notif.send_deleted_notif()
        return {"message": f"Review {review_id} has been successfully deleted"}
    else:
        flask.abort(404, f"Review {review_id} not found")

@app.route("/update_review", methods=['PUT'])
def update_review():
    data = flask.request.get_json()
    review_id = data.get('review_id')

    new_review_text = data.get('new_review_text')

    mod_rev = ds_reviews.modify_review_text(review_id, new_review_text)
    print("HELLO")
    print(str(mod_rev))
    if mod_rev != None:
        return flask.jsonify({'message': 'Review updated successfully' + str(mod_rev)}), 200
    else:
        return flask.jsonify({'error': 'Review not found'}), 404

if __name__ == "__main__":
    # Used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host="localhost", port=8080, debug=True)