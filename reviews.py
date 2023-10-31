import json


class ReviewsResource:
    #
    # This code is just to get us started.
    # It is also pretty sloppy code.
    #

    students_file = \
        "reviews.json"

    def __init__(self):
        self.reviews = None

        with open(self.students_file, "r") as j_file:
            self.reviews = json.load(j_file)

    def get_reviews(self):
        return self.reviews
