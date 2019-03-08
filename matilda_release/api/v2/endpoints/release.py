import logging

from flask import request
from flask_restplus import Resource
from werkzeug.exceptions import BadRequest
from matilda_release.api.v2.restplus import api
from matilda_release.api.v2.model.model import release, release_params, release_with_artifacts, release_type, \
    platforms_with_os, vnf_node_type_with_sites, rls_clone, \
    operating_system, infra_release_impacted_systems, release_names, release_count, status
from matilda_release.api.v2.handler import release_handler
from matilda_release.util.status_helper import ReleaseTypeCdDefinition as rls_type_cd

log = logging.getLogger(__name__)

ns = api.namespace('rls', description='Operations related to Release')

@ns.route('/releases')
class ReleaseCollection(Resource):

    @api.marshal_list_with(release_params, skip_none=True)
    def get(self):
        """
        Returns list of releases.
        """
        release_type_cd = request.args.get('release_type_cd', None)
        if release_type_cd is None or release_type_cd == 'NULL' or len(release_type_cd)==0:
            release_type_cd = rls_type_cd.application.release_type_cd
        else:
            try:
                release_type_cd = int(release_type_cd)
            except:
                raise BadRequest('release type code not int {}'.format(release_type_cd))

        resp = release_handler.get_release(release_id=None, release_type_cd=release_type_cd)

        return resp

    @api.response(201, '', release_params)
    @api.expect(release_params)
    def post(self):
        data = request.json
        resp = release_handler.create_release(data)

        return resp

@ns.route('/release/<int:release_id>/clone')
@api.response(404, 'Release not found.')
class CloneRelease(Resource):
    @api.expect(rls_clone)
    def post(self, release_id):
        try:
            data = request.json
            resp = release_handler.clone_release(release_id, data.get('name'),data.get('release_dt'))
        except:
            raise BadRequest('Clone release failed release id {}'.format(release_id))
        return resp

@ns.route('/release_count')
class ReleaseCount(Resource):

    @api.marshal_list_with(release_count, skip_none=True)
    def get(self):
        try:
            resp = release_handler.get_release_count()
        except:
            raise BadRequest('Get release count failed {}'.format(release_count))
        return resp

@ns.route('/release_type_cd/<int:release_type_cd>/status')
class ReleaseCount(Resource):

    @api.marshal_list_with(status, skip_none=True)
    def get(self,release_type_cd):
        try:
            resp = release_handler.get_status_count(release_type_cd=release_type_cd)
        except:
            raise BadRequest('Get release status failed {}'.format(status))
        return resp

@ns.route('/release_types')
class ReleaseTypeCollection(Resource):

    @api.marshal_list_with(release_type, skip_none=True)
    def get(self):
        try:
            resp = release_handler.get_release_type()
        except:
            raise BadRequest('Get release type failed {}'.format(release_type))
        return resp


@ns.route('/release/<int:release_id>')
@api.response(404, 'Release not found.')
class ReleaseItem(Resource):

    @api.marshal_with(release_with_artifacts, skip_none=True)
    def get(self, release_id):
        """
        Returns release details.
        """
        release_type_cd = request.args.get('release_type_cd', None)
        if release_type_cd is None or release_type_cd == 'NULL' or len(release_type_cd)==0:
            releases_type_cd = rls_type_cd.application.release_type_cd
        else:
            try:
                release_type_cd = int(release_type_cd)
            except:
                raise BadRequest('release type code not int {}'.format(release_type_cd))
                #print('release type code not int')
                release_type_cd = None
        try:
            resp = release_handler.get_release(release_id=release_id, release_type_cd=release_type_cd, filters=None, extended=True)
        except:
            raise BadRequest('Get release failed - release_id {} '.format(release_id))

        return resp[0]

    @api.expect(release)
    @api.response(204, 'Release successfully updated.')
    def put(self, id):

        data = request.json
        #update_category(id, data)
        return None, 204

    @api.response(204, 'Release successfully deleted.')
    def delete(self, id):
        #delete_category(id)
        return None, 204

@ns.route('/release/<int:release_id>/status')
@api.response(404, 'Release Metrics not found')
class ReleaseMetrics(Resource):

    #@api.marshal_list_with(infra_release_impacted_systems,skip_none=True)
    def get(self, release_id):

        try:
            resp = release_handler.get_release_metrics(release_id=release_id)
        except:
            raise BadRequest('Get Release metrics failed {}',release_id)
        return resp



@ns.route('/release/<int:id>/vnf/impacted_systems')
# this method should be replaced with actual vnf
@api.response(404, 'Impacted Systems not found')
class ImpactedSystems(Resource):
    @api.marshal_with(infra_release_impacted_systems, skip_none=True)
    def get(self, id, release_type_cd):
        resp = release_handler.get_impacted_systems_vnf(release_id=id)
        return resp


@ns.route('/Platforms')
class PlatformCollection(Resource):

    @api.marshal_list_with(platforms_with_os, skip_none=True)
    def get(self):
        """
        Returns type of releases.
        """
        try:
            platform_id = request.args.get('platform_id', None)
            resp = release_handler.get_platform(platform_id)

        except:
            raise BadRequest('Get Platforms failed - platform_id {} '.format(platform_id))
        return resp

@ns.route('/OperatingSystems')
class OperatingSystemCollection(Resource):

    @api.marshal_list_with(operating_system, skip_none=True)
    def get(self):
        """
        Returns type of releases.
        """
        try:
            os_id = request.args.get('os_id', None)
            resp = release_handler.get_operating_system(os_id)
        except:
            raise BadRequest('Get operating systems failed - os_id {} '.format(os_id))
        return resp

@ns.route('/Vnfnodes')
class PlatformCollection(Resource):

    @api.marshal_list_with(vnf_node_type_with_sites, skip_none=True)
    def get(self):
        """
        Returns type of releases.
        """

        vnf_node_id = request.args.get('vnf_node_id', None)
        resp = release_handler.get_vnf_nodes(vnf_node_id)

        return resp


@ns.route('/releases/names')
class ReleaseNamesList(Resource):

    @api.marshal_with(release_names, skip_none=True)
    def get(self):
        try:
            return release_handler.get_release_name_list()
        except:
            raise BadRequest('Get release name list failed')


# release_handler.get_impacted_systems_for_platform(release_id=1)