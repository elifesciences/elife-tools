Feature: Get inline graphic tag data from the document
  In order to extract inline graphic from an article
  as a script 
  I will parse the inline graphic tag and details from the xml file

  Scenario Outline: Count the number of inline graphics
    Given I have the document <document>
    When I count the number of inline graphics
    Then I count the total as <count>

  Examples:
    | document                    | count
    | elife-kitchen-sink.xml      | 1
    | elife00013.xml              | 0
    | elife00240.xml              | 1
    | elife_poa_e06828.xml        | 0

  Scenario Outline: Get the inline graphics
    Given I have the document <document>
    When I get the inline graphics
    And I get the list item <list_item>
    Then I see the string <string>
  
  Examples:
    | document                    | list_item                           | string
    | elife-kitchen-sink.xml      | [0]['xlink_href']                   | elife00013inf001
    | elife-kitchen-sink.xml      | [0]['position']                     | 1
    | elife-kitchen-sink.xml      | [0]['ordinal']                      | 1

    | elife00240.xml              | [0]['xlink_href']                   | elife00240inf001
    | elife00240.xml              | [0]['position']                     | 1
    | elife00240.xml              | [0]['ordinal']                      | 1
