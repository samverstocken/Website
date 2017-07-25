#!/usr/bin/env python
# -*- coding: utf8 -*-

# -----------------------------------------------------------------

# Import standard modules
import webbrowser

# Import PTS classes and modules
from pts.core.tools import html
from pts.core.tools import filesystem as fs
from pts.core.remote.mounter import RemoteMounter
from pts.core.remote.host import Host
from pts.core.tools import introspection

# -----------------------------------------------------------------

username, password = introspection.get_account("ugent.be")

# -----------------------------------------------------------------

# Create host
host = Host("www", name="files.ugent.be", user=username, password=password, mount_point=username + "/www/users", protocol="smb")

# Mount
mounter = RemoteMounter()
mount_path = mounter.mount(host)

# -----------------------------------------------------------------

base_url = "http://users.ugent.be/~sjversto"
stylesheet_url = fs.join(base_url, "stylesheet.css")
images_url = fs.join(base_url, "images")
fonts_url = fs.join(base_url, "fonts")

#skirt_url = fs.join(images_url, "skirt.png")
#ugent_url = fs.join(images_url, "ugent.png")
#dustpedia_url = fs.join(images_url, "dustpedia.png")
#eu_url = fs.join(images_url, "eu.jpg")
#fp7_url = fs.join(images_url, "fp7.png")

# -----------------------------------------------------------------



# -----------------------------------------------------------------

# Determine filename
filename = "index.html"
#filepath = fs.join(mount_path, filename)

# Write
fs.write_text(filepath, template)

# -----------------------------------------------------------------

# Unmount
mounter.unmount(host)

# -----------------------------------------------------------------

# Open
fs.open_in_browser(base_url)

# -----------------------------------------------------------------
