Feature: Get self uri tag data from the document
  In order to extract self uri from an article
  as a script 
  I will parse the self uri from the xml file

  Scenario Outline: Count the number of self uri
    Given I have the document <document>
    When I count the number of self uri
    Then I count the total as <count>

  Examples:
    | document                    | count
    | elife-kitchen-sink.xml      | 1
    | elife00013.xml              | 1
    | elife00007.xml              | 1
    | elife00240.xml              | 1
    | elife02935.xml              | 1
    | elife_poa_e06828.xml        | 0

  Scenario Outline: Get the self uri
    Given I have the document <document>
    When I get the self uri
    And I get the list item <list_item>
    Then I see the string <string>
  
  Examples:
    | document                    | list_item                        | string
    | elife-kitchen-sink.xml      | [0]['type']                      | self-uri
    | elife-kitchen-sink.xml      | [0]['xlink_href']                | elife00013.pdf
    | elife-kitchen-sink.xml      | [0]['content-type']              | pdf
    
    | elife02935.xml              | [0]['type']                      | self-uri
    | elife02935.xml              | [0]['xlink_href']                | elife02935.pdf
    | elife02935.xml              | [0]['content-type']              | pdf
