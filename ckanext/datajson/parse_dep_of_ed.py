"""
Temporal fixes to fit the Dep of Ed schema
"""
import logging
import ckan.model as model
log = logging.getLogger(__name__)


def parse_datajson_entry_for_dep_of_ed_schema(datajson, package, defaults, schema_version):
  # temporal FIX
  log.info('Parsing datajson entry for dep of ed : {}'.format(package))

  is_private = package.get('private', False)
  package['private'] = is_private
  
  if schema_version == '1.1':
    author_email = package.get('contact_email', 'missing@email.com')
    author = package.get('contact_name', 'Unknown author')
  elif schema_version == '1.0':
    author_email = package.get('maintainer_email', 'missing@email.com')
    author = package.get('maintainer', 'Unknown author')
    
  package['author'] = author
  package['author_email'] = author_email

  # require vocabularies created !
  # paster --plugin=ckanext-ed ed create_ed_vocabularies

  spatial = package.get('spatial', 'United States')
  package['spatial'] = spatial

  log.info('Finished Parsing datajson entry for dep of ed : {}'.format(package))