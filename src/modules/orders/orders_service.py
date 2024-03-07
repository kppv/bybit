from models.dto import BaseSignal


class OrderService:
    def make_order_by_signal(self, signal: BaseSignal):
        pass
        # TODO check if some order already exits
        # TODO create order
        # TODO send order to bybit


order_service = OrderService()
