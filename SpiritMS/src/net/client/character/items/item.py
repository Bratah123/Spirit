class Item:
    def __init__(
            self,
            id_=0,
            item_id=0,
            bag_index=0,
            cash_item_serial_num=0,
            inv_type=None,
            quantity=1,
            is_cash=False,
            owner=""
    ):
        self._id = id_
        self._item_id = item_id
        self._bag_index = bag_index
        self._cash_item_serial_num = cash_item_serial_num
        self._date_expire = 0  # TODO Implement FileTime

        self._inv_type = inv_type
        self._quantity = quantity
        self._is_cash = is_cash
        self._owner = owner
