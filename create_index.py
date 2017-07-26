#!/usr/bin/env python
# -*- coding: utf8 -*-

# -----------------------------------------------------------------

# Import standard modules
import inspect

# Import PTS classes and modules
from pts.core.tools import html
from pts.core.tools import filesystem as fs
from pts.core.tools import time
from pts.core.basics.configuration import ConfigurationDefinition, parse_arguments

# -----------------------------------------------------------------

definition = ConfigurationDefinition(write_config=False)
definition.add_flag("show", "show index page", False)
config = parse_arguments("create_index", definition)

# -----------------------------------------------------------------

base_url = "http://users.ugent.be/~sjversto"
skirt_repo_url = "https://github.com/SKIRT/SKIRT8"

# -----------------------------------------------------------------

this_filepath = fs.absolute_or_in_cwd(inspect.getfile(inspect.currentframe()))
directory_path = fs.directory_of(this_filepath)

# -----------------------------------------------------------------

#logos_path = fs.join(directory_path, "Logos")
#images_path = fs.join(directory_path, "Images")
#fonts_path = fs.join(directory_path, "Fonts")

logos_path = "logos"
images_path = "images"
fonts_path = "fonts"

# -----------------------------------------------------------------

index_path = fs.join(directory_path, "index.html")

# -----------------------------------------------------------------

dustpedia_logos_path = fs.join(logos_path, "DustPedia")
ugent_logos_path = fs.join(logos_path, "UGent")
github_logos_path = fs.join(logos_path, "GitHub")
eu_logos_path = fs.join(logos_path, "EU")
skirt_logos_path = fs.join(logos_path, "SKIRT")

# -----------------------------------------------------------------

me_path = fs.join(images_path, "sam.png")
skirt_path = fs.join(skirt_logos_path, "skirt.png")
ugent_path = fs.join(ugent_logos_path, "ugent.png")
dustpedia_path = fs.join(dustpedia_logos_path, "dustpedia.png")
eu_path = fs.join(eu_logos_path, "eu.jpg")
fp7_path = fs.join(eu_logos_path, "fp7.png")
github_path = fs.join(github_logos_path, "github.png")
github_grey_path = fs.join(github_logos_path, "github-grey.png")

# -----------------------------------------------------------------

#stylesheet_path = fs.join(directory_path, "stylesheet.css")
stylesheet_path = "stylesheet.css"

# -----------------------------------------------------------------

my_email = "sam.verstocken@ugent.be"
maarten_email = "maarten.baes@ugent.be"
peter_email = "peter.camps@ugent.be"
dries_email = "drvdputt.VanDePutte@UGent.be"
marjorie_email = "Marjorie.Decleir@UGent.be"
sebastien_email = "sebastien.viaene@ugent.be"
ana_email = "Ana.Trcka@UGent.be"
angelos_email = "ag.nersesian@gmail.com"
ilse_email = "Ilse.DeLooze@UGent.be"

# -----------------------------------------------------------------

body = ""

# -----------------------------------------------------------------

kwargs = dict()
kwargs["title"] = "Sam Verstocken"
kwargs["head"] = html.link_stylesheet_header_template.format(url=stylesheet_path)

# -----------------------------------------------------------------

text = "Sam Verstocken"
text += html.newline + html.mailto("sam.verstocken@ugent.be")
text += html.newline + "PhD student at Ghent University"
text += html.newline + "under the supervision of Prof. Maarten Baes"

rows = [[html.image(me_path, height=100), text]]
table = html.SimpleTable(rows)
body += str(table)

# -----------------------------------------------------------------

# AND: <body style='font-family="sans-serif"'> ?

# -----------------------------------------------------------------

body += html.make_line("heavy")

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
rows = [[html.image(skirt_path, height=100), html.image(ugent_path, height=100), html.hyperlink(skirt_repo_url, html.image(github_grey_path, height=80, hover=github_path))]]
table = html.SimpleTable(rows)
body += str(table) + html.line

# Create title
title = "Hybrid task+data parallelization in Monte Carlo radiative transfer code SKIRT"
title = html.fontsize_template.format(size=20, text=html.underline_template.format(text=title))

body += html.newline + title + html.newline

