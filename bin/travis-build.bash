#!/bin/bash
set -e

echo "This is travis-build.bash..."

echo "Installing the packages that CKAN requires..."
sudo apt-get update -qq
sudo apt-get install solr-jetty

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
pip install -r requirements.txt --allow-all-external
pip install -r dev-requirements.txt --allow-all-external

cd -

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
fi
elif [ $CKANVERSION == '2.3' ]
then
	git checkout master
fi

python setup.py develop
pip install -r pip-requirements.txt
cd -

echo "Installing ckanext-datajson and its requirements..."
cd ckanext-datajson
pip install -r pip-requirements.txt
python setup.py develop


echo "Moving test.ini into a subdir..."
mkdir subdir
mv test.ini subdir

echo "travis-build.bash is done."