#!/usr/bin/env python
# -*- coding: utf8 -*-

# -----------------------------------------------------------------

# Import standard modules
import inspect

# Import PTS classes and modules
from pts.core.tools import html
from pts.core.tools import filesystem as fs
from pts.core.basics.configuration import ConfigurationDefinition, parse_arguments
from pts.core.tools import browser

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

title = "Sam Verstocken"
style = "ugentstyle"

# -----------------------------------------------------------------

# Create the page
page = html.HTMLPage(title, css_path=stylesheet_path, style=style, footing=html.updated_footing())

# -----------------------------------------------------------------

page += html.center(html.make_theme_button())

# -----------------------------------------------------------------

text = "Sam Verstocken"
text += html.newline + html.mailto("sam.verstocken@ugent.be")
text += html.newline + "PhD student at Ghent University"
text += html.newline + "under the supervision of Prof. Maarten Baes"

rows = [[html.image(me_path, height=100), text]]
table = html.SimpleTable(rows)
page += table

# -----------------------------------------------------------------

# AND: <body style='font-family="sans-serif"'> ?

# -----------------------------------------------------------------

page += html.make_line("heavy")

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
page += str(table) + html.line

# Create title
title = "Hybrid task+data parallelization in Monte Carlo radiative transfer code SKIRT"
title = html.fontsize_template.format(size=20, text=html.underline_template.format(text=title))

page += html.newline + title + html.newline

page += html.mailto(my_email, html.bold_template.format(text="Sam Verstocken")) + ", "
page += html.mailto(dries_email, "Dries Van De Putte") + ", "
page += html.mailto(peter_email, "Peter Camps") + ", "
page += html.mailto(maarten_email, "Maarten Baes")

page += html.newline + html.newline + html.line
page += html.newline
page += html.small_template.format(text=abstract)

page += html.newline + html.newline + html.line + html.newline
page += "Paper:" + html.newline
items = []
items.append(html.hyperlink("http://adsabs.harvard.edu/abs/2017A%26C....20...16V", "ADS"))
items.append(html.hyperlink("http://www.sciencedirect.com/science/article/pii/S221313371730001X", "ScienceDirect"))
page += html.unordered_list(items)
page += html.line + html.newline

page += "Useful links:" + html.newline
items = []
items.append(html.hyperlink(skirt_repo_url, "SKIRT repository on GitHub"))
items.append(html.hyperlink("http://www.skirt.ugent.be/skirt/index.html", "SKIRT documentation"))
items.append(html.hyperlink("http://www.skirt.ugent.be/skirt/_parallelization.html", "Parallelization in SKIRT"))
items.append(html.hyperlink("http://www.skirt.ugent.be/tutorials/_tutorial_parallelization.html", "SKIRT parallelization tutorial"))
page += html.unordered_list(items)

#page += html.newline + html.newline
page += html.make_line("heavy") + html.newline

# -----------------------------------------------------------------

other_images = html.image(eu_path, height=40) + html.image(fp7_path, height=40) + html.newline + html.image(dustpedia_path, height=50)

# Logos
rows = [[html.image(ugent_path, height=100), other_images]]
table = html.SimpleTable(rows)
page += str(table) + html.line

# Create title
title = "High resolution 3D radiative transfer modeling of DustPedia galaxies"
title = html.fontsize_template.format(size=20, text=html.underline_template.format(text=title))

page += html.newline + title + html.newline

page += html.mailto(my_email, html.bold_template.format(text="Sam Verstocken")) + ", " + html.mailto(sebastien_email, "Sébastien Viaene") + ", "
page += html.mailto(ilse_email, "Ilse De Looze") + ", " + html.mailto(ana_email, "Ana Trcka") + ", "
page += html.mailto(angelos_email, "Angelos Neseserian") + ", " + html.mailto(maarten_email, "Maarten Baes")
page += html.newline + html.newline

page += html.line + html.newline

page += "Modelling details:" + html.newline + html.newline

rows = [[html.hyperlink("M81.html", "M81"), "In progress", "Sam Verstocken"], ["M77", "Preparation stage", "Sébastien Viaene"], ["NGC 1365", "Future", "Angelos Neseserian"]]
table = html.SimpleTable(rows, css_class="hovertable")
page += str(table) + html.newline

page += html.line + html.newline

page += "Interesting links:" + html.newline
items = []
items.append(html.hyperlink("http://www.dustpedia.com", "DustPedia.com"))
items.append(html.hyperlink("http://dustpedia.astro.noa.gr", "DustPedia Archive"))
items.append(html.hyperlink("https://en.wikipedia.org/wiki/DustPedia", "DustPedia on WikiPedia"))
page += html.unordered_list(items)

# Set
acknowledgement = "DustPedia is a collaborative focused research project supported by the European Union under the Seventh Framework Programme (2007-2013) call (proposal no. 606847). The participating institutions are: Cardiff University, UK; National Observatory of Athens, Greece; Ghent University, Belgium; Université Paris Sud, France; National Institute for Astrophysics, Italy and CEA (Paris), France."
page += html.line + html.newline + html.small_template.format(text=acknowledgement) + html.newline + html.newline + html.make_line("heavy")


# Write the page
page.saveto(index_path)

# -----------------------------------------------------------------

# Open
if config.show: browser.open_path(index_path)

# -----------------------------------------------------------------
