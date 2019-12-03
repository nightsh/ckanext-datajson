import copy
from urllib2 import URLError
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
from ckan.lib.munge import munge_title_to_name
# from ckanext.harvest.tests.factories import (HarvestSourceObj, HarvestJobObj,
#                                              HarvestObjectObj)
from factories import (HarvestSourceObj,
                       HarvestJobObj,
                       HarvestObjectObj)

import ckanext.harvest.model as harvest_model
from ckanext.harvest.harvesters.base import HarvesterBase
from ckanext.datajson.harvester_datajson import DataJsonHarvester
import logging
log = logging.getLogger(__name__)

import mock_datajson_source


class TestDataJSONHarvester(object):
    
    @classmethod
    def setup_class(cls):
        log.info('Starting mock http server')
        mock_datajson_source.serve()

    @classmethod
    def setup(cls):
        # Start data json sources server we can test harvesting against it
        reset_db()
        harvest_model.setup()

    def run_source(self, url, limit=1):
        """ harvest a source 
        
        Params
        url: URL of the datajson harvest source
        limit: number of datasets to harvest
        """
        
        source = HarvestSourceObj(url=url)
        job = HarvestJobObj(source=source)

        harvester = DataJsonHarvester()

        # gather stage
        log.info('GATHERING %s', url)
        obj_ids = harvester.gather_stage(job)
        log.info('job.gather_errors=%s', job.gather_errors)
        log.info('obj_ids=%s', obj_ids)
        if len(obj_ids) == 0:
            # nothing to see
            return

        c = 0
        for obj_id in obj_ids:
            if c > limit:
                break
            harvest_object = harvest_model.HarvestObject.get(obj_id)
            log.info('ho guid=%s', harvest_object.guid)
            log.info('ho content=%s', harvest_object.content)

            # fetch stage
            log.info('FETCHING %s', url)
            result = harvester.fetch_stage(harvest_object)

            log.info('ho errors=%s', harvest_object.errors)
            log.info('result 1=%s', result)

            # fetch stage
            log.info('IMPORTING %s', url)
            result = harvester.import_stage(harvest_object)

            log.info('ho errors 2=%s', harvest_object.errors)
            log.info('result 2=%s', result)
            log.info('ho pkg id=%s', harvest_object.package_id)
            dataset = model.Package.get(harvest_object.package_id)
            log.info('dataset name=%s', dataset.name)

            yield harvest_object, result, dataset
            c += 1

    def test_datason_arm(self):
        url = 'http://127.0.0.1:%s/arm' % mock_datajson_source.PORT
        
        # just the firs one
        for harvest_object, result, dataset in self.run_source(url=url):
            expected_title = "NCEP GFS: vertical profiles of met quantities at standard pressures, at Barrow"
            assert_equal(dataset.title, expected_title)
            tags = [tag.name for tag in dataset.get_tags()]
            assert_in(munge_title_to_name("ORNL"), tags)
            assert_equal(len(dataset.resources), 1)
            break
    
    def test_datason_usda(self):
        url = 'http://127.0.0.1:%s/usda' % mock_datajson_source.PORT

        # just the firs one
        for harvest_object, result, dataset in self.run_source(url=url):
            expected_title = "Department of Agriculture Congressional Logs for Fiscal Year 2014"
            assert_equal(dataset.title, expected_title)
            tags = [tag.name for tag in dataset.get_tags()]
            assert_in(munge_title_to_name("Congressional Logs"), tags)
            assert_equal(len(dataset.resources), 1)
            break
    
    def test_datason_404(self):
        url = 'http://127.0.0.1:%s/404' % mock_datajson_source.PORT
        with assert_raises(URLError) as harvest_context:
            self.run_source(url=url)
        
    def test_datason_500(self):
        url = 'http://127.0.0.1:%s/500' % mock_datajson_source.PORT
        with assert_raises(URLError) as harvest_context:
            self.run_source(url=url)
        
    def test_datason_ed(self):
        url = 'http://127.0.0.1:%s/ed' % mock_datajson_source.PORT
        
        for harvest_object, result, dataset in self.run_source(url=url, limit=10):
            log.info('Dataset: {}'.format(dataset))
            tags = [tag.name for tag in dataset.get_tags()]
            log.info('Tags: {}'.format(tags))
            log.info('Result: {}'.format(result))
            
            if dataset.title == 'National Reporting System for Adult Education, 2007-08':
                assert 'adult-literacy' in tags
                assert 'annual-performance-report' in tags
                assert 'financial-reports' in tags
                assert 'ovaes-gpra-goals-for-adult-education' in tags