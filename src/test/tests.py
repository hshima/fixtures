import pytest

from src.helper.LambdaResponse import LambdaResponse
from src.helper.Validator import Validator
from src.lambda_function import lambda_handler


class Fruit:
    def __init__(self, name):
        self.name = name
        self.cubed = False

    def __eq__(self, other):
        return self.name == other.name

    def cube(self):
        self.cubed = True


@pytest.fixture
def my_fruit():
    return Fruit("apple")


@pytest.fixture
def fruit_basket(my_fruit):
    return [Fruit("banana"), my_fruit]


def test_my_fruit_in_basket(my_fruit, fruit_basket):
    assert my_fruit in fruit_basket


def test_any_test():
    assert not False


@pytest.fixture
def banana():
    return Fruit("banana")


def test_exists_banana(banana, fruit_basket):
    assert banana in fruit_basket


@pytest.mark.parametrize("foo,bar", [
    (1, 1),
    (2, 2),
    (3, 3),
])
def test_true(foo, bar):
    assert foo == bar


class FruitSalad:

    def __init__(self, *fruit_bowl):
        self.fruit = fruit_bowl
        self._cube_fruit()

    def _cube_fruit(self):
        for fruit in self.fruit:
            fruit.cube()


# Arrange
@pytest.fixture
def fruit_bowl():
    return [Fruit("apple"), Fruit("banana")]


def test_fruit_salad(fruit_bowl):
    # Act
    fruit_salad = FruitSalad(*fruit_bowl)

    # Assert
    assert all(fruit.cubed for fruit in fruit_salad.fruit)


def test_lambda_handler_error():
    event = {
        'path': 'path_10',
        'httpMethod': 'GET',
        'queryStringParameters': 'key_1',
        'multiValueQueryStringParameters': ['key_1']
    }

    response = lambda_handler(event)

    assert response == {
        "statusCode": 400,
        "headers": {
            "Content-Type": "application/json"
        },
        "isBase64Encoded": False,
        "body": 'Endpoint inválido.'
    }


def test_validator_error():
    event = {
        'path': 'path_10',
        'httpMethod': 'GET',
        'queryStringParameters': 'key_1',
        'multiValueQueryStringParameters': ['key_1']
    }

    try:
        response = Validator(event).check_parameters()
    except Exception as e:
        erro = LambdaResponse.bad_request(400, e.args[0])

    assert erro == {
        "statusCode": 400,
        "headers": {
            "Content-Type": "application/json"
        },
        "isBase64Encoded": False,
        "body": 'Endpoint inválido.'
    }


def test_validator_error_null_param():
    event = {
        'path': 'path_3',
        'httpMethod': 'GET',
        'queryStringParameters': None,
        'multiValueQueryStringParameters': [None]
    }

    try:
        response = Validator(event).check_parameters()
    except Exception as e:
        erro = e.args[0]

    assert erro == 'Este método não aceita consultas sem parâmetros.'


def test_validator_success_null_param():
    event = {
        'path': 'path_1',
        'httpMethod': 'GET',
        'queryStringParameters': {'param_1': 'value_1'},
        'multiValueQueryStringParameters': {'param_1': ['value_1', 'value_2']}
    }

    try:
        response = Validator(event).check_parameters()
    except Exception as e:
        erro = e.args[0]

    assert response == ('path_1', [{'param_1': 'value_1'}])


def test_invalid_http_method():
    event = {
        'path': 'path_1',
        'httpMethod': 'POST',
        'queryStringParameters': {'param_1': 'value_1'},
        'multiValueQueryStringParameters': {'param_1': ['value_1', 'value_2']}
    }
    try:
        response = Validator(event).check_parameters()
    except Exception as e:
        erro = e.args[0]

    assert erro == 'Método não permitido para o endpoint.'
