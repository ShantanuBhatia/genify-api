from typing import Dict
from typing import Union
import numpy as np
import xgboost as xgb
from config import target_cols
from config import prod_eng_map
from config import eng_to_esp_inputs
from config import missing_cols
from config import mapping_dict
from config import cat_cols


def fetch_model(mdl_path):
    mdl = xgb.Booster()
    try:
        mdl.load_model(mdl_path)
    except xgb.core.XGBoostError:
        return None, "Failed to load model"
    return mdl, None

def query_model(payload: Dict, model_path: str) -> Union[np.array, None]:
    """
    Take a JSON-derived dict of user data
    and return an array of recommendation indices
    """
    # Allowing a default customer ID value - it's not necessary to provide
    cust_id = payload.get('cust_id', 99)
    age = payload.get('age', None)
    gender = payload.get('gender', None)
    nationality = payload.get('nationality', None)
    seniority = payload.get('seniority', None)
    rel_type = payload.get('rel_type', None)
    activity_level = payload.get('activity_type', None)
    segment = payload.get('segment', None)
    income = payload.get('income', None)

    params = [cust_id, age, gender, nationality, seniority,
              rel_type, activity_level, segment, income]
    # don't make a prediction off incomplete data
    if not all(params):
        return None, "Required parameters not provided"

    # load the model
    mdl, err = fetch_model(model_path)
    if mdl is None:
        return None, err

    # Construct model-friendly array of parameters from the user input
    params, err_msg = payload_to_row(payload, eng_to_esp_inputs, missing_cols)
    if params is None:
        return None, err_msg

    # make predictions
    predictions, err_msg = row_to_predictions(params, mdl, target_cols, prod_eng_map)
    if predictions is None:
        return None, err_msg
    return predictions, None


def row_to_predictions(row, model, target_cols, prod_eng_map):
    try:
        input_arr = np.array([row])
        xgb_matrix = xgb.DMatrix(input_arr)
        raw_predictions = model.predict(xgb_matrix)
        pred_target_cols = np.array(target_cols[2:])
        argsorted_preds = np.argsort(raw_predictions, axis=1)
        preds = np.fliplr(argsorted_preds)[:, :7]
        pred_names = [list(pred_target_cols[pred]) for pred in preds][0]
        pred_names_english = [prod_eng_map[pred] for pred in pred_names]
    except Exception:
        # This is an overly broad exception clause, yes,
        # but I couldn't get this code to actually cause an error
        # I'm still not ruling out the possibility that it MIGHT error out given more rigorous testing,
        # in which case I'd probably rewrite this method to be stricter than just a giant try-catch
        return None, "Failed to generate product recommendations for given input"
    return pred_names_english, None


def payload_to_row(payload, eng_to_esp_inputs, missing_cols):
    """
    Take the data given in the GET request, dummy out non-provided fields
    And create an array of numerical values to be accepted by the model for making predictions
    """
    row_dict = {}
    for item in payload:
        row_dict[eng_to_esp_inputs[item]] = payload[item]
    for missing_col in missing_cols:
        row_dict[missing_col] = 'NA'
    processed_row, err_msg = process_row(row_dict, cat_cols)
    if processed_row is None:
        return None, err_msg
    return processed_row, None

def getIndex(row, col):
    val = row[col].strip()
    if val not in ['', 'NA']:
        ind = mapping_dict[col][val]
    else:
        ind = mapping_dict[col][-99]
    return ind


def get_age(row):
    min_age = 20.
    max_age = 90.
    range_age = max_age - min_age
    age = row['age'].strip()
    if age.isnumeric():
        age = float(age)
        if age < min_age:
            age = min_age
        elif age > max_age:
            age = max_age
        # return round((age - min_age) / range_age, 4)
        return age
    else:
        return None


def get_customer_seniority(row):
    min_value = 0.
    max_value = 256.
    range_value = max_value - min_value
    cust_seniority = row['antiguedad'].strip()

    if cust_seniority.isnumeric():
        cust_seniority = float(cust_seniority)
        if cust_seniority < min_value:
            cust_seniority = min_value
        elif cust_seniority > max_value:
            cust_seniority = max_value
        return round((cust_seniority - min_value) / range_value, 4)
    else:
        return None


def get_income(row):
    min_value = 0.
    max_value = 1500000.
    range_value = max_value - min_value
    income = row['renta'].strip()
    if income.isnumeric():
        income = float(income)
        if income < min_value:
            income = min_value
        elif income > max_value:
            income = max_value
        return round((income - min_value) / range_value, 6)
    else:
        return None


def process_row(row, cat_cols):
    x_vars = []
    # in the correct order, append the values for each of the categorical columns encoded values
    try:
        for col in cat_cols:
            x_vars.append(getIndex(row, col))
    except KeyError as key_error:
        return None, f"Invalid input: value '{key_error}' not recognized"
    # append the values for numeric value columns after checking that they are valid -
    # Age, Seniority, Income
    age, seniority, income = get_age(row), get_customer_seniority(row), get_income(row)
    if not all([age, seniority, income]):
        bad_fields = []
        if age is None:
            bad_fields.append("age")
        if seniority is None:
            bad_fields.append("seniority")
        if income is None:
            bad_fields.append("income")
        return None, f"Invalid input: expected numeric values for following field(s): {', '.join(bad_fields)}"
    x_vars += [age, seniority, income]
    # we don't know the existing products this user has so we dummy them out
    dummy_values = [0] * 22
    return x_vars + dummy_values, None
