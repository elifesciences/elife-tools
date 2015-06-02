Feature: Get component DOI from the document
  In order to extract component DOI objects in an article
  as a script 
  I will parse the component DOI from the xml file

  Scenario Outline: Count the number of component DOI
    Given I have the document <document>
    When I count the number of component DOI
    Then I count the total as <count>

  Examples:
    | document                    | count
    | elife-kitchen-sink.xml      | 40
    | elife00013.xml              | 28
    | elife_poa_e06828.xml        | 0


  Scenario Outline: Get the component DOI
    Given I have the document <document>
    When I get the component DOI
    And I get the list item <list_item>
    Then I see the string <string>

  Examples:
    | document                    | list_item                  | string
    | elife-kitchen-sink.xml      | [0]['doi']                 | 10.7554/eLife.00013.001
    | elife00013.xml              | [0]['doi']                 | 10.7554/eLife.00013.001
    | elife_poa_e06828.xml        | [0]['doi']                 | None