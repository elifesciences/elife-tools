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
    assert world.string == string, \
        "Got %s" % world.string 
