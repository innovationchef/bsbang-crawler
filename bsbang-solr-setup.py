#!/usr/bin/env python3

# XXX: DON'T USE FOR NOW, WE WILL LET SOLR ADD DOCUMENTS AUTOMATICALLY USING DISCOVERED TYPES INSTEAD
import json
import requests

solrPath = 'http://localhost:8983/solr/bsbang-dev-core/'
solrSchemaPath = solrPath + 'schema'

idFieldAddJson = {'add-field': {'name': 'identifier', 'type': 'string'}}
headers = {'Content-type': 'application/json'}

r = requests.post(solrSchemaPath, data=json.dumps(idFieldAddJson), headers=headers)
print('response [%s]' % r.text)