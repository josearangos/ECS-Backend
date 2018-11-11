import storage as st
analist_db = st.connect()
from bson.json_util import dumps
class Analist:
    def __init__(self, _id=None, id=None, fullName=None, password=None, state=None):
        self._id = _id
        self.id = id
        self.fullName = fullName
        self.password = password
        self.state = state
    def get(self, _id):
        analist = analist_db.analists.find_one({'id': _id}, {'_id': False})
        if analist:
            return analist
        else:
            return None
    def insert(self, id, fullName, password, state):
        analist = {
            "id": id,
            "fullName": fullName,
            "password": password,
            "state": state
        }
        res = analist_db.analists.insert_one(analist)
        return res