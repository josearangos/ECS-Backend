import storage as st
collectors_db = st.connect()
class Collector:
    def __init__(self, _id=None, id=None, fullName=None, cellphone=None, password=None):
        self._id = _id
        self.id = id
        self.fullName = fullName
        self.cellphone = cellphone
        self.password = password
    def get(self, _id):
        collector = collectors_db.collectors.find_one({'id': _id},{'_id': False})
        if collector:
            return collector
        else:
            return None