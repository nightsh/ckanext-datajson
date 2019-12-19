# Test this extension

One way to run a CKAN environment with this extension is to use the [docker-ckan](https://github.com/okfn/docker-ckan) project and add manually this extensions.

```yml
volumes:
      - ./src:/srv/app/src_extensions
      - ckan_storage:/var/lib/ckan
      # to debug extensions
      # ckanext-harvest is required
      - /home/user/your-code-folder/ckanext-harvest:/srv/app/src_extensions/ckanext-harvest
      # this ckanext-datajson extension
      - /home/user/your-code-folder/ckanext-datajson:/srv/app/src_extensions/ckanext-datajson
```

You also going to need to initialize the harvester database as an entrypoint command.

```
paster --plugin=ckanext-harvest harvester initdb --config=$CKAN_INI
```

If you run this environment you will be able to add and use harvest soures at: http://ckan:5000/harvest
```
docker-compose -f docker-compose.dev.yml up --build
```

Then you can run tests inside the CKAN container:
```
docker-compose -f docker-compose.dev.yml exec ckan-dev bash
cd src_extensions/ckanext-datajson/
nosetests --ckan --with-pylons=test.ini ckanext/datajson

# run specific test
nosetests --ckan --with-pylons=test.ini ckanext/datajson/tests/test_datajsonharvester.py:TestDataJSONHarvester.test_datason_usda
```

