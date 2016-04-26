# -*- coding: utf-8 -*-

# Copyright (c) 2016, Wei Tao. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
 
import requests
import json
import time
from service import LocalService 

url_logstash = 'http://10.10.2.231:1109'
ps = LocalService()
class PsRunner(): 
    def run(self):
       # res = {}
        cpu_list = []
        disk_list = []
        #ps = LocalService()
        ps_cpu = ps.get_cpu()
        ps_mem = ps.get_mem()
        ps_disk = ps.get_disk()
        ps_net = ps.get_net()
        cpu_count = len(ps_cpu)
        disk_count = len(ps_disk)
        for x in range(cpu_count):
            cpu_list.append('cpu'+str(x+1))
        for d in range(disk_count): 
            ps_disk[d]['space_used'] = round(ps_disk[d]['space_used']/1024/1024/float(1024),2) 
            ps_disk[d]['space_total'] = round(ps_disk[d]['space_total']/1024/1024/float(1024),2) 
            disk_list.append('disk'+str(d+1))
        cpu_zip = zip(cpu_list,ps_cpu)
        disk_zip = zip(disk_list,ps_disk)
        cpus = dict(cpu_zip)
        mem = round(ps_mem.available/1024/1024/float(1024),2)
        disks = dict(disk_zip)
        net = ps_net
        res = {
          'hostname': ps.get_node(),
          'service' : '', 
          'cpu_pct' : cpus,
          'mem_avb' : mem,
          'disk'    : disks,
          'net'     : net
         }
        res_json = unicode(str(res), errors='ignore')
        print json.dumps(res)
        #return res
        r = requests.post(url_logstash,data=json.dumps(res)) 
        return r
def main():
    r = PsRunner()
    while True:
       r.run()
       time.sleep(30)
if __name__ == '__main__':
    main()
         
