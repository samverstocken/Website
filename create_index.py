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

skirt_url = fs.join(images_url, "skirt.png")
ugent_url = fs.join(images_url, "ugent.png")
dustpedia_url = fs.join(images_url, "dustpedia.png")
eu_url = fs.join(images_url, "eu.jpg")
fp7_url = fs.join(images_url, "fp7.png")

# -----------------------------------------------------------------

body = ""

# -----------------------------------------------------------------

kwargs = dict()
kwargs["title"] = "Sam Verstocken"
kwargs["head"] = html.link_stylesheet_header_template.format(url=stylesheet_url)

# -----------------------------------------------------------------

text = "Sam Verstocken"
text += html.newline + html.mailto("sam.verstocken@ugent.be")
text += html.newline + "PhD student at Ghent University"
text += html.newline + "under the supervision of Prof. Maarten Baes"

rows = [[html.image(fs.join(images_url, "sam.png"), height=100), text]]
table = html.SimpleTable(rows)
body += str(table)

# -----------------------------------------------------------------

# AND: <body style='font-family="sans-serif"'> ?

# -----------------------------------------------------------------

body += html.line

# -----------------------------------------------------------------

abstract = """
We designed and implemented a new hybrid parallelization scheme in our 
Monte Carlo radiative transfer code SKIRT, which has been used extensively for modeling the 
continuum radiation of dusty astrophysical systems including late-type galaxies and dusty tori. 
The hybrid scheme combines distributed memory parallelization, using the standard Message Passing 
Interface (MPI) to communicate between processes, and shared memory parallelization, providing 
multiple execution threads within each process to avoid duplication of data structures. The synchronization 
between multiple threads is accomplished through atomic operations without high-level locking (also called 
lock-free programming). This improves the scaling behavior of the code and substantially simplifies the 
implementation of the hybrid scheme. The result is an extremely flexible solution that adjusts to the number of 
available nodes, processors and memory, and consequently performs well on a wide variety of computing 
architectures."""

# Logos
rows = [[html.image(skirt_url, height=100), html.image(ugent_url, height=100)]]
table = html.SimpleTable(rows)
body += str(table) + html.line

# Create title
title = "Hybrid task+data parallelization in Monte Carlo radiative transfer code SKIRT"
title = html.fontsize_template.format(size=20, text=html.underline_template.format(text=title))

body += html.newline + title + html.newline

body += html.mailto("sam.verstocken@ugent.be", html.bold_template.format(text="Sam Verstocken")) + ", "
body += html.mailto("dries", "Dries Van De Putte") + ", "
body += html.mailto("peter", "Peter Camps") + ", "
body += html.mailto("maarten", "Maarten Baes")

body += html.newline + html.newline + html.line
body += html.newline
body += html.small_template.format(text=abstract)
body += html.newline + html.newline + html.line + html.newline
body += "Paper:" + html.newline + html.newline
body += "<li>" + html.hyperlink("http://adsabs.harvard.edu/abs/2017A%26C....20...16V", "ADS")
body += "<li>" + html.hyperlink("http://www.sciencedirect.com/science/article/pii/S221313371730001X", "ScienceDirect")
body += html.newline + html.newline + html.line

# -----------------------------------------------------------------

other_images = html.image(eu_url, height=40) + html.image(fp7_url, height=40) + html.newline + html.image(dustpedia_url, height=50)

# Logos
rows = [[html.image(ugent_url, height=100), other_images]]
table = html.SimpleTable(rows)
body += str(table) + html.line

# Create title
title = "High resolution 3D radiative transfer modeling of DustPedia galaxies"
title = html.fontsize_template.format(size=20, text=html.underline_template.format(text=title))

body += html.newline + title + html.newline

body += html.mailto("sam.verstocken@ugent.be", html.bold_template.format(text="Sam Verstocken")) + ", " + html.mailto("sebastien.viaene@ugent.be", "Sébastien Viaene") + ", "
body += html.mailto("ilsed", "Ilse De Looze") + ", " + html.mailto("Ana", "Ana Trcka") + ", "
body += html.mailto("angelos", "Angelos Neseserian") + ", " + html.mailto("maarten.baes@ugent.be", "Maarten Baes")
body += html.newline + html.newline

rows = [[html.hyperlink("M81.html", "M81"), "In progress", "Sam Verstocken"], ["M77", "Preparation stage", "Sébastien Viaene"], ["NGC 1365", "Future", "Angelos Neseserian"]]
table = html.SimpleTable(rows, css_class="realtable")
body += str(table) + html.newline

body += "Interesting links:" + html.newline + html.newline
body += html.item + html.hyperlink("http://www.dustpedia.com", "DustPedia.com")
body += html.item + html.hyperlink("http://dustpedia.astro.noa.gr", "DustPedia Archive")
body += html.item + html.hyperlink("https://en.wikipedia.org/wiki/DustPedia", "DustPedia on WikiPedia")
body += html.newline + html.newline

# Set
acknowledgement = "DustPedia is a collaborative focused research project supported by the European Union under the Seventh Framework Programme (2007-2013) call (proposal no. 606847). The participating institutions are: Cardiff University, UK; National Observatory of Athens, Greece; Ghent University, Belgium; Université Paris Sud, France; National Institute for Astrophysics, Italy and CEA (Paris), France."
body += html.line + html.newline + html.small_template.format(text=acknowledgement) + html.newline + html.newline + html.line

# -----------------------------------------------------------------

footing = "Last updated " + time.pretty_date().lower()

# Finish body
body += html.newline
body += html.center_template.format(text=footing)
kwargs["body"] = body
kwargs["style"] = "ugentstyle"

# -----------------------------------------------------------------

# Get the template
template = html.page_template.format(**kwargs)

# -----------------------------------------------------------------

# Determine filename
filename = "index.html"
filepath = fs.join(mount_path, filename)

# Write
fs.write_text(filepath, template)

# -----------------------------------------------------------------

# Unmount
mounter.unmount(host)

# -----------------------------------------------------------------

# Open
webbrowser._tryorder = ["safari"]
webbrowser.open(base_url, new=2)

# -----------------------------------------------------------------
