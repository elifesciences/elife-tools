Feature: get references from the document
  In order to extract the references citied in an article
  as a script 
  I will parse the references from the xml file

  Scenario Outline: Count the number of references
    Given I have the document <document>
    When I count the number of references
    Then I count the total as <references>

  Examples:
    | document                    | references
    | elife-kitchen-sink.xml      | 103
    | elife00013.xml              | 105
    | elife_poa_e06828.xml        | 0

  Scenario Outline: Count the number of references from a particular year
    Given I have the document <document>
    When I count references from the year <year>
    Then I get the total number of references as <references>
    
  Examples:
    | document                    | year  | references
    | elife-kitchen-sink.xml      | 2003  | 5
    | elife00013.xml              | 1999  | 4
    | elife00013.xml              | 2004a | 1
    
  Scenario Outline: Count the number of references from a particular journal
    Given I have the document <document>
    When I count references from the journal <journal>
    Then I count the total as <references>
    
  Examples:
    | document                    | journal                       | references
    | elife-kitchen-sink.xml      | Anaerobe                      | 1
    | elife00013.xml              | Int J Syst Evol Microbiol     | 17

  Scenario Outline: Get references
    Given I have the document <document>
    When I get the references
    And I get the list item <list_item>
    Then I see the string <string>
  
  Examples:
    | document                    | list_item                       | string
    | elife00013.xml              | [0]['etal']                     | None
    | elife00013.xml              | [0]['id']                       | bib1
    | elife00013.xml              | [9]['etal']                     | True
    | elife00013.xml              | [0]['ref']                      | AgostaWC1992Chemical communicationScientific American PressNew York
    | elife00013.xml              | [0]['publisher_name']           | Scientific American Press
    | elife00013.xml              | [0]['publisher_loc']            | New York
    | elife00013.xml              | [0]['authors'][0]               | WC Agosta
    | elife00013.xml              | [0]['article_doi']              | 10.7554/eLife.00013
    | elife00013.xml              | [0]['position']                 | 1
    | elife00013.xml              | [1]['ref']                      | AhmedIYokotaAFujiwaraT2007Chimaereicella boritolerans sp nov., a boron-tolerant and alkaliphilic bacterium of the family Flavobacteriaceae isolated from soilInt J Syst Evol Microbiol57986992
    | elife00013.xml              | [1]['authors'][0]               | I Ahmed
    | elife00013.xml              | [1]['authors'][1]               | A Yokota
    | elife00013.xml              | [1]['year']                     | 2007
    | elife00013.xml              | [1]['article_title']            | Chimaereicella boritolerans sp nov., a boron-tolerant and alkaliphilic bacterium of the family Flavobacteriaceae isolated from soil
    | elife00013.xml              | [1]['source']                   | Int J Syst Evol Microbiol
    | elife00013.xml              | [1]['volume']                   | 57
    | elife00013.xml              | [1]['fpage']                    | 986
    | elife00013.xml              | [1]['lpage']                    | 992
    | elife00013.xml              | [1]['position']                 | 2
    

    
    