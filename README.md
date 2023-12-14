# review-management
Cloud Computing Microservice on google app engine
# To Run :
_python main.py_

# To test JWT Token Authentication:
Copy your JWT token after running _python encode_token.py_ \
Make sure the microservice is running. \
__For valid JWT Token:__ In POSTMAN, go to _GET http://localhost:8080/authorized_reviews_ and paste the previous token into Authorization -> Bearer Token \
__For Invalid:__ In POSTMAN, go to _GET http://localhost:8080/authorized_reviews_ with No Auth
