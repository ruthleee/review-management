import json
import mysql.connector

class ReviewsDataService():
    def __init__(self):

        self.connection = self.get_connection()

    def get_connection(self):
        return mysql.connector.connect(
            user="admin",
            password="cloudymeatball",
            host="recipediadb.c52h6qfa4sj1.us-east-1.rds.amazonaws.com",
            port="3306",
            database="reviewsDB"
        )

    '''
    def get_data_file_name(self):
        filename =  self.data_dir + "/" + self.data_file
        return filename
    
    def load(self):
        file_name = self.get_data_file_name()
        with open(file_name, "r") as file:
            self.users = json.load(file)
        

    def save(self):
        file_name = self.get_data_file_name()
        with open(file_name, "w") as out_file:
            json.dump(self.users, out_file)
    '''

    def generate_next_id(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT MAX(review_id) FROM reviews")
            result = cursor.fetchone()
            max_review_id = result[0] if result[0] is not None else 0
            cursor.close()
            return max_review_id + 1
        except mysql.connector.Error as e:
            print("Error fetching max review_id:", e)
            return None
    
    def get_all_reviews(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM reviews")
            reviews = cursor.fetchall()
            cursor.close()
            return reviews
        except mysql.connector.Error as e:
            print("Error fetching reviews:", e)
            return []

    def get_review_for_recipe(self, recipe_id: int):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM reviews WHERE recipe_id = %s", (recipe_id,))
            reviews = cursor.fetchall()
            cursor.close()
            return reviews
        except mysql.connector.Error as e:
            print("Error fetching review info:", e)
            return None

    def get_review_for_user(self, user_id):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM reviews WHERE user_id = %s", (user_id,))
            reviews = cursor.fetchall()
            cursor.close()
            return reviews
        except mysql.connector.Error as e:
            print("Error fetching review info:", e)
            return None
    
    def get_toprated_for_recipe(self, recipe_id:int):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM reviews WHERE recipe_id = %s ORDER BY upvotes DESC", (recipe_id,))
            reviews = cursor.fetchall()
            cursor.close()
            return reviews
        except mysql.connector.Error as e:
            print("Error fetching review info:", e)
            return None
        
    def get_mostrecent_for_recipe(self, recipe_id:int):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM reviews WHERE recipe_id = %s ORDER BY date DESC", (recipe_id,))
            reviews = cursor.fetchall()
            cursor.close()
            return reviews
        except mysql.connector.Error as e:
            print("Error fetching review info:", e)
            return None
        
    def add_review(self, recipe_id: str, user_id: str, rating: str, date: str, text: str, upvotes: int, downvotes:int):
        """
        This will add a review into the db
        """
        review_id = self.generate_next_id()

        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT INTO reviews (review_id, recipe_id, user_id, rating, date, text, upvotes, downvotes) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (review_id, recipe_id, user_id, rating, date, text, upvotes, downvotes)
            )
            self.connection.commit()
            cursor.close()
            return (review_id, recipe_id, user_id, rating, date, text, upvotes, downvotes)
        except mysql.connector.Error as e:
            print("Error adding review:", e)
            return None

    def modify_review_text(self, review_id: str, new_text: str):
        """
        This will modify one of the user's fields
        """
        try:
            cursor = self.connection.cursor()

            # Check if the field exists in the table and construct the query accordingly
            
            cursor.execute(
                f"UPDATE reviews SET text = %s WHERE review_id = %s",
                (new_text, review_id)
            )
            self.connection.commit()

            cursor.execute("SELECT * FROM reviews WHERE review_id = %s", (review_id,))
            updated_review = cursor.fetchone()
            cursor.close()
            return updated_review

        except mysql.connector.Error as e:
            print("Error modifying review field:", e)
            return None

    def delete_review(self, review_id: str):
        """
        deletes a user from teh db
        """
        try:
            cursor = self.connection.cursor()

            cursor.execute("DELETE FROM reviews WHERE review_id = %s", (review_id,))
            self.connection.commit()

            cursor.close()

            # Optionally, you can return the updated list of users after deletion
            return self.get_all_reviews()
        except mysql.connector.Error as e:
            print("Error deleting review:", e)
            return None