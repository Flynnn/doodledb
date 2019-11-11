# doodledb
A json doodle database. Based on the work of Adi Ben-Hur

All doodles available here are copied from the Doodle Library, and are therefore:

Free to download, share and adapt under Creative Commons Attribution 4.0 International License.
https://creativecommons.org/licenses/by/4.0/

Attribution (in accordance with this license) should go to the Doodle Library:
https://www.thedoodlelibrary.com/

I have modified this data by downloading it, converting it from SVG to basic JSON path data, and uploading it here.

# How it works
download.py will generate a brand new doodledb.json every time you run it. How? *by scraping the doodle library's website*

As such, please only run said script if absolutely necessary.

Since I am allowed to do so, under CC4.0, I have simply included the final results of scraping.

Many of the doodles need cleanup, I'm afraid it simply isn't perfect, but ce's la vie

# How to use doodledb.json
Doodledb.json is a dict containing two elements:
'categories' and 'doodles'

The categories element is a dictionary mapping category names to lists of doodle names

The doodles element is a dictionary mapping doodle names to doodle objects

The so called 'doodle objects' are, in fact, just lists of strokes. Each stroke is a list of two coordinates, one being the start location for the stroke and the other being the end location.

The doodle names are not sanitized, so some of them include strange special characters, etc.

That should be enough to get you started.
