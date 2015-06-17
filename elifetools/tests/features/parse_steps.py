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

@step('I get the short title') 
def get_the_short_title(step):
    world.string = pm.title_short(world.filecontent)

@step('I get the slug title') 
def get_the_slug_title(step):
    world.string = pm.title_slug(world.filecontent)

@step('I get the doi')
def get_the_doi(step):
    world.doi = pm.doi(world.filecontent)

@step(u'I see the identifier (.*$)')
def i_see_the_identifier(step, string):
    assert world.doi == string, \
        "Got %s" % world.doi

@step('I get the authors')
def i_get_the_authors(step):
    world.list = pm.authors(world.filecontent)

@step('I count the number of authors')
def count_the_number_of_authors(step):
    world.count = len(pm.authors(world.filecontent))

@step(u'I count the number of contributors')
def i_count_the_number_of_contributors(step):
    world.count = len(pm.contributors(world.filecontent))

@step(u'I count the total as (.*)')
def i_count_the_total_as(step, number):
    # Allow None because sometimes it is not a list returned
    if number == "None":
        assert world.count is None, \
            "Got %s" % world.count
    else:
        number = int(number)
        assert world.count == number, \
            "Got %d" % world.count

@step(u'I see list index (\d+) as (.*)')
def i_see_list_index_as_val(step, index, val):
    # Turn index to int
    index = int(index)
    
    # Allow comparing different types
    if val == "None":
        val = None
    elif val == "True" or val == "False":
        val = bool(val)
    else:
        # Try to compare integers if it is int
        try:
            val = int(val)
        except ValueError:
            pass
    
    # Get the value from the list
    try:
        value = world.list[index]
    except KeyError:
        value = None
            
    # Remove new lines for when comparing against kitchen sink XML
    if type(value) == unicode or type(value) == str:
        value = value.replace("\n", "")
    
    assert value == val, \
        "Got %s" % value

@step('I count the number of references')
def count_the_number_of_references(step):
    world.count = len(pm.references(world.filecontent))

@step(u'I get the total number of references as (\d+)')
def i_get_the_total_number_of_references_as(step, number):
    number = int(number)
    assert world.count == number, \
        "Got %d" % world.count

@step('I count references from the year (\S+)')
def count_referneces_from_the_year(step, year):
    world.count = 0
    references = pm.refs(world.filecontent)
    for ref in references:
        try:
            if int(ref['year']) == int(year):
                world.count += 1
        except ValueError:
            # Probably not a number
            if ref['year'] == year:
                world.count += 1
        except(KeyError):
            continue

@step('I count references from the journal (.*$)')
def count_references_from_the_journal(step, journal):
    if (journal == 'None'):
      journal = None
    world.count = 0
    references = pm.refs(world.filecontent)
    for ref in references:
        try:
            if ref['source'] == journal:
                world.count += 1
        except(KeyError):
            if journal == None:
                world.count += 1

@step('I get the references')
def i_get_the_references(step):
    world.list = pm.refs(world.filecontent)

@step(u'I get the URL of the license')
def i_get_the_url_of_license(step):
    world.string = pm.license_url(world.filecontent)

@step(u'I get the license')
def i_get_the_license(step):
    world.string = pm.license(world.filecontent)

@step(u'I get the journal id')
def i_get_the_journal_id(step):
    world.string = pm.journal_id(world.filecontent)
    
@step(u'I have the pub format (\S+)')
def i_have_the_pub_format_pub_format(step, pub_format):
    world.pub_format = pub_format
    assert world.pub_format is not None, \
        "Got pub_format %s" % world.pub_format

@step(u'I get the issn of the journal')
def i_get_the_issn_of_the_journal(step):
    world.string = pm.journal_issn(world.filecontent, world.pub_format)
    
@step(u'I get the journal title')
def i_get_the_journal_title(step):
    world.string = pm.journal_title(world.filecontent)
    
@step(u'I get the publisher name')
def i_get_the_publisher_name(step):
    world.string = pm.publisher(world.filecontent)

@step(u'I get the copyright statement')
def i_get_the_copyright_statement(step):
    world.string = pm.copyright_statement(world.filecontent)
    
@step(u'I get the copyright year')
def i_get_the_copyright_year(step):
    world.string = pm.copyright_year(world.filecontent)

