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

logos_path = "logos"
images_path = "images"
fonts_path = "fonts"

# -----------------------------------------------------------------

modeling_path = fs.join(directory_path, "modeling.html")

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

title = "High-resolution, 3D radiative transfer modeling"
style = "ugentstyle"

# -----------------------------------------------------------------

# Create the page
page = html.HTMLPage(title, css_path=stylesheet_path, style=style, footing=html.updated_footing())

# -----------------------------------------------------------------

page += html.center(html.make_theme_button())

# -----------------------------------------------------------------

other_images = html.image(eu_path, height=40) + html.image(fp7_path, height=40) + html.newline + html.image(dustpedia_path, height=50)

# Create title
title = "High resolution 3D radiative transfer modeling of DustPedia galaxies"
title = html.fontsize_template.format(size=20, text=html.underline_template.format(text=title))
page += html.newline
page += title
page += html.newline + html.newline

# Add modeling table
rows = [[html.hyperlink("modelling/M81/index.html", "M81"), "In progress", "Sam Verstocken"], ["M77", "Model construction", "Sébastien Viaene"], ["NGC 1365", "Exploration stage", "Angelos Nersesian"]]
table = html.SimpleTable(rows, css_class="hovertable")
page += str(table) + html.newline

page += html.line + html.newline

# Write the page
page.saveto(modeling_path)

# -----------------------------------------------------------------

# Open
if config.show: browser.open_path(modeling_path)

# -----------------------------------------------------------------
