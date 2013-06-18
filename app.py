#!/usr/bin/python

import os
import sys

app_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(app_dir)
sys.path.insert(0, os.path.join(app_dir,'bottle'))

import bottle
import json
import subprocess
#import socket

@bottle.route('/locate')
@bottle.route('/locate/')
@bottle.route('/locate/:phrase')
def getResults(phrase = ""):
    jsonp = bottle.request.GET.get('callback') or "jsonp"

    response = {}

    p = subprocess.Popen('locate -i -d db_file "{0}"'.format(phrase), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    result = p.stdout.readlines()
    response["origCount"] = len(result)
    response["result"] = [x.strip() for x in result[:100]]
    response["count"] = len(response["result"])
    response["retval"] = p.wait()

    responseJSON = json.dumps(response, separators=(',',':'))
    return "{0}({1})".format(jsonp, responseJSON)


@bottle.route('/updatedb/')
@bottle.route('/updatedb')
def updatedb():
    jsonp = bottle.request.GET.get('callback') or "jsonp"
    
    response = {}
    p = subprocess.Popen('updatedb --prunepaths "/tmp /var/spool /home/.ecryptfs" -l 0 -o db_file -U /', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    response["retval"] = p.wait()

    responseJSON = json.dumps(response, separators=(',',':'))
    return "{0}({1})".format(jsonp, responseJSON)

# Do NOT use bottle.run() with mod_wsgi
#try:
bottle.run(host='0.0.0.0', port=8080)
#except socket.error:
#    print "There is already running some service on port 8080"
#    print "starting the browser anyway..."
#subprocess.call(["xdg-open","locati.html"])
