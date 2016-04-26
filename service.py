# -*- coding: utf-8 -*-

# Copyright (c) 2016, Wei Tao. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

'''This is a tool collect system running info use psutil'''

import psutil
import requests
import json
import socket
import time

class LocalService():
    def __init__(self):
        self.old_net = {}
        self.old_time = None
    def get_cpu(self):
        return psutil.cpu_percent(interval=1,percpu=True)
    def get_mem(self):
        return psutil.virtual_memory()
    def get_node(self):
        return socket.gethostname()
    def get_disk(self):
        disks = []
        for dp in psutil.disk_partitions(False):
          try:
            usage = psutil.disk_usage(dp.mountpoint)
            disk = {
                'device': dp.device,
                'mountpoint': dp.mountpoint,
                'type': dp.fstype,
                'options': dp.opts,
                'space_total': usage.total,
                'space_used': usage.used,
                'space_used_percent': usage.percent,
                'space_free': usage.free
            }
            disks.append(disk)
          except StandardError, e:
            print e
        return disks
    def get_net(self):
        c = psutil.net_io_counters(pernic=False) 
        netifs = {}
        if not self.old_time:
            self.old_time = time.time()
        else:
            time_delta = time.time() - self.old_time
            print time_delta
        netifs['net'] = {
                'bytes_sent': c.bytes_sent,
                'bytes_recv': c.bytes_recv,
                'packets_sent': c.packets_sent,
                'packets_recv': c.packets_recv,
                'errors_in': c.errin,
                'errors_out': c.errout,
                'dropped_in': c.dropin,
                'dropped_out': c.dropout,
                'send_rate': 0, 
                'recv_rate': 0
            }
        if len(self.old_net.keys())==0:
                self.old_net.update({
                'net' : {'bytes_sent' : netifs['net']['bytes_sent'],'bytes_recv' : netifs['net']['bytes_recv']}
          })
        else:
                #print "time_delta:" + str(time_delta)
                #print netifs[addr]['bytes_sent']
                #print self.old_net[addr]['bytes_sent']
                #print netifs[addr]['bytes_recv']
                #print self.old_net[addr]['bytes_recv']
                
                netifs.update({
                'send_rate' : (netifs['net']['bytes_sent'] - self.old_net['net']['bytes_sent']) / time_delta / 1024,
                'recv_rate' : (netifs['net']['bytes_recv'] - self.old_net['net']['bytes_recv']) / time_delta / 1024 
          })
        self.old_net.update({
              'net' : {'bytes_sent' : netifs['net']['bytes_sent'],'bytes_recv' : netifs['net']['bytes_recv']}
          })
        self.old_time = time.time()
        return netifs
