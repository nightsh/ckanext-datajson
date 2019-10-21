# Testing extension

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

Also this repo includes [the TestDatajsonPlugin class](https://github.com/akariv/ckanext-datajson/blob/datagov/ckanext/datajson/tests/test_datajson.py#L11). We need to analyze if this run with [the scripts](https://github.com/akariv/ckanext-datajson/blob/datagov/bin/travis-run.sh#L6) at the _bin_ folder.  

```
#!/bin/sh -e

echo "NO_START=0\nJETTY_HOST=127.0.0.1\nJETTY_PORT=8983\nJAVA_HOME=$JAVA_HOME" | sudo tee /etc/default/jetty
sudo cp ckan/ckan/config/solr/schema.xml /etc/solr/conf/schema.xml
sudo service jetty restart
nosetests --ckan --nologcapture --with-pylons=subdir/test.ini --reset-db --with-coverage --cover-package=ckanext.datajson --cover-inclusive --cover-erase --cover-tests
```
