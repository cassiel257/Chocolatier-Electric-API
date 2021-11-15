# The Chocolatier Electric

Welcome to The Chocolatier Electric, an app to help chocolate lovers discover the best chocolate makers and to encourage chocolatiers to increase their visibility amongst connoisseurs! Chocolate makers can share their specialties and contact information with customers. Customers can give details of great chocolate foods that they've eaten, and access the reviews of others. Get inspiration for your next chocolate fix, whether it be for a gift, holiday, or every day.

Please keep reading for instructions on how to access and use our API, and how to set up a development environment to test it out and contribute to the project!

## API Instructions and Examples
-This API can be accessed at: https://chocolatier-electric.herokuapp.com/
-Only the Chocolates route can be viewed pubicly with a get request. All other routes and methods required authentication detailed below.
### Authentication Required
- **For project reviewers:** valid tokens for both roles(Customer and Manager) will be stored in the ```setup.sh``` file.
- Customer tokens have the permissions: get:chocolates, post:chocolates, patch:chocolates, get:chocolatiers
- Manager tokens have the same permissions and the additional permissions: post:chocolatiers, patch:chocolatiers, delete:chocolatiers, delete:chocolates
  
- The URLs that will provide authentication tokens(you will find these in your browser address bar after the phrase 'token='):
    - Live site: https://sparkle-coffee.us.auth0.com/authorize?audience=chocolate&response_type=token&client_id=p6Mrnz5sU1X4WYtKSuTiBG8LkSFt4Wf4&redirect_uri=https://chocolatier-electric.herokuapp.com

    - Local site (for dev/testing): https://sparkle-coffee.us.auth0.com/authorize?audience=chocolate&response_type=token&client_id=p6Mrnz5sU1X4WYtKSuTiBG8LkSFt4Wf4&redirect_uri=http://localhost:5000

  
- For general users: when accessing the API, go to the first URL above.
- You will be redirected to an Auth0 screen. Please register/login using your email address and a password, or through your Google account.
- You will then be directed to the index page of the API, a simple welcome message. Locate the token in the browser bar and copy/paste it into the setup.sh file if you are running locally and want to export it, or paste it into Postman "Bearer Token" section under the 'Authentication' tab of your requests.
- You can now access the authorized endpoints described in the "Endpoints" section below, by using
- The security tokens expire after a few hours, so you may need to log in again to continue using the API.

**ROLES**

**Customers**
- Can view chocolatiers and chocolates
- Add a chocolate entry
- Search chocolate names
- Modify chocolates
  
**Managers**
(Only managers can add or modify chocolatier information)
- Has all the permissions of a Customer and also the following:
- Add a chocolatier to the database
- Modify a chocolatier entry
- Delete a chocolate entry
- Delete a chocolatier entry
  
**ENDPOINTS:**
- GET /chocolates
    - Retrieves a list of all chocolates and their details, and also returns a "Success" response.
-  GET /chocolatiers
    - Retrieves a list of all chocolatiers and their details, and also returns a "Success" response.
- POST /chocolates
    - Creates a new chocolate, taking input for the fields 'name','chocolate_type','vendor','vendor_id'(optional), and 'comments'.
    - Returns a success message, the id number and name of the created chocolate entry, and the total number of chocolate reviews.
- POST /chocolatiers
    - Creates a new chocolatier, taking input for the fields 'name','address','website','facebook','phone', 'chef' and 'comments'.
    - Returns a success message, the id number and name of the created chocolatier entry, and the total number of chocolatiers.
- PATCH /chocolates/{id}
    - Modifies a chocolate entry based on its id number, taking input for the fields 'name','chocolate_type','vendor','vendor_id', and 'comments'.
    - Returns a success message, and the updated chocolate entry.
- PATCH /chocolatiers/{id}
    - Modifies a chocolate entry based on its id number, taking input for the fields 'name','chocolate_type','vendor','vendor_id', and 'comments'.
    - Returns a success message, and the updated chocolate entry.
- DELETE /chocolates/{id}
  - Deletes a chocolate entry based on its id number. 
  - Returns the id number of the deleted item, and a success message. If the entry has already been deleted, it will produce a 422 error. 
- DELETE /chocolatiers/{id}
  - Deletes a chocolatier entry based on its id number. 
  - Returns the id number of the deleted item, and a success message. If the entry has already been deleted, it will produce a 422 error.
- POST /chocolates/search
  - Takes user input for a 'searchTerm' string value and retrieves a list of all chocolate entries that contain that word/string (case-insensitive). Also returns a "Success" message.

