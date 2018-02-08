# -*- coding: utf-8 -*-

"""
Tarbell project configuration
"""
from flask import Blueprint, g, render_template
import os.path # for testing for images
import jinja2 #for context-getting

from itertools import ifilter # For the route
from tarbell.hooks import register_hook #for the route, too

blueprint = Blueprint('candidate-surveys-2018', __name__)


# This is so we don't need to make physical html files for each one. 
@blueprint.route('/responses/<id>.html')
def candidate_survey_response_page(id):
    """
    Make a page for each candidate, based on the unique
    """

    site = g.current_site

    # get our production bucket for URL building
    bucket = site.project.S3_BUCKETS.get('production', '')
    data = site.get_context()
    rows = data.get('candidates', [])

    # get the row we want, defaulting to an empty dictionary
    row = next(ifilter(lambda r: r['id'] == id, rows), {})

    # render a template, using the same template environment as everywhere else
    return render_template('templates/_candidate.html', bucket=bucket, id=id,candidate_info=row,**data)


"""
################################################################
FILTERS & FUNCTIONS //// #######################################
################################################################
"""


@blueprint.app_template_filter('completed_survey')
@jinja2.contextfilter
def generate_autocomplete_list(context, candidate):
    """
    takes a candidate from the candidates tab 
    and looks for survey responses. 
    Returns True if they are found
    """
    
    email = candidate['email']
    ss_tab = candidate['race_category'] # The name of the tab to check

    for c in context[ss_tab]:
        # Check each candidate in the specified survey responses tab
        try:
            if c["contact_email"] == email:
                # If an email match is found, then return true
                return True
        except:
            print "No contact email for {}".format(candidate["email"])
    # If no email match is found, then no repsonses exist.
    return False

def use_this_candidate(candidate, context):
    """
    Autocomplete list helper func to do the actual checking if there are responses
    """
    ss_tab = candidate['race_category']
    responses = context[ss_tab]
    for response in responses:
        if candidate['email'].lower().strip() == response['contact_email'].lower().strip():
            return True
    return False

@blueprint.app_template_filter('generate_autocomplete_list')
@jinja2.contextfilter
def generate_autocomplete_list(context, candidates):
    """
    Takes the list of candidates and checks each one for existing survey responses.
    returns an array of objects to power the autocomplete javascript.

    format => [{label: <readable>, value:<url_id>}, ... ]

    """
    retval = []
    for c in candidates:
        if use_this_candidate(c, context):
            retval.append({
                "label":c['name'].strip(),
                "value": c['id'].strip()
            })

    return retval

def get_candidate_info_from_list(candidates_list, key_to_check, desired_value):
    """
    takes an array of candidate stuff and finds the specified row by matching emails
    """
    for c in candidates_list:
        if c[key_to_check] == desired_value:
            return c

@blueprint.app_template_filter('get_candidate_info')
@jinja2.contextfilter
def get_candidate_info(context, candidate_key):
    """
    This is a filterified version of the reference function
    """
    return get_candidate_info_from_list(context['candidates'], "email", candidate_key)


@blueprint.app_template_filter('get_control_row')
@jinja2.contextfilter
def get_control_row(context, control_row_key):
    """
    Finds and returns the appropriate row from the control tab
    """
    for c in context['control']:
        if c['id'] == control_row_key:
            return c


@blueprint.app_template_filter('has_any')
def has_any(candidates, *args):
    """
    returns true if there is even one single lousy candidate who meets the criteria
    """
    
    final_list = candidates

    for arg in args: # ... test each k-v pair
        final_list = filter((lambda c: arg[0] in c and c[arg[0]] == arg[1]), final_list)
    
    # The the final_list has any candidates, return it. Otherwise return False
    return final_list if len(final_list) > 0 else False


# @blueprint.app_template_filter('has_any')
# def has_any(candidates, category, office_category, office):
#     """
#     returns true if there is even one single lousy candidate who meets the criteria
#     """
#     for c in candidates:
#         if c['race_category'] == category and c[office_category] and c[office_category] == office:
#             return True
#     return False


@blueprint.app_template_filter('get_judicial_circuits')
def get_judicial_circuits(candidates):
    filtered_data = []
    for c in candidates:
        if c['race_category'] == "judicial":
            try:
                filtered_data.append(c['race_district'])
            except:
                # print "skipping", c
                pass
    
    filtered_data = list(set(filtered_data))
    
    return filtered_data

