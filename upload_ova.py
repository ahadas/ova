#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tarfile
import re
import ovirtsdk4 as sdk
import ovirtsdk4.types as types
import logging
import time

connection = sdk.Connection(
    url='http://0.0.0.0:8080/ovirt-engine/api',
    username='admin@internal',
    password='1',
    debug=True,
    log=logging.getLogger(),
)

disks_service = connection.system_service().disks_service()

tar = tarfile.open("ovirt.ova")
entries = tar.getmembers()

f = tar.extractfile(entries[0])
ovf = f.read()
print "content: %s" %(ovf)

diskSection = re.findall("\<DiskSection>.*?\</DiskSection>", ovf)[0]
disks = re.findall("\<Disk (.*?)\>\</Disk>", diskSection)
for disk in disks:
    break
    props = dict(e.strip().split('=') for e in disk.split('ovf:') if e != '')
    for prop in props:
        props[prop] = props[prop][1:len(props[prop])-1]
    print props
    print int(props['actual_size']) * 2**30
    d = disks_service.add(
        disk = types.Disk(
            id=props['diskId'],
            name=props['disk-alias'],
            description=props['description'],
            format=types.DiskFormat.COW if props['volume-format']=='COW' else types.DiskFormat.RAW,
            provisioned_size=int(props['size']) * 2**30,
            initial_size=int(props['actual_size']) * 2**30,
            storage_domains=[
                types.StorageDomain(
                    name='Default2'
                )
            ]
        )
    )

#disk_service = disks_service.disk_service(d.id)
while True:
    break
    time.sleep(5)
    disk = disk_service.get()
    if disk.status == types.DiskStatus.OK:
        break

# TODO: transfer image

vms_service = connection.system_service().vms_service()
vm = vms_service.add(
    types.Vm(
        cluster=types.Cluster(
            name='Default',
        ),
        initialization = types.Initialization(
            configuration = types.Configuration(
                type = types.ConfigurationType.OVF,
                data = ovf
            )
        ),
    ),
)

tar.close()
