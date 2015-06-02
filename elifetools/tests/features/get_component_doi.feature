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

 