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


vms_service = connection.system_service().vms_service()
exported_vm = vms_service.list()[0]
vms_service.vm_service(exported_vm.id).export(
    host = types.Host(name='vm1'),
    path='/tmp/arik.ova'
)

