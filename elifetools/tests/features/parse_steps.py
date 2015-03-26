# -*- coding: utf-8 -*-
from lettuce import *
import parseJATS
import os

test_xml_path = world.basedir + os.sep +  "sample-xml" + os.sep

# Set the default parser for when it is not specified
pm = parseJATS

@step('I have the document (\S+)')
def have_the_document(step, document):
    world.document = document
    file_location = set_file_location(document)
    world.filecontent = pm.parse_document(file_location)

@step('I get the title') 
def get_the_title(step):
    world.string = pm.title(world.filecontent)

@step('I get the doi')
def get_the_doi(step):
    world.doi = pm.doi(world.filecontent)

@step(u'I see the identifier (.*$)')
def i_see_the_identifier(step, string):
    assert world.doi == string, \
        "Got %s" % world.doi

@step('I get the pmid')
def get_the_pmid(step):
    world.pmid = pm.pmid(world.filecontent)

@step(u'I see the number (.*$)')
def i_see_the_number(step, number):
    if (number == 'None'):
      number = None
    assert world.pmid == number, \
        "Got %d" % int(world.pmid)

@step('I get the authors')
def i_get_the_authors(step):
    world.authors = pm.authors(world.filecontent)

@step('I count the number of authors')
def count_the_number_of_authors(step):
    world.authors_count = len(pm.authors(world.filecontent))

@step(u'I count the total authors as (\d+)')
def i_count_the_total_authors_as(step, number):
    number = int(number)
    assert world.authors_count == number, \
        "Got %d" % world.authors_count

@step(u'I see author index (\d+) (\S+) (\d*) as (.*)')
def i_see_author_index_attribute_subindex_as_val(step, index, attribute, subindex, val):
    # Turn index to int
    index = int(index)
    if subindex != "":
        subindex = int(subindex)
    
    # Allow comparing different types
    if val == "None":
        val = None
    else:
        # Try to compare integers if it is int
        try:
            val = int(val)
        except ValueError:
            pass
    
    # Get the value from the author
    if subindex != "":
        value = world.authors[index][attribute][subindex]
    else:
        value = world.authors[index][attribute]
    
    
    assert value == val, \
        "Got %s" % value

@step('I count the number of references')
def count_the_number_of_references(step):
    world.references_count = len(pm.references(world.filecontent))

@step(u'I get the total number of references as (\d+)')
def i_get_the_total_number_of_references_as(step, number):
    number = int(number)
    assert world.references_count == number, \
        "Got %d" % world.references_count

@step('I count references from the year (\S+)')
def count_referneces_from_the_year(step, year):
    world.references_count = 0
    references = pm.refs(world.filecontent)
    for ref in references:
        try:
            if int(ref['year']) == int(year):
                world.references_count += 1
        except ValueError:
            # Probably not a number
            if ref['year'] == year:
                world.references_count += 1
        except(KeyError):
            continue

@step('I count the number of references from the journal (.*$)')
def count_the_number_of_references_from_the_journal(step, journal):
    if (journal == 'None'):
      journal = None
    world.references_count = 0
    references = pm.refs(world.filecontent)
    for ref in references:
        try:
            if ref['source'] == journal:
                world.references_count += 1
        except(KeyError):
            if journal == None:
                world.references_count += 1

def set_file_location(doc):
    document = doc.lstrip('"').rstrip('"')
    file_location = test_xml_path + document
    return file_location