**SAMPLE REQUESTS AND RESPONSES**
- GET /chocolates
  - Sample curl:
    ```
    curl --location --request GET 'https://chocolatier-electric.herokuapp.com/chocolates' --header 'Authorization: Bearer ${MANAGER_TOKEN}'
    ```
  - Sample response:
    ```
    {
    "Chocolates": [
        {
            "chocolate_type": "bittersweet cocoa powder",
            "comments": "Best organic brownies in town",
            "id": 1,
            "name": "brownies",
            "vendor": "Chamberlain",
            "vendor_id": 2
        },
        {
            "chocolate_type": "dark chocolate",
            "comments": "Cool concept",
            "id": 2,
            "name": "tortes",
            "vendor": "Chocolate Lab",
            "vendor_id": 4
        },
        {
            "chocolate_type": "milk chocolate",
            "comments": "Excellent milk chocolates and truffles.",
            "id": 3,
            "name": "chocolate bunnies",
            "vendor": "Christophe Artisan Chocolates",
            "vendor_id": 5
        }
    ],
    "Success": true
    }
    ```
- POST /chocolates
  - Sample curl:
    ```
    curl --location --request POST 'https://chocolatier-electric.herokuapp.com/chocolates/' \
    --header 'Authorization: Bearer ${MANAGER_TOKEN}'
    --header 'Content-Type: application/json' \
    --data-raw '{
    "name":"post test tortes",
    "chocolate_type":"test",
    "vendor":"test",
    "vendor_id": 1,
    "comments":"Wow"
    }'
    ```
  - Sample response:
- POST /chocolates/search
  - Sample curl:
  ```
    curl --location --request POST 'https://chocolatier-electric.herokuapp.com/chocolates/search' \
    --header 'Authorization: Bearer ${MANAGER_TOKEN}'
    --header 'Content-Type: application/json' \
    --data-raw '{"searchTerm":"choc"}'
  ```
  - Sample response:
    ```
    {
    "chocolates": [
        {
            "chocolate_type": "milk chocolate",
            "comments": "Excellent milk chocolates and truffles.",
            "id": 3,
            "name": "chocolate bunnies",
            "vendor": "Christophe Artisan Chocolates",
            "vendor_id": 5
        }
    ],
    "success": true
    }
    ```
- PATCH /chocolates/{id}
  - Sample curl:
  ```
    curl --location --request PATCH 'https://chocolatier-electric.herokuapp.com/chocolates/1' \
    --header 'Authorization: Bearer ${MANAGER_TOKEN}'
    --header 'Content-Type: application/json' \
    --data-raw '{
    "name":"newer Test", 
    "chocolate_type":"test", 
    "vendor":"test", 
    "vendor_id":2,
    "comments":"test"
    }'
  ```
  - Sample response:
    ```
    {
    "chocolate": [
        "id":1,
        "name":"test",
        "chocolate_type":"test",
        "vendor":"test",
        "vendor_id":2,
        "comments":"test"
    ],
    "success": true
    }
    ```
- DELETE /chocolates/{id}
  - Sample curl:
    ```
    curl --location --request DELETE 'https://chocolatier-electric.herokuapp.com/chocolates/1' --header 'Authorization: Bearer ${MANAGER_TOKEN}'
    ```
  - Sample response:
    ```
    {
    "deleted": 1,
    "success": true
    }
    ```
- GET /chocolatiers
  - Sample curl:
  ```
  curl --location --request GET 'https://chocolatier-electric.herokuapp.com/chocolatiers' --header 'Authorization: Bearer ${MANAGER_TOKEN}'
  ```
  - Sample response:
  ```
  {
    "Chocolatiers": [
        {
            "address": "234 Sweets Avenue",
            "chef": "Belle Thackeray",
            "comments": "Specializing in baked chocolate goods.",
            "id": 1,
            "name": "Brownie Belle",
            "phone": "234-445-5674",
            "website": "website.com"
        },
        {
            "address": "Atlanta, Georgia",
            "chef": "Chamberlain staff",
            "comments": "Ask about our catering service!",
            "id": 2,
            "name": "Chamberlain's Chocolate",
            "phone": "678-728-0100",
            "website": "https://www.chamberlainschocolate.com/"
        },
        {
            "address": "Wisconsin",
            "chef": "Dillon Family",
            "comments": "Non GMO and organic",
            "id": 3,
            "name": "Dillon's Chocolates",
            "phone": "262-337-9639",
            "website": "https://dillonschocolates.com/"
        },
        {
            "address": "Denver, Colorado",
            "chef": "Phil Simonson",
            "comments": "Visit our restaurant!",
            "id": 4,
            "name": "Chocolate Lab",
            "phone": "720-536-5037",
            "website": "https://chocolatelabdenver.com"
        },
        {
            "address": "Charleston, SC",
            "chef": "Christophe",
            "comments": "Now in multiple locations.",
            "id": 5,
            "name": "Christophe Artisan Chocolatier",
            "phone": "843-297-8674",
            "website": "https://christophechocolatier.com/"
        }
    ],
    "Success": true
    }
  ```
