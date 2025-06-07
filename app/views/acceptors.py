from .base_view import BaseAppListView, PersonBaseDetailAppView


class AcceptorAppListVeiw(BaseAppListView):
    def __init__(self, parent, controller, columns, double_click_callback):
        super().__init__(parent, controller, columns, double_click_callback)


class AcceptorAppDetailsView(PersonBaseDetailAppView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

