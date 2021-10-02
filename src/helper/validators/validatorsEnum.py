from enum import Enum


class AllowedPath(Enum):
    path_1 = {
        'nullable_param': True,
        'allowed_params': [
            'param_1',
            'param_2',
            'param_3'
        ],
        'allowedMethods': [
            'GET'
        ]
    }
    path_2 = {
        'nullable_param': True,
        'allowed_params': [
            'param_1',
            'param_2'
        ],
        'allowedMethods': [
            'GET'
        ]
    }
    path_3 = {
        'nullable_param': False,
        'allowed_params': [
            'param_3'
        ],
        'allowedMethods': [
            'GET'
        ]
    }
