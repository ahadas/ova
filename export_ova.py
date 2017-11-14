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
vms_service.vm_service(exported_vm.id).export_to_path_on_host(
    host = types.Host(id='ce5f4bd2-1c08-4deb-83a3-07574a56f323'),
    directory='/tmp',
    filename='arik987.ova'
)

