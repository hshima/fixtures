from enum import Enum


class ValidationMessage(Enum):
    INVALID_ENDPOINT = 'Endpoint inválido.'
    INVALID_HTTP_METHOD = 'Método não permitido para o endpoint.'
    NON_NULL_PARAM = 'Este método não aceita consultas sem parâmetros.'
    INVALID_PARAM_KEY = 'O parâmetro {0} não é permitido nesse endpoint'
