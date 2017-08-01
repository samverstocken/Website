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
from pts.core.tools.logging import log
from pts.core.tools import browser

# -----------------------------------------------------------------

# Create configuration
definition = ConfigurationDefinition(write_config=False)
definition.add_flag("show", "show the webpage after uploading", False)
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

stylesheet_name = "stylesheet.css"
index_name = "index.html"
images_name = "images"
logos_name = "logos"
fonts_name = "fonts"

# -----------------------------------------------------------------

this_filepath = fs.absolute_or_in_cwd(inspect.getfile(inspect.currentframe()))
directory_path = fs.directory_of(this_filepath)
mathjax_delete_path = fs.join(directory_path, "mathjax_delete.txt")

stylesheet_path = fs.join(directory_path, stylesheet_name)
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

    # Inform the user
    log.info("Installing JS9 ...")

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

    # in js9.js:
    # line 151: mousetouchZoom: false,	// use mouse wheel, pinch to zoom?
    # i replaced 'false' to 'true'.

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

    # Inform the user
    log.info("Installing MathJax ...")

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

def upload_stylesheet():

    """
    This function ...
    :return:
    """

    # Inform the user
    log.info("Uploading the stylesheet ...")

    # Syncrhonize
    mount_stylesheet_path = fs.join(mount_path, stylesheet_name)
    updated = fs.update_file(stylesheet_path, mount_stylesheet_path, create=True, report=log.is_debug())

    if updated: log.success("Succesfully uploaded the stylesheet")
    else: log.info("Already up-to-date")

# -----------------------------------------------------------------

def upload_images():

    """
    This function ...
    :return:
    """

    # Inform the user
    log.info("Uploading the images ...")

    # Synchronize
    mount_images_path = fs.join(mount_path, images_name)
    updated = fs.update_directory(images_path, mount_images_path, create=True, report=log.is_debug())

    if updated: log.success("Succesfully uploaded the images")
    else: log.info("Already up-to-date")

# -----------------------------------------------------------------

def upload_logos():

    """
    This function ...
    :return:
    """

    # Inform the user
    log.info("Uploading the logos ...")

    # Synchronize
    mount_logos_path = fs.join(mount_path, logos_name)
    updated = fs.update_directory(logos_path, mount_logos_path, create=True, report=log.is_debug())

    if updated: log.success("Succesfully uploaded the logos")
    else: log.info("Already up-to-date")

# -----------------------------------------------------------------

def upload_fonts():

    """
    This function ...
    :return:
    """

    # Inform the user
    log.info("Uploading the fonts ...")

    # Synchronize
    mount_fonts_path = fs.join(mount_path, fonts_name)
    updated = fs.update_directory(fonts_path, mount_fonts_path, create=True, report=log.is_debug())

    if updated: log.success("Succesfully uploaded the fonts")
    else: log.info("Already up-to-date")

# -----------------------------------------------------------------

def upload_index():

    """
    This function ...
    :return:
    """

    # Inform the user
    log.info("Uploading the index page ...")

    # Check
    mount_index_path = fs.join(mount_path, index_name)
    if fs.is_file(mount_index_path): fs.remove_file(mount_index_path)

    # Copy
    fs.copy_file(index_filepath, mount_path)

# -----------------------------------------------------------------

# Steps
#if not has_js9(): install_js9()
#if not has_mathjax(): install_mathjax()
upload_stylesheet()
upload_images()
upload_logos()
upload_fonts()
upload_index()

# Unmount
mounter.unmount(host)

# -----------------------------------------------------------------

# Open
if config.show: browser.open_url(base_url)

# -----------------------------------------------------------------
