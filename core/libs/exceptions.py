class FyleError(Exception):
    status_code = 400
    message = ""

    def __init__(self, status_code, message):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code

    def to_dict(self):
        res = dict()
        res["message"] = self.message
        res["status_code"] = self.status_code
        return res
