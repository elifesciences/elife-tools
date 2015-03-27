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