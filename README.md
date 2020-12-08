## About

An API for recommending banking products based on customer info.

Built for [Genify](https://www.genify.ai)'s Software Developer interview assignment.

Dockerised into a Meinheld/Gunicorn server based off of [Miangolo's meinheld-gunicorn-flask image](https://hub.docker.com/r/tiangolo/meinheld-gunicorn-flask/)

### Built With

* [Flask](https://flask.palletsprojects.com/en/1.1.x/)
* [XGBoost](https://xgboost.ai/)

Based on code from a [reference Kaggle notebook](https://www.kaggle.com/sudalairajkumar/when-less-is-more)

With some basic styling on the example frontend with [min.css](http://mincss.com/)

## Getting Started

### Prerequisites
For development: [python3.8](https://www.python.org/downloads/release/python-383/)

For deployment: [Docker](https://www.docker.com/) to run the container

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/ShantanuBhatia/genify-api.git
   ```
2. Create a virtual environmennt and install dependencies
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
   
### Development

During development, use the Flask dev server:
   ```sh
   cd app/
   python main.py
   ```
The development server will serve to http://localhost:5000

For ease of use during development, a simple frontend for querying the api is provided at the base route.

### Docker Container Build

This application comes with a Dockerfile to build a container running a Gunicorn server for production.
To build the container, from the base folder run:
   ```sh
   docker build -t genapp ./
   ```
Once built, run the container with 
   ```sh
   docker run -d -p 80:80 genapp
   ```
This will serve at https://localhost

### Additional Notes

* At query time, the customer ID field is optional. 
* The provided Kaggle notebook seemed to have mistranslated "renta" as "rent" rather than "income", which from the Kaggle competition docs seems to be the correct translation. For clarity, the code refers to this field as income. 
* Moved all the hardcoded mapping data into a data_config.json file. Putting this into a database would be overkill for the scope of this assignment.

