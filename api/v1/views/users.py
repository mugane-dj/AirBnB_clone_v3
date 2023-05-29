import hashlib
from models.base_model import BaseModel
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


class User(BaseModel):
    """User class"""
    def __init__(self, password=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.password = password

    def to_dict(self, save_to_disk=False):
        """Return a dictionary representation of the object"""
        dict_rep = super().to_dict()
        if not save_to_disk:
            dict_rep.pop('password', None)
        return dict_rep

    @property
    def password(self):
        """Getter method for password"""
        return self.__password

    @password.setter
    def password(self, value):
        """Setter method for password"""
        if value is not None:
            hashed_password = hashlib.md5(value.encode()).hexdigest()
            self.__password = hashed_password
        else:
            self.__password = None
