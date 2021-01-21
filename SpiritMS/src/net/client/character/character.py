class Character:
    def __init__(
            self,
            id=0,
            acc_id=0,
            client=None
    ):
        # Database attributes
        self._id = id
        self._acc_id = acc_id

        # Non-Database attributes
        self._client = client

    @property
    def id(self):
        return self._id
