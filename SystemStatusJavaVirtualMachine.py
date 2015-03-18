"""SystemStatusJavaVirtualMachine.py

A Server Densitiy plugin for monitoring JVM statistics (i.e. memory use, threads, and garbage collection performance
via a REST service in a Grails project
"""

import logging
import json
import urllib2

__author__ = 'richardwooding'
__version__ = "1.0"
__date__ = "2015/03/18"
__copyright__ = "Copyright (c) 2015 42Engines"

class SystemStatusJavaVirtualMachine:
    def __init__(self, agentConfig, checksLogger, rawConfig):
        self.agentConfig = agentConfig
        self.checksLogger = checksLogger
        self.rawConfig = rawConfig



    def run(self):
        cfg = self.rawConfig["Main"]

        statsNames = cfg["system_stats_site_names"].split(',')
        statsUrls = cfg["system_stats_site_urls"].split(',')

        content = {}

        for idx in range(0, len(statsNames)):
            request = urllib2.Request(statsUrls[idx], headers={"Accept": "application/json"})
            content[statsNames[idx]] = json.load(urllib2.urlopen(request))
        return flatten(content)


def flatten(structure, key="", path="", flattened=None):
    if flattened is None:
        flattened = {}
    if type(structure) not in(dict, list):
        flattened[((path + "_") if path else "") + key] = structure
    elif isinstance(structure, list):
        for i, item in enumerate(structure):
            flatten(item, "%d" % i, "_".join(filter(None,[path,key])), flattened)
    else:
        for new_key, value in structure.items():
            flatten(value, new_key, "_".join(filter(None,[path,key])), flattened)
    return flattened

if __name__ == "__main__":
    testLogger = logging.getLogger("test")
    testLogger.setLevel(logging.DEBUG)
    stdErrHandler = logging.StreamHandler();
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stdErrHandler.setFormatter(formatter)
    testLogger.addHandler(stdErrHandler)

    rawConfig = { "Main" : {
        "system_stats_site_names" : "quirk,brandseye",
        "system_stats_site_urls" : "https://dali.quirk.biz/systemStatus,https://dali.brandseye.com/systemStatus"
        }
    }

    ssjvm = SystemStatusJavaVirtualMachine(None, testLogger, rawConfig)
    print ssjvm.run()
