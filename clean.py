#!/usr/bin/env python
# -*- coding: utf8 -*-

# -----------------------------------------------------------------

# Import PTS classes and modules
from pts.core.tools import filesystem as fs
from pts.core.remote.mounter import RemoteMounter
from pts.core.remote.host import load_host
from pts.core.basics.configuration import ConfigurationDefinition, parse_arguments

# -----------------------------------------------------------------

# Create configuration
definition = ConfigurationDefinition(write_config=False)
config = parse_arguments("clean", definition)

# -----------------------------------------------------------------

# Mount the remote file system
host = load_host("www")
mounter = RemoteMounter()
mount_path = mounter.mount(host)

# -----------------------------------------------------------------

# Clear the entire directory
fs.clear_directory(mount_path)

# -----------------------------------------------------------------

# Unmount
mounter.unmount(host)

# -----------------------------------------------------------------
