from lettuce import *
import parseJATS

# Set the default parser for when it is not specified
pm = parseJATS

@step(u'I count the number of research organism')
def i_count_the_number_of_research_organism(step):
    world.count = len(pm.research_organism(world.filecontent))
    
@step(u'I get the research organism')
def i_get_the_research_organism(step):
    world.list = pm.research_organism(world.filecontent)
    
@step(u'I count the number of keywords')
def i_count_the_number_of_keywords(step):
    world.count = len(pm.keywords(world.filecontent))
    
@step(u'I get the keywords')
def i_get_the_keywords(step):
    world.list = pm.keywords(world.filecontent)

@step(u'I count the number of author notes')
def i_count_the_number_of_author_notes(step):
    world.count = len(pm.author_notes(world.filecontent))
    
@step(u'I get the author notes')
def i_get_the_author_notes(step):
    world.list = pm.author_notes(world.filecontent)