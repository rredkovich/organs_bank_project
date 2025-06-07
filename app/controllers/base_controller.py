class BaseAppController:
    def __init__(self, app_model_klass, app_view_klass, parent):
        self.model = app_model_klass()
        self.view = app_view_klass(parent, self)
        self.view.pack(fill='both', expand=True)
        self.refresh()

    def refresh(self):
        self.view.populate()
        
    def open_detail(self, *args, **kwargs):
        raise Exception("Not implemented")

    def save(self, *args, **kwargs):
        self.model.save(*args, **kwargs)
        self.refresh()