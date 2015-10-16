Feature: Get research organism from the document
  In order to use the research organism of this article
  as a script 
  I will parse the research organisms from the xml file
  
  Scenario Outline: Count the number of research organisms
    Given I have the document <document>
    When I count the number of research organism
    Then I count the total as <count>
  
  Examples:
    | document                    | count
    | elife-kitchen-sink.xml      | 3     
    | elife00013.xml              | 1       
    | elife_poa_e06828.xml        | 1
    | elife07586.xml              | 0
    

  Scenario Outline: Get research organism
    Given I have the document <document>
    When I get the research organism
    And I get the list item <list_item>
    Then I see the string <string>
  
  Examples:
    | document                    | list_item   | string
    | elife-kitchen-sink.xml      | [0]         | Mouse
    | elife00013.xml              | [0]         | Other
    | elife_poa_e06828.xml        | [0]         | Mouse