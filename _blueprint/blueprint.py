# -*- coding: utf-8 -*-
import locale
from flask import Blueprint

from clint.textui import colored
from tarbell.hooks import register_hook
from tarbell.utils import puts

import xlrd 			# for parsing excel dates
import datetime 		# For parsing dates
import dateutil.parser 	# For parsing dates

from PIL import Image 	# For the image sizing

from tribune_viztools.tarbell.blueprint import TribuneTarbellBlueprint
from tribune_viztools.tarbell.hooks import (
    copy_front_end_build_script_templates,
    create_front_end_files,
    create_readme,
    create_unfuddle_project,
    newproject_add_excludes,
    newproject_add_default_omniture_config,
    merge_extra_context,
    update_facebook,
)

NAME = "Tribune Off-Platform Tarbell Blueprint, version 2"

blueprint = TribuneTarbellBlueprint('blueprint', __name__)


try:
    locale.setlocale(locale.LC_ALL, 'en_US')
except locale.Error:
    puts(colored.red("Locale error"))





NEWPROJECT_HOOKS = (
    copy_front_end_build_script_templates,
    create_front_end_files,
    create_readme,
    create_unfuddle_project,
    newproject_add_excludes,
    newproject_add_default_omniture_config,
)

GENERATE_HOOKS = (
    merge_extra_context,
)

PUBLISH_HOOKS = (
    update_facebook,
)

for f in NEWPROJECT_HOOKS:
    register_hook('newproject')(f)

for f in GENERATE_HOOKS:
    register_hook('generate')(f)

for f in PUBLISH_HOOKS:
    register_hook('publish')(f)

@blueprint.app_template_filter('get_thumbnail_info')
def get_thumbnail_info(image):
    """
        For SEO metadata, get and return image dimensions
    """
    try:
        im = Image.open(image)
        width,height = im.size
        return {
            "width": width,
            "height": height
        }
    except IOError:
        print("Can't find ", id)

@blueprint.app_template_filter('xldate_to_datetime')
def xldate_to_datetime(xldate):
	"""
	Takes a date in excel format and returns it as a python datetime
	"""
	if isinstance(xldate, unicode):
		# print('unicode!!')
		retval = datetime.datetime.strptime(xldate, '%m/%d/%Y')
	else:
		# print('Not unicode!!')
		retval = xlrd.xldate.xldate_as_datetime(xldate, 0)
	# retval = xldate_as_tuple(xldate, 0)
	return retval

@blueprint.app_template_filter('format_date_with_strftime')
def format_date_with_strftime(date_to_format, format):
	"""
	Formats a date in your preferred format using strftime
	Includes a convenience format of "ISO" which will return 
	the date in standard ISO format, which should make schema 
	markup easier. You're welcome.
	"""
	return date_to_format.strftime(format) if format.upper() == "ISO" else date_to_format.strftime(format) 