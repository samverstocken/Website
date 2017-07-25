#!/usr/bin/env python
# -*- coding: utf8 -*-

# -----------------------------------------------------------------

# Import PTS classes and modules
from pts.core.tools import filesystem as fs
from pts.core.remote.mounter import RemoteMounter
from pts.core.remote.host import load_host
from pts.core.basics.configuration import ConfigurationDefinition, parse_arguments
from pts.core.tools import introspection
from pts.core.tools import git

# -----------------------------------------------------------------

definition = ConfigurationDefinition(write_config=False)
config = parse_arguments("upload", definition)

# -----------------------------------------------------------------

base_url = "http://users.ugent.be/~sjversto"
js9_repo_url = "https://github.com/ericmandel/js9"
mathjax_repo_url = "git://github.com/mathjax/MathJax.git"

# -----------------------------------------------------------------

# Mount the remote file system
host = load_host("www")
mounter = RemoteMounter()
mount_path = mounter.mount(host)
js9_path = fs.join(mount_path, "js9")
mathjax_path = fs.join(mount_path, "mathjax")

# -----------------------------------------------------------------

def upload_index():

    """
    This function ...
    :return:
    """

    pass

# -----------------------------------------------------------------

def has_js9():

    """
    This function ...
    :return:
    """

    return fs.is_directory(js9_path) and not fs.is_empty(js9_path)

# -----------------------------------------------------------------

def install_js9():

    """
    This function ...
    :return:
    """

    # Clone into temporary directory
    temp_repo_path = fs.join(introspection.pts_temp_dir, "js9")
    git.clone(js9_repo_url, temp_repo_path, show_output=True)

    # Copy to remote
    fs.copy_directory(temp_repo_path, mount_path)

    # Remove temporary clone
    fs.remove_directory(temp_repo_path)

# -----------------------------------------------------------------

def has_mathjax():

    """
    This function ...
    :return:
    """

    return fs.is_directory(mathjax_path) and not fs.is_empty(mathjax_path)

# -----------------------------------------------------------------

def install_mathjax():

    """
    This function ...
    :return:
    """

    ## Clone the repository and checkout version 2.4
    command = "git clone git://github.com/mathjax/MathJax.git ../html/mathjax"
    command = "git -C ../html/mathjax checkout -b v2.4-latest origin/v2.4-latest"

    # Remove unnecessary files and folders
    #xargs -I fname rm -r fname < doc/mathjax_delete.txt

# -----------------------------------------------------------------

# Steps
if not has_js9(): install_js9()
if not has_mathjax(): install_mathjax()
upload_index()

# Unmount
mounter.unmount(host)

# -----------------------------------------------------------------

# Open
fs.open_in_browser(base_url)

# -----------------------------------------------------------------
