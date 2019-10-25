#!/bin/sh -e

echo "TESTING ckanext-datajson"
# nosetests --ckan --nologcapture --with-pylons=subdir/test.ini --reset-db --with-coverage --cover-package=ckanext.datajson --cover-inclusive --cover-erase --cover-tests

nosetests --ckan --nologcapture --with-pylons=subdir/test.ini ckanext.datajson 