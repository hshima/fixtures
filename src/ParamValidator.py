class ParamValidator:

    def __init__(self):
        pass

    def validate_params(self, single_param, multi_param) -> (bool, dict):
        pass


class CartoesDisponiveis(ParamValidator):

    singleParam = {
        'key_1': 'value_1',
        'key_2': 'value_2',
        'key_3': 'value_3'
    }

    multiParam = {
        'key_1': 'value_1',
        'key_2': 'value_2',
        'key_3': 'value_3'
    }

    def validate_params(self, queryStringParameters, multiValueQueryStringParameters) -> (bool, dict):

        if single_param is None or multi_param is None:
            return False, {'message': 'Este método não aceita consultas sem parâmteros.'}

        single = self.singleParam.get(single_param)

        if single_param in

        for param in multi_param:
            if param in self.multiParam.get(param, False):
                pass
