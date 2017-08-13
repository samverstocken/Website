#!/usr/bin/env python
# -*- coding: utf8 -*-

# -----------------------------------------------------------------

# Import standard modules
import tinycss

# Import PTS classes and modules
from pts.core.tools import filesystem as fs

# -----------------------------------------------------------------

stylesheet_path = "stylesheet.css"
text = fs.get_text(stylesheet_path)

# -----------------------------------------------------------------

# The stylesheet can be read in as a Python object:
parser = tinycss.make_parser('page3')
stylesheet = parser.parse_stylesheet(text)
print(stylesheet)

# -----------------------------------------------------------------