@step(u'I get the copyright holder')
def i_get_the_copyright_holder(step):
    world.string = pm.copyright_holder(world.filecontent)

@step(u'I get the article type')
def i_get_the_article_type(step):
    world.string = pm.article_type(world.filecontent)

@step(u'I have the index (\d+)')
def i_have_the_index(step, index):
    world.index = int(index)
    assert world.index is not None, \
        "Got index %d" % world.index
    
@step(u'I get the correspondence')
def i_get_the_correspondence(step):
    world.list = pm.correspondence(world.filecontent)
    
@step(u'I get the conflict')
def i_get_the_conflict(step):
    world.list = pm.conflict(world.filecontent)
    
@step(u'I get the pub date date')
def i_get_the_pub_date(step):
    world.string = pm.pub_date_date(world.filecontent)
    
@step(u'I get the pub date day')
def i_get_the_pub_date_day(step):
    world.string = pm.pub_date_day(world.filecontent)
    
@step(u'I get the pub date month')
def i_get_the_pub_date_month(step):
    world.string = pm.pub_date_month(world.filecontent)
    
@step(u'I get the pub date year')
def i_get_the_pub_date_year(step):
    world.string = pm.pub_date_year(world.filecontent)
    
@step(u'I get the pub date timestamp')
def i_get_the_pub_date_timestamp(step):
    world.string = pm.pub_date_timestamp(world.filecontent)

@step(u'I get the received date date')
def i_get_the_received_date_date(step):
    world.string = pm.received_date_date(world.filecontent)
    
@step(u'I get the received date day')
def i_get_the_received_date_day(step):
    world.string = pm.received_date_day(world.filecontent)
    
@step(u'I get the received date month')
def i_get_the_received_date_month(step):
    world.string = pm.received_date_month(world.filecontent)
    
@step(u'I get the received date year')
def i_get_the_received_date_year(step):
    world.string = pm.received_date_year(world.filecontent)
    
@step(u'I get the received date timestamp')
def i_get_the_received_date_timestamp(step):
    world.string = pm.received_date_timestamp(world.filecontent)

@step(u'I get the accepted date date')
def i_get_the_accepted_date_date(step):
    world.string = pm.accepted_date_date(world.filecontent)
    
@step(u'I get the accepted date day')
def i_get_the_accepted_date_day(step):
    world.string = pm.accepted_date_day(world.filecontent)
    
@step(u'I get the accepted date month')
def i_get_the_accepted_date_month(step):
    world.string = pm.accepted_date_month(world.filecontent)
    
@step(u'I get the accepted date year')
def i_get_the_accepted_date_year(step):
    world.string = pm.accepted_date_year(world.filecontent)
    
@step(u'I get the accepted date timestamp')
def i_get_the_accepted_date_timestamp(step):
    world.string = pm.accepted_date_timestamp(world.filecontent)

@step(u'I get the collection year')
def i_get_the_collection_year(step):
    world.string = pm.collection_year(world.filecontent)

@step(u'I get the is poa')
def i_get_the_is_poa(step):
    world.string = pm.is_poa(world.filecontent)

@step(u'I get the abstract')
def i_get_the_abstract(step):
    world.string = pm.abstract(world.filecontent)

@step(u'I get the funding statement')
def i_get_the_funding_statement(step):
    world.string = pm.funding_statement(world.filecontent)

@step(u'I get the acknowledgements')
def i_get_the_acknowledgements(step):
    world.string = pm.ack(world.filecontent)

@step(u'I count the number of subject area')
def i_count_the_number_of_subject_area(step):
    world.count = len(pm.subject_area(world.filecontent))
    
@step(u'I get the subject area')
def i_get_the_subject_area(step):
    world.list = pm.subject_area(world.filecontent)

@step(u'I count the number of display channel')
def i_count_the_number_of_display_channel(step):
    world.count = len(pm.display_channel(world.filecontent))
    
@step(u'I get the display channel')
def i_get_the_display_channel(step):
    world.list = pm.display_channel(world.filecontent)

"""
Note: Adding more steps seems to break other tests, so maybe
      add more in the more_parse_steps.py file
"""

def set_file_location(doc):
    document = doc.lstrip('"').rstrip('"')
    file_location = test_xml_path + document
    return file_location
