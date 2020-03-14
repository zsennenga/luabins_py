import json


class LuaTableKey:
    def __init__(self, inner):
        self.inner = inner

    def __hash__(self):
        return json.dumps(self.inner).__hash__()

    def __eq__(self, other):
        return other.__hash__() == self.__hash__()
