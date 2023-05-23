from flask import redirect, request, url_for
from . import clients
from app.models import BaseResponse
from app.decorators import login_required
from app.utils import jwt_functions

from sqlalchemy import or_
from datetime import datetime

from snowflake import SnowflakeGenerator
from app import client_manager

@clients.route('/', methods=['GET'])
def get_online_clients_list():
	
	return BaseResponse(data={'count': client_manager.get_user_count(), 'users': client_manager.USER_TABLE, 'sid_table': client_manager.SID_TABLE}).dict()