# import boto3
from aws_xray_sdk.core import patch_all
from aws_xray_sdk.core import xray_recorder

from src.helper import log
from src.helper.LambdaResponse import LambdaResponse
from src.helper.Validator import Validator

logger = log.setup_custom_logger()

patch_all()

# client = boto3.client('lambda')
# client.get_account_settings()


def lambda_handler(event, context=None):
    xray_recorder.begin_segment(name='start')
    logger.info(msg='begins_lambda')
    # validator = Validator(event)
    # path = validator.get_path()
    #
    # if path == 'ValueError':
    #     msg = 'Nenhum endpoint válido foi identificado'
    #     xray_recorder.end_segment()
    #     logger.error(msg=msg)
    #     return LambdaResponse.bad_request(400, msg)

    try:
        path, query = Validator(event).check_parameters()
    except Exception as e:
        msg = e.args[0]
        xray_recorder.end_segment()
        logger.error(msg=msg)
        return LambdaResponse.bad_request(400, msg)

    xray_recorder.end_segment()
