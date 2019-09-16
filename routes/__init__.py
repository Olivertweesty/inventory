from flask import Blueprint
routes = Blueprint('routes', __name__)

from .warehouse import *
from .pointofsale import *
from .management import *