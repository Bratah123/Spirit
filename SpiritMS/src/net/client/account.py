class Account:
    def __init__(
            self,
            user=None,
            world_id=0
    ):
        self._id = 0
        self._world_id = 0

        self._characters = []

        self._trunk = None
        self._employee_trunk = None

        self._friends = []

        self._user = None
        self._current_chr = None

    @property
    def account_id(self):
        return self._id

    @property
    def world_id(self):
        return self._world_id

    @property
    def characters(self):
        return self._characters

    @property
    def user(self):
        return self._user

    @property
    def current_chr(self):
        return self._current_chr

    @property
    def trunk(self):
        return self._trunk

    @trunk.setter
    def trunk(self, new_trunk):
        self._trunk = new_trunk
