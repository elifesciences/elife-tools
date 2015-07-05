Feature: Get graphic tag data from the document
  In order to extract graphic from an article
  as a script 
  I will parse the graphic tag and details from the xml file

  Scenario Outline: Count the number of graphics
    Given I have the document <document>
    When I count the number of graphics
    Then I count the total as <count>

  Examples:
    | document                    | count
    | elife-kitchen-sink.xml      | 26
    | elife00013.xml              | 23
    | elife00007.xml              | 10
    | elife00240.xml              | 1
    | elife02935.xml              | 19
    | elife_poa_e06828.xml        | 0

  Scenario Outline: Get the graphics
    Given I have the document <document>
    When I get the graphics
    And I get the list item <list_item>
    Then I see the string <string>
  
  Examples:
    | document                    | list_item                           | string
    | elife-kitchen-sink.xml      | [0]['xlink_href']                   | elife00013f001
    | elife-kitchen-sink.xml      | [0]['parent_type']                  | fig
    | elife-kitchen-sink.xml      | [0]['parent_ordinal']               | 1
    | elife-kitchen-sink.xml      | [0]['parent_component_doi']         | 10.7554/eLife.00013.003
    | elife-kitchen-sink.xml      | [0]['parent_parent_type']           | fig-group
    | elife-kitchen-sink.xml      | [0]['parent_parent_ordinal']        | 1
    | elife-kitchen-sink.xml      | [0]['parent_parent_component_doi']  | 10.7554/eLife.00013.003

    | elife-kitchen-sink.xml      | [5]['xlink_href']                   | elife00013fs002
    | elife-kitchen-sink.xml      | [5]['parent_type']                  | fig
    | elife-kitchen-sink.xml      | [5]['parent_ordinal']               | 5
    | elife-kitchen-sink.xml      | [5]['parent_component_doi']         | 10.7554/eLife.00013.013
    | elife-kitchen-sink.xml      | [5]['parent_parent_type']           | fig-group
    | elife-kitchen-sink.xml      | [5]['parent_parent_ordinal']        | 2
    | elife-kitchen-sink.xml      | [5]['parent_parent_component_doi']  | 10.7554/eLife.00013.012
