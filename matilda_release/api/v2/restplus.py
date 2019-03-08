import logging
import traceback

from flask_restplus import Api
from matilda_release.api.v2 import settings
from sqlalchemy.orm.exc import NoResultFound

log = logging.getLogger(__name__)

api = Api(version='1.0', title='Matilda Release API',
          description='Matilda release API')

#
# @api.errorhandler
# def default_error_handler(e):
#     log.error(traceback.print_exc())
#     #message = 'An unhandled exception occurred.'
#     return {'message': str(e)}, getattr(e, 'code', 400)

     # if not settings.FLASK_DEBUG:
    #     return {'message': message}, 400


@api.errorhandler(NoResultFound)
def database_not_found_error_handler(e):
    log.warning(traceback.format_exc())
    return {'message': 'A database result was required but none was found.'}, 404
