class GuiState:
    def __init__(self) -> None:
        self._state_vars = dict()
        self._call_backs = dict()

    def __getitem__(self, key: str):
        return self.get(key)

    def get(self, key: str):
        return self._state_vars.get(key)

    def __setitem__(self, key: str, value):
        old_item = self.get(key)
        self.set(key, value)

    def set(self, key: str, value):
        self[key] = value
