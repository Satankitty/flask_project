from flask import Blueprint

psssport_blue = Blueprint('passport', __name__, url_prefix='/passport')

from . import views