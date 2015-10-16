# -*- coding: utf-8 -*-
from lettuce import *
import json
import time
from utils import *

@step('I have the string (.*)')
def have_the_string(step, string):
    if string == "None":
        world.string = None
    else:
        world.string = string

@step('I convert the string to upper case')
def i_put_it_in_upper_case(step):
    world.string = world.string.upper()

@step('I see the string (.*)')
def i_see_the_string(step, string):
    # Remove new lines for when comparing against kitchen sink XML
    if type(world.string) == unicode or type(world.string) == str:
        world.string = world.string.replace("\n", "\\n")
    # Convert our value to int if world string is int for comparison
    if type(world.string) == int:
        string = int(string)
        
    if string == "None":
        string = None
    if string == "True":
        string = True
    if string == "False":
        string = False
        
    assert world.string == string, "Got %s" % world.string
    
@step(u'I have the list json (.*)')
def i_have_the_list_json(step, json_string):
    if json_string == "None":
        world.list = None
    else:
        world.list = json.loads(json_string)
    
@step(u'I get the first item')
def i_get_the_first_item(step):
    world.string = first(world.list)
    
@step(u'I strip punctuation and space from the string')
def i_strip_punctuation_and_space_from_the_string(step):
    world.string = strip_punctuation_space(world.string)
    
@step(u'I strip punctuation and space from the list')
def i_strip_punctuation_and_space_from_the_list(step):
    world.list = strip_punctuation_space(world.list)
    
@step(u'I have the default (.*)')
def i_have_the_default(step, default):
    if default == "0xDEADBEEF":
        world.default = 0xDEADBEEF
    else:
        world.default = default
    
@step(u'I coerce the string to an int')
def i_coerce_the_string_to_an_int(step):
    world.string = coerce_to_int(world.string, world.default)
    
    
@step(u'I have the date parts (.*), (.*), (.*), (.*)')
def i_have_the_date_parts_year_month_day_tz(step, year, month, day, tz):
    world.year = world.month = world.day = world.tz = None
    if year != "None":
        world.year = year
    if month != "None":
        world.month = month
    if day != "None": 
        world.day = day
    if tz != "None":
        world.tz = tz
    
@step('I have the date format (.*)')
def i_have_the_date_format(step, date_format):
    world.date_format = date_format
    
@step(u'I get the date struct')
def i_get_the_date_struct(step):
    world.date_struct = date_struct(world.year, world.month, world.day, world.tz)
    
@step(u'I see the date struct from date string (.*)')
def i_see_the_date_struct_from_date_string(step, date_string):
    if date_string == "None":
        date_struct = None
    else:
        date_struct = time.strptime(date_string, world.date_format)
        
    assert world.date_struct == date_struct, "Got %s" % world.date_struct
