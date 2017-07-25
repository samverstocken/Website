#!/usr/bin/env python
# -*- coding: utf8 -*-

# -----------------------------------------------------------------

# Import standard modules
import inspect

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

# -----------------------------------------------------------------

js9_name = "js9"
mathjax_name = "mathjax"
js9_path = fs.join(mount_path, js9_name)
mathjax_path = fs.join(mount_path, mathjax_name)

# -----------------------------------------------------------------

this_filepath = fs.absolute_or_in_cwd(inspect.getfile(inspect.currentframe()))
directory_path = fs.directory_of(this_filepath)
mathjax_delete_path = fs.join(directory_path, "mathjax_delete.txt")

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
    temp_repo_path = fs.join(introspection.pts_temp_dir, js9_name)
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

    # Clone into temporary directory
    temp_repo_path = fs.join(introspection.pts_temp_dir, mathjax_name)
    git.clone(mathjax_repo_url, temp_repo_path, show_output=True)

    # Checkout some version
    git.checkout_new_branch(temp_repo_path, "v2.4-latest", "origin/v2.4-latest", show_output=True)

    # Remove unnecessary files
    for relative_path in fs.read_lines(mathjax_delete_path):

        path = fs.join(temp_repo_path, relative_path)
        fs.remove_directory_or_file(path)

    # Copy to remote
    fs.copy_directory(temp_repo_path, mount_path)

    # Remove temporary clone
    fs.remove_directory(temp_repo_path)

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
