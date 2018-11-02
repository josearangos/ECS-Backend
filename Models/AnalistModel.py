import storage as st
analist_db = st.connect()
class Analist:
    def __init__(self, _id=None, id=None, password=None):
        self._id = _id
        self.id = id
        self.password = password
    def get(self, _id):
        analist = analist_db.analists.find_one({'id': _id})
        if analist:
            self.__init__(**analist)
            return self
        else:
            return None