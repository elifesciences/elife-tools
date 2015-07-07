Feature: Get media tag data from the document
  In order to extract media from an article
  as a script 
  I will parse the media tag and details from the xml file

  Scenario Outline: Count the number of media
    Given I have the document <document>
    When I count the number of media
    Then I count the total as <count>

  Examples:
    | document                    | count
    | elife-kitchen-sink.xml      | 6
    | elife00013.xml              | 0
    | elife00007.xml              | 4
    | elife00240.xml              | 0
    | elife02935.xml              | 6
    | elife_poa_e06828.xml        | 0

  Scenario Outline: Get the media
    Given I have the document <document>
    When I get the media
    And I get the list item <list_item>
    Then I see the string <string>
  
  Examples:
    | document                    | list_item                        | string
    | elife-kitchen-sink.xml      | [0]['mimetype']                  | application
    | elife-kitchen-sink.xml      | [0]['mime-subtype']              | xlsx
    | elife-kitchen-sink.xml      | [0]['content-type']              | None
    | elife-kitchen-sink.xml      | [0]['position']                  | 1
    | elife-kitchen-sink.xml      | [0]['ordinal']                   | 1
    | elife-kitchen-sink.xml      | [0]['xlink_href']                | elife00013s001.xlsx
    | elife-kitchen-sink.xml      | [0]['component_doi']             | None
    | elife-kitchen-sink.xml      | [0]['parent_component_doi']      | 10.7554/eLife.00013.004
    | elife-kitchen-sink.xml      | [0]['parent_type']               | supplementary-material
    | elife-kitchen-sink.xml      | [0]['parent_ordinal']            | 1
    | elife-kitchen-sink.xml      | [0]['parent_sibling_ordinal']    | 1
    | elife-kitchen-sink.xml      | [0]['p_parent_type']             | fig
    | elife-kitchen-sink.xml      | [0]['p_parent_ordinal']          | 1
    | elife-kitchen-sink.xml      | [0]['p_parent_sibling_ordinal']  | 1
    | elife-kitchen-sink.xml      | [0]['p_p_parent_ordinal']        | None
    | elife-kitchen-sink.xml      | [0]['p_p_parent_type']           | None
    | elife-kitchen-sink.xml      | [0]['p_p_parent_ordinal']        | None
    
    | elife02935.xml              | [5]['mimetype']                  | application
    | elife02935.xml              | [5]['mime-subtype']              | xlsx
    | elife02935.xml              | [5]['content-type']              | None
    | elife02935.xml              | [5]['position']                  | 6
    | elife02935.xml              | [5]['ordinal']                   | 6
    | elife02935.xml              | [5]['xlink_href']                | elife02935s006.xlsx
    | elife02935.xml              | [5]['parent_component_doi']      | 10.7554/eLife.02935.026
    | elife02935.xml              | [5]['parent_type']               | supplementary-material
    | elife02935.xml              | [5]['parent_ordinal']            | 6
    | elife02935.xml              | [5]['parent_sibling_ordinal']    | 6
    | elife02935.xml              | [5]['p_parent_type']             | None
    | elife02935.xml              | [5]['p_parent_ordinal']          | None
    
    | elife00007.xml              | [1]['mimetype']                  | video
    | elife00007.xml              | [1]['mime-subtype']              | avi
    | elife00007.xml              | [1]['content-type']              | glencoe play-in-place height-250 width-310
    | elife00007.xml              | [1]['position']                  | 2
    | elife00007.xml              | [1]['ordinal']                   | 2
    | elife00007.xml              | [1]['xlink_href']                | elife00007v002.AVI
    | elife00007.xml              | [1]['component_doi']             | 10.7554/eLife.00007.017
    | elife00007.xml              | [1]['parent_component_doi']      | None
    | elife00007.xml              | [1]['parent_type']               | None
    | elife00007.xml              | [1]['parent_ordinal']            | None
    | elife00007.xml              | [1]['p_parent_type']             | None
    | elife00007.xml              | [1]['p_parent_ordinal']          | None