from functools import cache


class MissingType:

    @cache
    def __new__(cls):
        return super().__new__(cls)

    def __bool__(self):
        return False

    def __or__(self, other):
        return type(self) | other

    def __ror___(self, other):
        return other | type(self)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return 'Missing'


Missing = MissingType()