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

@step(u'I count the number of full keyword groups')
def i_count_the_number_of_full_keyword_groups(step):
    world.count = len(pm.full_keyword_groups(world.filecontent))

@step(u'I count the number of author notes')
def i_count_the_number_of_author_notes(step):
    try:
        world.count = len(pm.author_notes(world.filecontent))
    except TypeError:
        world.count = None
    
@step(u'I get the author notes')
def i_get_the_author_notes(step):
    world.list = pm.author_notes(world.filecontent)

@step("I count the number of full author notes")
def i_count_the_number_of_full_author_notes(step):
    try:
        world.count = len(pm.full_author_notes(world.filecontent))
    except TypeError:
        world.count = None

@step(u'I get the full author notes')
def i_get_the_full_author_notes(step):
    world.list = pm.full_author_notes(world.filecontent)

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
        if 'type' in item and item['type'] == type:
            world.count += 1
    
@step(u'I get the components')
def i_get_the_components(step):
    world.list = pm.components(world.filecontent)
    
@step(u'I count the number of award groups')
def i_count_the_number_of_award_groups(step):
    world.count = len(pm.award_groups(world.filecontent))
    
@step(u'I get the award groups')
def i_get_the_award_groups(step):
    world.list = pm.award_groups(world.filecontent)

@step(u'I count the number of full award groups')
def i_count_the_number_of_full_award_groups(step):
    world.count = len(pm.full_award_groups(world.filecontent))

@step(u'I get the full award groups')
def i_get_the_full_award_groups(step):
    world.list = pm.full_award_groups(world.filecontent)

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
    
@step(u'I get the volume')
def i_get_the_volume(step):
    world.string = pm.volume(world.filecontent)

@step(u'I get the elocation-id')
def i_get_the_elocation_id(step):
    world.string = pm.elocation_id(world.filecontent)
    
@step(u'I count the number of category')
def i_count_the_number_of_category(step):
    world.count = len(pm.category(world.filecontent))
    
@step(u'I get the category')
def i_get_the_category(step):
    world.list = pm.category(world.filecontent)
    
@step(u'I count the number of non-byline authors')
def i_count_the_number_of_non_byline_authors(step):
    world.count = len(pm.authors_non_byline(world.filecontent))
    
@step(u'I get the non-byline authors')
def i_get_the_non_byline_authors(step):
    world.list = pm.authors_non_byline(world.filecontent)
    
@step(u'I get the publisher id')
def i_get_the_publisher_id(step):
    world.string = pm.publisher_id(world.filecontent)

@step(u'I count the number of component DOI')
def i_count_the_number_of_component_doi(step):
    world.count = len(pm.component_doi(world.filecontent))
    
@step(u'I get the component DOI')
def i_get_the_component_doi(step):
    world.list = pm.component_doi(world.filecontent)
    
@step(u'I count permissions of components index (\d+)')
def i_count_permissions_of_components_index(step, index):
    if not world.list[int(index)].get('permissions'):
        world.count = 0
    else:
        world.count = len(world.list[int(index)]['permissions'])
            
@step(u'I count the number of author contributions')
def i_count_the_number_of_author_contributions(step):
    try:
        world.count = len(pm.author_contributions(world.filecontent, "con"))
    except TypeError:
        world.count = None
    
@step(u'I get the author contributions')
def i_get_the_author_contributions(step):
    world.list = pm.author_contributions(world.filecontent, "con")
    
@step(u'I get the impact statement')
def i_get_the_impact_statement(step):
    world.string = pm.impact_statement(world.filecontent)
    
@step(u'I count the number of related object ids')
def i_count_the_number_of_related_object_ids(step):
    world.count = len(pm.related_object_ids(world.filecontent))
    
@step(u'I get the related object ids')
def i_get_the_related_object_ids(step):
    world.list = pm.related_object_ids(world.filecontent)

@step(u'I get the string of the list')
def i_get_the_string_of_the_list(step):
    world.string = str(world.list)

@step(u'I count the number of competing interests')
def i_count_the_number_of_competing_interests(step):
    try:
        world.count = len(pm.competing_interests(world.filecontent, "conflict"))
    except TypeError:
        world.count = None
        
@step(u'I get the competing interests')
def i_get_the_competing_interests(step):
    world.list = pm.competing_interests(world.filecontent, "conflict")

@step(u'I get the full affiliation')
def i_get_the_full_affiliation(step):
    world.list = pm.full_affiliation(world.filecontent)
    
@step(u'I count the number of media')
def i_count_the_number_of_media(step):
    world.count = len(pm.media(world.filecontent))
    
@step(u'I get the media')
def i_get_the_media(step):
    world.list = pm.media(world.filecontent)
    
@step(u'I count the number of graphics')
def i_count_the_number_of_graphics(step):
    world.count = len(pm.graphics(world.filecontent))

@step(u'I get the graphics')
def i_get_the_graphics(step):
    world.list = pm.graphics(world.filecontent)
    
@step(u'I count the number of inline graphics')
def i_count_the_number_of_inline_graphics(step):
    world.count = len(pm.inline_graphics(world.filecontent))
    
@step(u'I get the inline graphics')
def i_get_the_inline_graphics(step):
    world.list = pm.inline_graphics(world.filecontent)

@step(u'I count the number of self uri')
def i_count_the_number_of_self_uri(step):
    world.count = len(pm.self_uri(world.filecontent))

@step(u'I get the self uri')
def i_get_the_self_uri(step):
    world.list = pm.self_uri(world.filecontent)
    