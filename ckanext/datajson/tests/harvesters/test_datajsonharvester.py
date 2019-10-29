import copy

from nose.tools import assert_equal, assert_raises, assert_in
import json
from mock import patch, MagicMock, Mock
from requests.exceptions import HTTPError, RequestException

try:
    from ckan.tests.helpers import reset_db, call_action
    from ckan.tests.factories import Organization, Group
except ImportError:
    from ckan.new_tests.helpers import reset_db, call_action
    from ckan.new_tests.factories import Organization, Group
from ckan import model
from ckan.plugins import toolkit

# from ckanext.harvest.tests.factories import (HarvestSourceObj, HarvestJobObj,
#                                              HarvestObjectObj)
from ckanext.datajson.tests.factories import (HarvestSourceObj, HarvestJobObj,
                                             HarvestObjectObj)

import ckanext.harvest.model as harvest_model
from ckanext.harvest.harvesters.base import HarvesterBase
from ckanext.datajson.harvester_datajson import DataJsonHarvester

import mock_datajson_source

# Start data json sources server we can test harvesting against it
mock_datajson_source.serve()


class TestDataJSONHarvester(object):
    @classmethod
    def setup(cls):
        reset_db()
        harvest_model.setup()

    def run_source(self, url):
        source = HarvestSourceObj(url=url)
        job = HarvestJobObj(source=source)

        harvester = DataJsonHarvester()

        # gather stage
        print 'GATHERING'
        obj_ids = harvester.gather_stage(job)
        print job.gather_errors
        print obj_ids
        if len(obj_ids) == 0:
            # nothing to see
            return

        harvest_object = harvest_model.HarvestObject.get(obj_ids[0])
        print harvest_object.guid
        print harvest_object.content

        # fetch stage
        print 'FETCHING'
        result = harvester.fetch_stage(harvest_object)

        print harvest_object.errors
        print result

        # fetch stage
        print 'IMPORTING'
        result = harvester.import_stage(harvest_object)

        print harvest_object.errors
        print result
        print harvest_object.package_id
        dataset = model.Package.get(harvest_object.package_id)
        print dataset.name

    def test_datason_usda(self):
        url = 'https://www.archive.arm.gov/metadata/data.json'
        self.run_source(url=url)
    
    def test_datason_arm(self):
        url = 'http://www.usda.gov/data.json'
        self.run_source(url=url)
    
    def test_datason_404(self):
        url = 'http://some404/data.json'
        self.run_source(url=url)
        
    def test_datason_500(self):
        url = 'http://some500/data.json'
        self.run_source(url=url)
