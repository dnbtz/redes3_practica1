#!/usr/bin/env python

import rrdtool


def create(nom,id):
    ret = rrdtool.create('%s%s.rrd' % (nom,id),
                         "--start",'N',
                         "--step",'10',
                         "DS:inoctets:COUNTER:600:U:U",
                         "DS:outoctets:COUNTER:600:U:U",
                         "RRA:AVERAGE:0.5:6:700",
                         "RRA:AVERAGE:0.5:1:600")

    if ret:
        print (rrdtool.error())
