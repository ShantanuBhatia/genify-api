from flask import Blueprint
from flask import request
from config import model_path
from config import api_url_base
from config import client_error_ret_code
import model_utils

recommender = Blueprint('recommender', __name__, url_prefix=api_url_base)


@recommender.route('/get_recc', methods=['GET', 'POST'])
def get_recommendation():
    # If it's a post request, read the post data directly, else if a GET request read the URL params
    if request.method == 'POST':
        payload = request.json
    else:
        payload = request.args
    recommendation_list, err_msg = model_utils.query_model(payload, model_path)

    if recommendation_list is None:
        return {
                   "err": err_msg
               }, client_error_ret_code
    return {
        "products": recommendation_list
    }
