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

    def generate_next_id(self):
        # Assuming data is a list of objects with numeric IDs
        if not self.reviews:
            return 1  # If the list is empty, start with ID 1
        else:
            # Find the maximum ID and increment by 1
            max_id = max(item['review_id'] for item in self.reviews)
            return max_id + 1

    def get_reviews(self):
        return self.reviews
    
    def add_review(self, review_info):
        self.reviews.append(review_info)
        with open(self.students_file, 'w') as file:
            json.dump(self.reviews, file, indent=2)

    def update_review(self, review_id, new_review_text):
        for review in self.reviews:
            if review['review_id'] == review_id :
                review['text'] = new_review_text
        with open(self.students_file, 'w') as file:
            json.dump(self.reviews, file, indent=2)