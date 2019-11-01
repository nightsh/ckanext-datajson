from __future__ import print_function

import os
import json
import re
import copy
import urllib

import SimpleHTTPServer
import SocketServer
from threading import Thread

PORT = 8998


class MockDataJSONHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        # test name is the first bit of the URL and makes CKAN behave
        # differently in some way.
        # Its value is recorded and then removed from the path
        self.test_name = None
        self.sample_datajson_file = None
        self.samples_path = 'datajson-samples'
        if self.path == 'http://127.0.0.1:%s/arm' % PORT:
            self.sample_datajson_file = 'arm.data.json'
            self.test_name = 'arm'
        elif self.path == 'http://127.0.0.1:%s/usda' % PORT:
            self.sample_datajson_file = 'usda.gov.data.json'
            self.test_name = 'usda'
        elif self.path == 'http://127.0.0.1:%s/404' % PORT:
            self.test_name = 'e404'
            self.respond('Not found', status=404)
        elif self.path == 'http://127.0.0.1:%s/500' % PORT:
            self.test_name = 'e500'
            self.respond('Error', status=500)
        
        if self.sample_datajson_file is not None:
            self.respond_json_sample_file(file_path=self.sample_datajson_file)

        if self.test_name == None:
            self.respond('Mock DataJSON doesnt recognize that call', status=400)

    def respond_json(self, content_dict, status=200):
        return self.respond(json.dumps(content_dict), status=status,
                            content_type='application/json')
    
    def respond_json_sample_file(self, file_path, status=200):
        pt = os.path.join(self.samples_path, file_path)
        data = json.load(open(pt, 'r'))
        return self.respond(data, status=status,
                            content_type='application/json')

    def respond(self, content, status=200, content_type='application/json'):
        self.send_response(status)
        self.send_header('Content-Type', content_type)
        self.end_headers()
        self.wfile.write(content)
        self.wfile.close()


def serve(port=PORT):
    '''Runs a CKAN-alike app (over HTTP) that is used for harvesting tests'''

    # Choose the directory to serve files from
    # os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),
    #                      'mock_ckan_files'))

    class TestServer(SocketServer.TCPServer):
        allow_reuse_address = True

    httpd = TestServer(("", PORT), MockDataJSONHandler)

    print('Serving test HTTP server at port {}'.format(PORT))

    httpd_thread = Thread(target=httpd.serve_forever)
    httpd_thread.setDaemon(True)
    httpd_thread.start()
