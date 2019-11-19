# Testing extension

_paster_ creates some travis boilerprate for you when you create a new extension.  
Some examples:
 - https://travis-ci.org/ckan/ckanext-dcat 
 - https://travis-ci.org/ckan/ckanext-scheming

## Testing at harvester-base extension

The harvester base extension [includes testing for the harvest process](https://github.com/ckan/ckanext-harvest/blob/master/ckanext/harvest/commands/harvester.py#L417).  

With [Ckan Cloud docker](https://github.com/avdata99/ckan-cloud-docker/blob/master/.docker-compose.datagov-theme.yaml) repo we use like this:

```
docker-compose -f docker-compose.yaml \
    -f .docker-compose-db.yaml \
    -f .docker-compose.datagov-theme.yaml \
    run ckan /bin/bash
source /usr/lib/ckan/venv/bin/activate
# list harvest sources
paster --plugin=ckanext-harvest harvester sources --config /etc/ckan/production.ini
# check the job
paster --plugin=ckanext-harvest harvester jobs --config /etc/ckan/production.ini
# Run ALL jobs to the queue
paster --plugin=ckanext-harvest harvester run --config /etc/ckan/production.ini
# #### TEST (from harvestesr base)
# install some dev reqs
pip install factory-boy mock
# test source by ID
paster --plugin=ckanext-harvest harvester run_test onhir-test-200 --config /etc/ckan/production.ini
```

## Testing datajson extension

Running at [CircleCI](https://circleci.com/gh/datopian/ckanext-datajson)
```
#!/bin/sh -e

nosetests --ckan --with-pylons=subdir/test.ini ckanext/datajson 
```