body += html.mailto(my_email, html.bold_template.format(text="Sam Verstocken")) + ", "
body += html.mailto(dries_email, "Dries Van De Putte") + ", "
body += html.mailto(peter_email, "Peter Camps") + ", "
body += html.mailto(maarten_email, "Maarten Baes")

body += html.newline + html.newline + html.line
body += html.newline
body += html.small_template.format(text=abstract)

body += html.newline + html.newline + html.line + html.newline
body += "Paper:" + html.newline + html.newline
body += html.item + html.hyperlink("http://adsabs.harvard.edu/abs/2017A%26C....20...16V", "ADS")
body += html.item + html.hyperlink("http://www.sciencedirect.com/science/article/pii/S221313371730001X", "ScienceDirect")

body += html.newline + html.newline + html.line + html.newline

body += "Useful links:" + html.newline + html.newline
body += html.item + html.hyperlink(skirt_repo_url, "SKIRT repository on GitHub")
body += html.item + html.hyperlink("http://www.skirt.ugent.be/skirt/index.html", "SKIRT documentation")
body += html.item + html.hyperlink("http://www.skirt.ugent.be/skirt/_parallelization.html", "Parallelization in SKIRT")
body += html.item + html.hyperlink("http://www.skirt.ugent.be/tutorials/_tutorial_parallelization.html", "SKIRT parallelization tutorial")

body += html.newline + html.newline + html.make_line("heavy") + html.newline

# -----------------------------------------------------------------

other_images = html.image(eu_path, height=40) + html.image(fp7_path, height=40) + html.newline + html.image(dustpedia_path, height=50)

# Logos
rows = [[html.image(ugent_path, height=100), other_images]]
table = html.SimpleTable(rows)
body += str(table) + html.line

# Create title
title = "High resolution 3D radiative transfer modeling of DustPedia galaxies"
title = html.fontsize_template.format(size=20, text=html.underline_template.format(text=title))

body += html.newline + title + html.newline

body += html.mailto(my_email, html.bold_template.format(text="Sam Verstocken")) + ", " + html.mailto(sebastien_email, "Sébastien Viaene") + ", "
body += html.mailto(ilse_email, "Ilse De Looze") + ", " + html.mailto(ana_email, "Ana Trcka") + ", "
body += html.mailto(angelos_email, "Angelos Neseserian") + ", " + html.mailto(maarten_email, "Maarten Baes")
body += html.newline + html.newline

body += html.line + html.newline

body += "Modelling details:" + html.newline + html.newline

rows = [[html.hyperlink("M81.html", "M81"), "In progress", "Sam Verstocken"], ["M77", "Preparation stage", "Sébastien Viaene"], ["NGC 1365", "Future", "Angelos Neseserian"]]
table = html.SimpleTable(rows, css_class="hovertable")
body += str(table) + html.newline

body += html.line + html.newline

body += "Interesting links:" + html.newline + html.newline
body += html.item + html.hyperlink("http://www.dustpedia.com", "DustPedia.com")
body += html.item + html.hyperlink("http://dustpedia.astro.noa.gr", "DustPedia Archive")
body += html.item + html.hyperlink("https://en.wikipedia.org/wiki/DustPedia", "DustPedia on WikiPedia")
body += html.newline + html.newline

# Set
acknowledgement = "DustPedia is a collaborative focused research project supported by the European Union under the Seventh Framework Programme (2007-2013) call (proposal no. 606847). The participating institutions are: Cardiff University, UK; National Observatory of Athens, Greece; Ghent University, Belgium; Université Paris Sud, France; National Institute for Astrophysics, Italy and CEA (Paris), France."
body += html.line + html.newline + html.small_template.format(text=acknowledgement) + html.newline + html.newline + html.make_line("heavy")

# -----------------------------------------------------------------

footing = html.small_template.format(text="Last updated on " + time.pretty_time())

# -----------------------------------------------------------------

# Finish body
body += html.center_template.format(text=footing)
kwargs["body"] = body
kwargs["style"] = "ugentstyle"

# -----------------------------------------------------------------

# Get the template
template = html.page_template.format(**kwargs)

# -----------------------------------------------------------------

# Write
fs.write_text(index_path, template)

# -----------------------------------------------------------------

# Open
if config.show: fs.open_in_browser(index_path)

# -----------------------------------------------------------------
