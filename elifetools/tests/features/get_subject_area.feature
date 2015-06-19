Feature: Get subject areas from the document
  In order to use the subject area of this article
  as a script 
  I will parse the subject area from the xml file
  
  Scenario Outline: Count the number of subject areas
    Given I have the document <document>
    When I count the number of subject area
    Then I count the total as <count>
  
  Examples:
    | document                    | count
    | elife-kitchen-sink.xml      | 3      
    | elife00013.xml              | 2       
    | elife_poa_e06828.xml        | 3
    

  Scenario Outline: Get subject area
    Given I have the document <document>
    When I get the subject area
    And I get the list item <list_item>
    Then I see the string <string>
  
  Examples:
    | document                    | list_item | string
    | elife-kitchen-sink.xml      | [0]       | Research article
    | elife-kitchen-sink.xml      | [1]       | Cell biology
    | elife-kitchen-sink.xml      | [2]       | Computer science
    | elife00013.xml              | [0]       | Research article
    | elife00013.xml              | [1]       | Cell biology
    | elife_poa_e06828.xml        | [0]       | Research article
    | elife_poa_e06828.xml        | [1]       | Developmental biology and stem cells
    | elife_poa_e06828.xml        | [2]       | Neuroscience
    
  Scenario Outline: Count the number of full subject area
    Given I have the document <document>
    When I count the number of full subject area
    Then I count the total as <count>

  Examples:
    | document                    | count
    | elife-kitchen-sink.xml      | 2
    | elife00013.xml              | 2
    | elife00240.xml              | 3 

  Scenario Outline: Get full subject area
    Given I have the document <document>
    When I get the full subject area
    And I get the list item <list_item>
    Then I see the string <string>

  Examples:
    | document                    | list_item                   | string
    | elife-kitchen-sink.xml      | ['heading'][0]              | Cell biology
    | elife-kitchen-sink.xml      | ['heading'][1]              | Computer science
    | elife-kitchen-sink.xml      | ['display-channel'][0]      | Research article

    | elife00240.xml              | ['sub-display-channel'][0]  | Plant biology
    | elife00240.xml              | ['heading'][0]              | Genomics and evolutionary biology
    | elife00240.xml              | ['heading'][1]              | Plant biology
    | elife00240.xml              | ['display-channel'][0]      | Insight
    
    
