from src.helper import log
from src.helper.messages.validationMessage import ValidationMessage
from src.helper.validators.validatorsEnum import AllowedPath

MESSAGE = ValidationMessage

logger = log.setup_custom_logger()


class Validator(object):

    __allowedPaths__ = {
        'path_1': {
            'nullable_param': True,
            'allowed_params': [
                'param_1',
                'param_2',
                'param_3'
            ],
            'allowedMethods': [
                'GET'
            ]
        },
        'path_2': {
            'nullable_param': True,
            'allowed_params': [
                'param_1',
                'param_2'
            ],
            'allowedMethods': [
                'GET'
            ]
        },
        'path_3': {
            'nullable_param': False,
            'allowed_params': [
                'param_3'
            ],
            'allowedMethods': [
                'GET'
            ]
        }
    }

    __singleParam__ = {
        'customer_id': {
            'type': str,
            'numeric': True,
            'alpha': False,
            'length': 6,
            'strict_values': None
        },
        'accepted': {
            'type': str,
            'numeric': False,
            'alpha': True,
            'strict_values': ['s', 'n']
        },
        'document': {
            'type': str,
            'numeric': True,
            'alpha': False,
            'length': 14,
            'min_length': 11
        }
    }

    __multiParam__ = {
        'product_id': {
            'type': str,
            'numeric': False,
            'alpha': True,
            'length': 6
        },
        'address': {
            'type': str,
            'numeric': False,
            'alpha': True
        },
        'param_3': 'value_3'
    }

    def __init__(self, event):
        self.path = event['path']
        self.method = event['httpMethod']
        self.single_param = event['queryStringParameters']
        self.array_string = event['multiValueQueryStringParameters']

    def __get_path__(self):
        logger.info(msg='get_path')
        # return next((path for path in self.__allowedPaths__ if path == self.path), 'ValueError')
        return self.__allowedPaths__.get(self.path, 'ValueError')

    def __is_null_parameters__(self) -> bool:
        logger.info(msg='check_null_params')
        return self.single_param is None or self.array_string is None

    def __allows_null_param_path__(self, path) -> bool:
        logger.info(msg='check_nullable_param_path')
        allows = self.__allowedPaths__.get(path)['nullable_param']
        null = self.__is_null_parameters__()
        return True if allows else not null

    def __is_allowed_http_method__(self, method, path):
        logger.info(msg='check_http_method_validity')
        return True if method.upper() in self.__allowedPaths__[path]['allowedMethods'] else False

    def check_parameters(self):
        if self.__get_path__() == 'ValueError':
            raise Exception(MESSAGE.INVALID_ENDPOINT.value)
        if not self.__is_allowed_http_method__(self.method, self.path):
            raise Exception(MESSAGE.INVALID_HTTP_METHOD.value)
        if not self.__allows_null_param_path__(self.path):
            raise Exception(MESSAGE.NON_NULL_PARAM.value)

        query = []
        params = AllowedPath[self.path].value['allowed_params']

        for key in self.array_string:
            if key not in params:
                raise Exception(MESSAGE.INVALID_PARAM_KEY.value.format(key))
            else:
                query.append({
                    key: self.single_param[key]
                })

        # for key, values in self.array_string:
        #
        #     for value in values:
        #         if value in self.__multiParam__:
        #
        #     query.append({key: values})

        return self.path, query
