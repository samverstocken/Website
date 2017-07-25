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
from pts.core.tools import terminal

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

index_name = "index.html"
images_name = "Images"
logos_name = "Logos"
fonts_name = "Fonts"

# -----------------------------------------------------------------

this_filepath = fs.absolute_or_in_cwd(inspect.getfile(inspect.currentframe()))
directory_path = fs.directory_of(this_filepath)
mathjax_delete_path = fs.join(directory_path, "mathjax_delete.txt")
index_filepath = fs.join(directory_path, index_name)
logos_path = fs.join(directory_path, logos_name)
images_path = fs.join(directory_path, images_name)
fonts_path = fs.join(directory_path, fonts_name)

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
    #fs.remove_directory(temp_repo_path)

    js9_web_name = "js9-web"
    temp_web_path = fs.join(introspection.pts_temp_dir, js9_web_name)

    terminal.execute("npm install socket.io", cwd=temp_repo_path, show_output=True)
    terminal.execute("npm install electron", cwd=temp_repo_path, show_output=True)

    # npm install socket.io
    # npm install electron

    configure = "sh configure --with-webdir=" + temp_web_path + " --with-helper=nodejs"
    terminal.execute(configure, cwd=temp_repo_path, show_output=True)

    terminal.execute("make", cwd=temp_repo_path, show_output=True)
    terminal.execute("make install", cwd=temp_repo_path, show_output=True)

    terminal.execute("npm install socket.io", cwd=temp_web_path, show_output=True)
    terminal.execute("npm install electron", cwd=temp_web_path, show_output=True)

    # Run desktop:
    # ./node_modules/.bin/electron .

    fs.open_directory(temp_web_path)

    # configure location to install the JS9 web files,
    # where to find cfitsio library and include files,
    # where to install programs and scripts,
    # what sort of helper to build:
    #./ configure --with-webdir=[path_to_web_install] \
    #        --with-cfitsio=[path_to_cfitsio] \
    #        --prefix=[path_to_prog_install] \
    #        --with-helper=nodejs

    # the usual ...
    #make
    #make install

    # start helper
    #cd path_to_web_install
    #node js9Helper.js 2>&1 > js9node.log &

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

def has_equal_number_of_files(directory_a, directory_b, create=False):

    """
    This function ...
    :param directory_a:
    :param directory_b:
    :param create:
    :return:
    """

    nlocal = fs.nfiles_in_path(directory_a, recursive=True)
    if fs.is_directory(directory_b): nremote = fs.nfiles_in_path(directory_b, recursive=True)
    else:
        if create: fs.create_directory(directory_b)
        else: raise ValueError("The directory '" + directory_b + "' does not exist")
        nremote = 0

    return nlocal == nremote

# -----------------------------------------------------------------

def upload_images():

    """
    This function ...
    :return:
    """

    mount_images_path = fs.join(mount_path, images_name)

    if not has_equal_number_of_files(images_path, mount_images_path, create=True):
        fs.clear_directory(mount_images_path)
        fs.copy_from_directory(images_path, mount_images_path)

# -----------------------------------------------------------------

def upload_logos():

    """
    This function ...
    :return:
    """

    mount_logos_path = fs.join(mount_path, logos_name)

    if not has_equal_number_of_files(logos_path, mount_logos_path, create=True):
        fs.clear_directory(mount_logos_path)
        fs.copy_from_directory(logos_path, mount_logos_path)

# -----------------------------------------------------------------

def upload_fonts():

    """
    This function ...
    :return:
    """

    mount_fonts_path = fs.join(mount_path, fonts_name)

    if not has_equal_number_of_files(fonts_path, mount_fonts_path, create=True):
        fs.clear_directory(mount_fonts_path)
        fs.copy_from_directory(fonts_path, mount_fonts_path)

# -----------------------------------------------------------------

def upload_index():

    """
    This function ...
    :return:
    """

    mount_index_path = fs.join(mount_path, index_name)
    if fs.is_file(mount_index_path): fs.remove_file(mount_index_path)

    # Copy
    fs.copy_file(index_filepath, mount_path)

# -----------------------------------------------------------------

install_js9()
exit()

# Steps
if not has_js9(): install_js9()
if not has_mathjax(): install_mathjax()
upload_images()
upload_logos()
upload_fonts()
upload_index()

# Unmount
mounter.unmount(host)

# -----------------------------------------------------------------

# Open
fs.open_in_browser(base_url)

# -----------------------------------------------------------------
