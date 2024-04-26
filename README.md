# Order Processing System

simplified Order Processing System for an online store.

* Stock management
* Mock payment gateway integration
* Order confirmation email sending

**Project Structure:**

The project consists of the following files:
* config.py: Contains configuration settings for flask, stripe, flask_pymongo.
* functions.py: Contains helper functions used in the project.
* app.py: The main Flask application file that defines the routes and handles the order processing logic.

**Requirements:**

* `Python` 
* `smtplib` 
* `Flask` 
* `flask-pymongo` 
* `stripe` 

**Setup:**

* Build the Docker image by running `docker build -t order-processing-system .` in the project directory.
* Run the Docker container by running `docker run -p 8000:8000 order-processing-system`.

**Flask routes:**
1. /review/<userId>: Retrieves the order for a given user ID, checks the inventory, and renders the review page. If the order is out of stock, it displays an appropriate message.

2. /checkout/<userId>: Renders the checkout page for a given user ID.

3. /stripe_pay/<userId>: Processes the payment using Stripe's checkout session API. It creates a new session, including the line items from the order, and returns the checkout session ID and public key.

4. /thanks/<userId>: Handles the success redirect from Stripe after payment. If the session ID is present, it updates the inventory, sends an order confirmation email, and renders the thank you page.

