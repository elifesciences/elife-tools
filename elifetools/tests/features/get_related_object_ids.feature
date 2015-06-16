Feature: Get related object ids from the document
  In order to use the keywords of this article
  as a script 
  I will parse the related object ids from the xml file
  
  Scenario Outline: Count the number of related object ids
    Given I have the document <document>
    When I count the number of related object ids
    Then I count the total as <count>
  
  Examples:
    | document                    | count
    | elife-kitchen-sink.xml      | 3    
    | elife00013.xml              | 0      
    | elife_poa_e06828.xml        | 0
    | elife02304.xml              | 15

  Scenario Outline: Get related object ids
    Given I have the document <document>
    When I get the related object ids
    And I get the string of the list
    Then I see the string <string>
  
  Examples:
    | document                    | string
    | elife-kitchen-sink.xml      | {u'dataro1': {}, u'dataro2': {}, u'dataro3': {}}

