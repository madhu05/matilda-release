import logging

from flask import request
from flask_restplus import Resource

from matilda_release.api.v2.restplus import api
from matilda_release.api.v2.model.model import release_link, release_link_items
from matilda_release.api.v2.handler import release_link_handler

log = logging.getLogger(__name__)

ns = api.namespace('rls', description='Operations related to Release')

@ns.route('/release/<int:release_id>/links')
class ReleaseLinksCollection(Resource):

    @api.marshal_list_with(release_link, skip_none=True)
    def get(self, release_id):
        """
        Returns list of releases.
        """
        resp = release_link_handler.get_release_links(release_id)
        return resp

    @api.response(201, 'Release successfully created.')
    @api.expect(release_link)
    def post(self, release_id):
        data = request.json
        print ('Incomig request {}'.format(data))
        release_link_handler.create_release_link(release_id, data)
        return None, 201


@ns.route('/release/<int:release_id>/link/<int:link_id>/items')
@api.response(404, 'Release not found.')
class ReleaseLinkItem(Resource):

    @api.marshal_with(release_link_items, skip_none=True)
    def get(self, release_id, link_id):
        """
        Returns release details.
        """
        resp = release_link_handler.get_release_link_item(release_id, link_id)
        return resp

    @api.response(201, 'Release Link Item successfully created.')
    @api.expect(release_link_items)
    def post(self, release_id, link_id):
        data = request.json
        print ('Incomig request {}'.format(data))
        release_link_handler.create_release_link_item(link_id, data)
        return None, 201

    @api.expect(release_link_items)
    @api.response(204, 'Release successfully updated.')
    def put(self, id):

        data = request.json
        #update_category(id, data)
        return None, 204

    @api.response(204, 'Release successfully deleted.')
    def delete(self, id):
        #delete_category(id)
        return None, 204
