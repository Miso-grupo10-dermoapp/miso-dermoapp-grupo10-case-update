import json

from datetime import date
from db_service import insert_item, get_item
from request_validation_utils import validate_body_params, validate_property_exist
from request_response_utils import return_error_response, return_status_ok

ENV_TABLE_NAME = "dermoapp-patient-cases"


def handler(event, context):
    try:
        print("lambda execution with context {0}".format(str(context)))
        if validate_query_params(event) and validate_property_exist('body', event):
            if validate_body_params(event['body']):
                response = update_case(event)
                return return_status_ok(response)
        else:
            return return_error_response("missing or malformed request body", 412)
    except FileNotFoundError as ex:
        return return_error_response("case not found: " + str(ex), 404)
    except Exception as err:
        return return_error_response("cannot proceed with the request error: " + str(err), 500)



def update_case(request):
    parsed_body = json.loads(request["body"])
    case_id = request['pathParameters']['case_id']

    case = get_item("case_id", case_id)
    if not case:
        raise FileNotFoundError("not found [case:{0}".format(case_id))
    case['status'] = parsed_body['status']
    case['creation_date'] = str(date.today())
    insert_item(case)
    return get_item("case_id", case_id)


def validate_query_params(request):
    return validate_property_exist("patient_id", request['pathParameters']) and \
        validate_property_exist("patient_id", request['pathParameters'])
