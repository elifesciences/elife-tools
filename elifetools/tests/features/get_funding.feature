Feature: Get funding data from the article
  In order to use the funding data of this article
  as a script 
  I will parse the funding from the xml file
  
  Scenario Outline: Get the funding statement
    Given I have the document <document>
    When I get the funding statement
    Then I see the string <funding_statement>
  
  Examples:
    | document                    | funding_statement   
    | elife00013.xml              | The funders had no role in study design, data collection and interpretation, or the decision to submit the work for publication.
    
    
  Scenario Outline: Count the number of award groups
    Given I have the document <document>
    When I count the number of award groups
    Then I count the total as <awards_groups>

  Examples:
    | document                    | awards_groups
    | elife-kitchen-sink.xml      | 7
    | elife00013.xml              | 6
    
    

  Scenario Outline: Get the award groups
    Given I have the document <document>
    When I get the award groups
    And I get the list item <list_item>
    Then I see the string <string>

  Examples:
    | document                    | list_item                         | string
    | elife00013.xml              | [0]['funding_source'][0]          | Gordon and Betty Moore Foundation Marine Microbiology Initiative
    | elife00013.xml              | [0]['recipient'][0]               | Nicole King
    | elife00013.xml              | [1]['award_id'][0]                | F32 GM086054
    
    | elife-kitchen-sink.xml      | [0]['funding_source'][0]           | \n\ndx.doi.org/10.13039/100000011\nHoward Hughes Medical Institute\n\n
    | elife-kitchen-sink.xml      | [0]['recipient'][0]                | Nicole King
    
    
  Scenario Outline: Count the number of full award groups
    Given I have the document <document>
    When I count the number of full award groups
    Then I count the total as <awards_groups>

  Examples:
    | document                    | awards_groups
    | elife-kitchen-sink.xml      | 7
    | elife00013.xml              | 6
    

  Scenario Outline: Get the full award groups
    Given I have the document <document>
    When I get the full award groups
    And I get the list item <list_item>
    Then I see the string <string>

  Examples:
    | document                    | list_item                       | string
    
    | elife-kitchen-sink.xml      | [0]['par-1']['id-type']         | FundRef
    | elife-kitchen-sink.xml      | [0]['par-1']['institution']        | Howard Hughes Medical Institute
    | elife-kitchen-sink.xml      | [0]['par-1']['id']                 | dx.doi.org/10.13039/100000011
    | elife-kitchen-sink.xml      | [0]['par-1']['award-id']           | None
    
    | elife-kitchen-sink.xml      | [1]['par-2']['award-id']           | F32 GM086054
    | elife-kitchen-sink.xml      | [1]['par-2']['id']                 | dx.doi.org/10.13039/100000002
    