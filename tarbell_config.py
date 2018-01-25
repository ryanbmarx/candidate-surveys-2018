# -*- coding: utf-8 -*-

"""
Tarbell project configuration
"""
from flask import Blueprint, g, render_template


blueprint = Blueprint('candidate-surveys-2018', __name__)


@blueprint.app_template_filter('get_opponents')
def make_photo_slug(candidates, c):
    """
        Takes the current candidate (c) and returns a list of their opponents.
        it also marks the candidate on whose page this is displaying.
    """
    retval=[]
    race = c['race']
    for key in candidates.keys():
        candidate = candidates[key]
        if candidate == c:
            candidate['current'] = True
        if candidate['race'] == race:
            retval.append(candidate)
    return retval




@blueprint.app_template_filter('make_photo_slug')
def make_photo_slug(name_str):
    """
        takes a name, and formats it to be filename compatible
    """
    return name_str.lower().replace(" ", "-").replace(".", "").replace("'", "").replace('"', "")



# BACKUP FO DEV PURPOSES:
# SPREADSHEET_KEY = "1QcrOV8ERi1DtosEBUe0qH2Cz22ISyXqRLL4SpUIT0mg"

# REAL Google spreadsheet key:
SPREADSHEET_KEY = "11TAK4CxsSFhZOMXeGVN2ejmqb-NU2WmiXcFzSB_GavQ"

# Exclude these files from publication
EXCLUDES = ['*.md', 'subtemplates', 'img/svgs' ,'requirements.txt', 'node_modules', 'sass', 'js/src', 'package.json', 'package-lock.json', 'Gruntfile.js']

# Spreadsheet cache lifetime in seconds. (Default: 4)
# SPREADSHEET_CACHE_TTL = 4

# Create JSON data at ./data.json, disabled by default
# CREATE_JSON = True

# Get context from a local file or URL. This file can be a CSV or Excel
# spreadsheet file. Relative, absolute, and remote (http/https) paths can be 
# used.
# CONTEXT_SOURCE_FILE = ""

# EXPERIMENTAL: Path to a credentials file to authenticate with Google Drive.
# This is useful for for automated deployment. This option may be replaced by
# command line flag or environment variable. Take care not to commit or publish
# your credentials file.
# CREDENTIALS_PATH = ""

# S3 bucket configuration
S3_BUCKETS = {
    # Provide target -> s3 url pairs, such as:
    #     "mytarget": "mys3url.bucket.url/some/path"
    # then use tarbell publish mytarget to publish to it
    
    "production": "graphics.chicagotribune.com/candidate-surveys-2018",
    "staging": "apps.beta.tribapps.com/candidate-surveys-2018",
}

# Default template variables
DEFAULT_CONTEXT = {
    'name': 'candidate-surveys-2018',
    'title': 'Candidate Surveys 2018'
}