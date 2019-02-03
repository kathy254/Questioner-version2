import re


class Validations:

    def is_empty(self, items):
        for item in items:
            if bool(item) is False:
                res = True
            else:
                res = False
            return res

    def is_whitespace_only(self, items):
        for item in items:
            if item.isspace() is True:
                res = True
            else:
                res = False
            return res

    def is_whitespace_exists(self, items):
        for item in items:
            if re.search(r"\s", item):
                res = True
            return res

    def is_string(self, items):
        for item in items:
            if type(item) is str:
                res = True
            else:
                res = False
            return res

    def is_integer(self, items):
        for item in items:
            if type(item) is int:
                res = True
            else:
                res = False
            return res

    def payload(self, items, length, keys):
        items = items.keys()
        if len(items) == length:
            for item in items:
                if item not in keys:
                    res = False
                else:
                    res = True
        else:
            res = False
        return res

    def valid_login_payload(self, items):
        res = self.payload(items, 2, ["username", "password"])
        return res

    def valid_signup_payload(self, items):
        res = self.payload(items, 7, ["first_name", "last_name", "other_name",
                           "email", "phone_number", "username", "password"])
        return res

    @staticmethod
    def valid_email(email):
        if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
                    email) is None:
            res = False
        else:
            res = True
        return res

    @staticmethod
    def valid_password(password):
        if len(password) < 6:
            res = False
        elif re.search(r"\s", password):
            res = False
        else:
            res = True
        return res
