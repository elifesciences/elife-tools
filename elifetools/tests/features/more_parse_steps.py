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

@step(u'I get the list item (.*)')
def i_get_the_item_item(step, list_item):
    # Given a list or dict item, we need to convert
    #  it to the string from the world.list as specified
    eval_string = "world.list" + list_item
    try:
        world.string = eval(eval_string)
    except:
        world.string = None
        
@step(u'I count the number of components')
def i_count_the_number_of_components(step):
    world.count = len(pm.components(world.filecontent))
    
@step('I count components of the type (\S+)')
def i_count_components_of_the_type(step, type):
    world.count = 0
    list = pm.components(world.filecontent)
    for item in list:
        try:
            if int(item['type']) == type:
                world.count += 1
        except ValueError:
            # Probably not a number
            if item['type'] == type:
                world.count += 1
        except(KeyError):
            continue
    
@step(u'I get the components')
def i_get_the_components(step):
    world.list = pm.components(world.filecontent)
    
@step(u'I count the number of award groups')
def i_count_the_number_of_award_groups(step):
    world.count = len(pm.award_groups(world.filecontent))
    
@step(u'I get the award groups')
def i_get_the_award_groups(step):
    world.list = pm.award_groups(world.filecontent)

@step('I get the full title') 
def get_the_full_title(step):
    world.string = pm.full_title(world.filecontent)

@step('I get the full abstract') 
def get_the_full_abstract(step):
    world.string = pm.full_abstract(world.filecontent)
    
@step(u'I get the digest')
def i_get_the_digest(step):
    world.string = pm.digest(world.filecontent)
    
@step(u'I get the full digest')
def i_get_the_full_digest(step):
    world.string = pm.full_digest(world.filecontent)
    
@step(u'I count the number of related articles')
def i_count_the_number_of_related_articles(step):
    world.count = len(pm.related_article(world.filecontent))
    
@step(u'I get the related articles')
def i_get_the_related_articles(step):
    world.list = pm.related_article(world.filecontent)