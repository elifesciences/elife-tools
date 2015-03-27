# -*- coding: utf-8 -*-
from lettuce import *

@step('I have the string "(.*)"')
def have_the_string(step, string):
    world.string = string

@step('I convert the string to upper case')
def i_put_it_in_upper_case(step):
    world.string = world.string.upper()

@step('I see the string "(.*)"')
@step('I see the string (.*)')
def i_see_the_string(step, string):
    # Remove new lines for when comparing against kitchen sink XML
    if type(world.string) == unicode or type(world.string) == str:
        world.string = world.string.replace("\n", "")
    # Convert our value to int if world string is int for comparison
    if type(world.string) == int:
        string = int(string)
        
    if string == "None":
        string = None
    if string == "True" or string == "False":
        string = bool(string)
        
    assert world.string == string, \
        "Got %s" % world.string 