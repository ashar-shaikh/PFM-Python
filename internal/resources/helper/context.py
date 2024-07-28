import uuid


class Context:
    def __init__(self, trace_id=None, **kwargs):
        self.trace_id = trace_id or str(uuid.uuid4())
        self.data = kwargs

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        self.data[key] = value
