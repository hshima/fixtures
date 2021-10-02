
class LambdaResponse(object):

    @staticmethod
    def bad_request(status_code, body):
        return {
            "statusCode": status_code,
            "headers": {
                "Content-Type": "application/json"
            },
            "isBase64Encoded": False,
            "body": body
        }
