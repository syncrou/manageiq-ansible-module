#!/usr/bin/python
#
# (c) 2017, Daniel Korn <korndaniel1@gmail.com>
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#


import os
from manageiq_client.api import ManageIQClient


def manageiq_argument_spec():
    return dict(
        miq_url=dict(default=os.environ.get('MIQ_URL', None)),
        miq_username=dict(default=os.environ.get('MIQ_USERNAME', None)),
        miq_password=dict(default=os.environ.get('MIQ_PASSWORD', None), no_log=True),
        miq_verify_ssl=dict(require=False, type='bool', default=True),
        ca_bundle_path=dict(required=False, type='str', defualt=None)
    )


class ManageIQ(object):
    """
        class encapsulating ManageIQ API client
    """

    def __init__(self, module):
        """
            module         - an AnsibleModule instance
            url            - manageiq environment url
            user           - the username in manageiq
            password       - the user password in manageiq
            miq_verify_ssl - whether SSL certificates should be verified for HTTPS requests
            ca_bundle_path - the path to a CA_BUNDLE file or directory with certificates
        """

        for arg in ['miq_url', 'miq_username', 'miq_password']:
            if module.params[arg] in (None, ''):
                module.fail_json(msg="missing required argument: {}".format(arg))

        url            = module.params['miq_url']
        username       = module.params['miq_username']
        password       = module.params['miq_password']
        verify_ssl     = module.params['miq_verify_ssl']
        ca_bundle_path = module.params['ca_bundle_path']

        self.module  = module
        self.api_url = url + '/api'
        self.client  = ManageIQClient(self.api_url, (username, password), verify_ssl=verify_ssl, ca_bundle_path=ca_bundle_path)

    def find_collection_resource_by(self, collection_name, **params):
        """ Searches the collection resource by the collection name and the param passed

        Returns:
            the resource as an object if it exists in manageiq, None otherwise.
        """
        try:
            entity = self.client.collections.__getattribute__(collection_name).get(**params)
        except ValueError:
            return None
        except Exception as e:
            self.module.fail_json(msg="Failed to find resource {error}".format(error=e))
        return vars(entity)