@blueprint.app_template_filter('get_unique_values')
def get_unique_values(candidates, column):
    filtered_data = []
    for c in candidates:
        try:
            filtered_data.append(c[column])
        except:
            # print "skipping", c
            pass
    
    filtered_data = list(set(filtered_data))
    
    return filtered_data


@blueprint.app_template_filter('get_survey_keys')
@jinja2.contextfilter
def get_survey_keys(context, candidate_key):
    candidate_info = get_candidate_info_from_list(context['candidates'], "email", candidate_key)
    ss_tab = candidate_info['race_category']

    control_tab_row = get_control_row(context, ss_tab)
    
    print ("Fetching for ",candidate_key)
    candidate_keys = control_tab_row["survey_questions"]

    return candidate_keys.split(",")


@blueprint.app_template_filter('get_survey_questions')
@jinja2.contextfilter
def get_survey_questions(context, candidate_key):
    candidate_info = get_candidate_info_from_list(context['candidates'], "email", candidate_key)
    ss_tab = candidate_info['race_category']

    candidate_questions = context[ss_tab][0]

    return candidate_questions


@blueprint.app_template_filter('get_survey_responses')
@jinja2.contextfilter
def get_survey_responses(context, candidate_key):
    candidate_info = get_candidate_info_from_list(context['candidates'], "email", candidate_key)
    ss_tab = candidate_info['race_category']

    responses = "Null"

    for c in context[ss_tab]:
        if c['contact_email'] == candidate_info['email']:
            return c

    return False

    

@blueprint.app_template_filter('get_candidate_bio')
@jinja2.contextfilter
def get_candidate_bio(context, candidate_key):
    candidate_info = get_candidate_info_from_list(context['candidates'], "email", candidate_key)

    ss_tab = candidate_info['race_category']

    responses = "Null"

    for c in context[ss_tab]:
        if c['contact_email'] == candidate_key:
            responses = c
    return responses

@blueprint.app_template_filter('get_opponents')
def get_opponents(candidates, c):
    """
        Takes the current candidate (c) and returns a list of their opponents.
        it also marks the candidate on whose page this is displaying.
    """
    retval=[]
    race = c['race']
    for candidate in candidates:
        if candidate == c:
            candidate['current'] = True
        else: 
            candidate['current'] = False
            
        if candidate['race'] == race:
            retval.append(candidate)
    return retval


@blueprint.app_template_filter('make_photo_slug')
def make_photo_slug(name_str):
    """
        Takes a name, and formats it to be filename compatible.
        It then checks for both a jpeg, jpg and png, returning 
        the version it found.
    """
    retval = name_str.lower().strip().replace(" ", "-").replace(".", "").replace("'", "").replace('"', "")
    if os.path.isfile('img/candidates/' + retval + ".jpg"):
        return "{}.jpg".format(retval)
    elif os.path.isfile('img/candidates/' + retval + ".jpeg"):
        return "{}.jpeg".format(retval)
    elif os.path.isfile('img/candidates/' + retval + ".png"):
        return "{}.png".format(retval)
    else:
        return "missing.jpg"


# BACKUP FO DEV PURPOSES:
# SPREADSHEET_KEY = "1QcrOV8ERi1DtosEBUe0qH2Cz22ISyXqRLL4SpUIT0mg"

# REAL Google spreadsheet key:
SPREADSHEET_KEY = "11TAK4CxsSFhZOMXeGVN2ejmqb-NU2WmiXcFzSB_GavQ"

# Exclude these files from publication
EXCLUDES = ['*.md', 'subtemplates','img/candidates/src' ,'img/svgs' ,'requirements.txt', 'node_modules', 'sass', 'js/src', 'package.json', 'package-lock.json', 'Gruntfile.js']

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
    "elex":"elections.chicagotribune.com/candidates",
    "production": "graphics.chicagotribune.com/candidate-surveys-2018",
    "staging": "apps.beta.tribapps.com/candidate-surveys-2018",
}

# Default template variables
DEFAULT_CONTEXT = {
    'name': 'candidate-surveys-2018',
    'title': 'Candidate Surveys 2018'
}