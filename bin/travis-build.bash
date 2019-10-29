#!/bin/bash
set -e

echo "This is travis-build.bash..."

echo "Installing the packages that CKAN requires..."
sudo apt-get update -qq
sudo apt-get install solr-jetty libcommons-fileupload-java libpq-dev

pip install setuptools -U

if [ $CKANVERSION == '2.8' ]
then
	sudo apt-get install postgresql-9.6
elif [ $CKANVERSION == '2.3' ]
then
	sudo apt-get install postgresql-9.1
fi

echo "Installing CKAN and its Python dependencies..."
git clone https://github.com/ckan/ckan
cd ckan
if [ $CKANVERSION == '2.8' ]
then
	git checkout master
elif [ $CKANVERSION == '2.3' ]
then
	git checkout release-v2.3
fi
python setup.py develop
cp ./ckan/public/base/css/main.css ./ckan/public/base/css/main.debug.css
pip install -r requirements.txt
pip install -r dev-requirements.txt

cd -

echo "Setting up Solr..."
# solr is multicore for tests on ckan master now, but it's easier to run tests
# on Travis single-core still.
# see https://github.com/ckan/ckan/issues/2972
sed -i -e 's/solr_url.*/solr_url = http:\/\/127.0.0.1:8983\/solr/' ckan/test-core.ini
printf "NO_START=0\nJETTY_HOST=127.0.0.1\nJETTY_PORT=8983\nJAVA_HOME=$JAVA_HOME" | sudo tee /etc/default/jetty
sudo cp ckan/ckan/config/solr/schema.xml /etc/solr/conf/schema.xml
sudo service jetty restart


echo "Creating the PostgreSQL user and database..."
sudo -u postgres psql -c "CREATE USER ckan_default WITH PASSWORD 'pass';"
sudo -u postgres psql -c 'CREATE DATABASE ckan_test WITH OWNER ckan_default;'
sudo -u postgres psql -c 'CREATE DATABASE datastore_test WITH OWNER ckan_default;'

echo "Initialising the database..."
cd ckan
paster db init -c test-core.ini
cd -

cd ..
echo "Installing Harverter"
git clone https://github.com/ckan/ckanext-harvest
cd ckanext-harvest
if [ $CKANVERSION == '2.8' ]
then
	git checkout master
elif [ $CKANVERSION == '2.3' ]
then
	git checkout master
fi

python setup.py develop
pip install -r pip-requirements.txt
pip install -r dev-requirements.txt

cd -

echo "Installing ckanext-datajson and its requirements..."
cd ckanext-datajson
pip install -r pip-requirements.txt
python setup.py develop


echo "Moving test.ini into a subdir..."
mkdir subdir
mv test.ini subdir

echo "travis-build.bash is done."