- POST /chocolatiers
  - Sample curl:
    ```
    curl --location --request POST 'https://chocolatier-electric.herokuapp.com/chocolatiers' \
    --header 'Authorization: Bearer ${MANAGER_TOKEN}'
    --header 'Content-Type: application/json' \
    --data-raw '{
    "name":"Test",
    "address":"Test",
    "website":"Test",
    "facebook":"Test",
    "phone":"12345",
    "comments":"Test"
    }'
    ```
  - Sample response:
- PATCH /chocolatiers/{id}
  - Sample curl:
    ```
    
    curl --location --request PATCH 'https://chocolatier-electric.herokuapp.com/chocolatiers/1' \
    --header 'Authorization: Bearer ${MANAGER_TOKEN}'
    --header 'Content-Type: application/json' \
    --data-raw '{
        "name":"new Test", 
        "address":"test", 
        "website":"test", 
        "facebook":"test",
        "phone":"test",
        "chef":"test",
        "comments":"test"
        }'
  
    ```
  - Sample response:
    ```
    {
    "chocolatier": [
        "id":1,
        "name":"new Test",
        "address":"test",
        "website":"test",
        "phone":"test",
        "chef":"test",
        "comments":"test"
    ],
    "success": true
    }
    ```
- DELETE /chocolatiers/{id}
  - Sample curl:
    ```
    curl --location --request DELETE 'https://chocolatier-electric.herokuapp.com/chocolatiers/1' --header 'Authorization: Bearer ${MANAGER_TOKEN}'
    ```
  - Sample response:
    ```
    {
    "deleted": 1,
    "success": true
    }
    ```
  
### Error Handling
Incorrect requests or missing information may produce the following errors:
- 400 Bad Request
- 401 Not Authorized
- 404 Resource Not Found
- 405 Method Not Allowed
- 422 Unprocessable
- 500 Server Error

Here is an example of an error response:
```
    {
         "success": False,
         "error": 404,
         "message": "Resource Not Found. Sorry!"
    }
 ```   
## Setting Up A Development Environment
- Download our project code to your local machine by using the command ```git clone https://github.com/cassiel257/FullStackCapstone.git``` (or clicking the green "Code" button on Github and downloading a zip file).
### Installing Software Dependencies
- To run our app locally, please install the latest version of Python 3 (which automatically includes the venv virtual environment tool).
- You will need to install Postgres to work with the database. The project is set up to use the default username 'postgres' and password 'postgres'.
- Within the project directory, create a virtual environment for this project using ```py -m venv env``` or ``python3 -m venv env``
- Start your virtual environment with a command like ```source env/bin/activate``` or ```source env\Scripts\activate```(Windows)
- Install the other necessary software by typing the command ``pip install -r requirements.txt``.
### Running the App Locally
- From within the project directory, start your virtual environment if you haven't already.
- To create the database and import sample data, use the commands:
  ```
  createdb chocolate
  psql chocolate<chocolate.psql
  ```
- Export environment variables by running the setup script:type the command ```source setup.sh``` or ```bash setup.sh``` depending on your system.
- Use the command ```flask run --reload``` or ```python app.py``` to start the server
- Check that it is running by typing ```localhost:5000``` or ```localhost:8080``` into your browser address bar and pressing Enter.
### Testing
- To use our sample database and test file, run the following commands from within the project directory (remember to start the virtual environment first):
  ```
  dropdb chocolate && createdb chocolate
  psql -U postgres chocolate<chocolate.psql
  source setup.sh
  python test_app.py
  ```
  **Troubleshooting**: Sometimes importing a database backup can cause "null violation constraint" or other primary key errors, because it can interfere with sequencing. To reset the sequence enter the following commands from within the project directory: (replace 'chocolate' with 'chocolate_test' if restoring that database for testing)
  ```
  psql chocolate postgres
  ```
  - (enter 'postgres' as the password)
  ```
  SELECT SETVAL((SELECT PG_GET_SERIAL_SEQUENCE('"Chocolate"', 'id')), (SELECT (MAX("id") + 1) FROM "Chocolate"), FALSE);
  SELECT SETVAL((SELECT PG_GET_SERIAL_SEQUENCE('"Chocolatier"', 'id')), (SELECT (MAX("id") + 1) FROM "Chocolatier"), FALSE);
  ```
  Source: 'SommerEngineering' on Stack Overflow: https://stackoverflow.com/questions/4448340/postgresql-duplicate-key-violates-unique-constraint


## How to Contribute

- In addition to contacting us directly with suggestions, you can also make a pull request to share solutions and bugs that you have discovered while experimenting with our app locally.
- Free Code Camp offers a good tutorial on how to do a pull request (steps 6-8): https://www.freecodecamp.org/news/how-to-make-your-first-pull-request-on-github-3/
- Support our mission by spreading the word about our app and shopping with a chocolate maker near you!