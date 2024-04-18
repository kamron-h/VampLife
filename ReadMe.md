

# VampLife
#### A Flask-based Web Application for determining the probability of students being a vampire based on user input.

---------------------------
## Authors
Kamron Hopkins - hopkinsk19@students.ecu.edu \
Mehki Corpening - corpeningm19@students.ecu.edu \
Robert Fernald - fernaldr16@students.ecu.edu

---------------------------

## Description

* This is a Python based application that takes the input of multiple user responses to determine the probability of the user being a vampire. The application uses a Bayesian model to calculate the probability based on the user's responses to questions about vampire-related activities and characteristics. The application provides a fun and interactive way to engage with users and generate personalized results based on their input. Many people have been bitten, do you possess vampire-like blood? Find out now!


[//]: # (!PDF Research Assistant WebApp Diagram]&#40;./docs/PDF-LangChain.jpg&#41;)

----------------------------------

## Installation

### Prerequisites

* Python 3.12 ([https://www.python.org/downloads/](https://www.python.org/downloads/))
* pip (usually installed with Python)

### Steps
 
1. **Create a virtual environment (recommended):**

    ```bash
    python3 -m venv env 
    source env/bin/activate
    ```
    
* If you're using Windows, the activation command is:
    
    ```powershell
    .\venv\Scripts\Activate.ps1
    ```

2. **Install dependencies:**

     ```bash
    pip install -r requirements.txt
    ```

3.  **Create a `.env` file AND add your Redis Database credentials inside the `.env` file.
-  **The `.env` file should be in the root directory of the project.**

    ```bash
    # Input your Redis URL, Host, Port, Password, and User in the .env file
    REDIS_URL=<YOUR_REDIS_URL>
    REDIS_HOST=<YOUR_HOST>
    REDIS_PORT=<YOUR_PORT>
    REDIS_PASSWORD=<YOUR_REDIS_PASSWORD>
    REDIS_USER=<YOUR_REDIS_DB_USERNAME>

    SECRET_KEY=NC2K-4-otNReI54u3ihf-g  # Change this to a random string, if desired...
    ```
---------------------------

### Running the Application

1.  **Make sure your virtual environment is activated (if you created one).**

2.  **Start the Flask development server:**

    ```bash
    flask run
    ```

    * This typically starts the app at: http://127.0.0.1:5000/

---------------------------

### Usage

To use the Vampire Bloodline App, follow these steps:

* Open the provided URL (e.g.,  http://127.0.0.1:5000/) in your web browser.

1. Navigate to the "Are You Vamp?" page.

2. Fill out the form with your responses to the questions.

3. Submit the form to see your results.

4. Additionally, you can test multiple users and view the results of all user's on the "Results" page.



### Important Points:

* **Redis Configuration:** The above example assumes Redis is running on localhost with the default port 6379. Adjust these settings as necessary.
* **Session Management:** We’re using Flask’s session.sid as the Redis key for storing each user’s vectorstore. Ensure your Flask session is securely configured.

------------------------

## Contributing
This repository is intended for educational purposes and does not accept further contributions.