from httpx import Response as HttpxResponse


class RaifPayError(BaseException):
    def __init__(self, response: HttpxResponse, *args, **kwargs):
        self.status_code = response.status_code
        if "message" in response.text:
            self.text = response.json()["message"]
        else:
            self.text = response.text
        self.response = response
        super().__init__(f"(code={self.status_code}) {self.text}", *args)
