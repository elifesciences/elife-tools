Feature: Get author notes from the document
  In order to use the author notes of this article
  as a script 
  I will parse the author notes from the xml file
  
  Scenario Outline: Count the number of author notes
    Given I have the document <document>
    When I count the number of author notes
    Then I count the total as <count>
  
  Examples:
    | document                    | count
    | elife-kitchen-sink.xml      | 3    
    | elife00013.xml              | 1      


  Scenario Outline: Get author notes
    Given I have the document <document>
    When I get the author notes
    Then I see list index <idx> as <val>
  
  Examples:
    | document                    | idx | val
    | elife-kitchen-sink.xml      | 0   | †These authors contributed equally to this work
    | elife-kitchen-sink.xml      | 1   | ‡These authors contributed equally to this work
    | elife-kitchen-sink.xml      | 2   | **Deceased
    | elife00013.xml              | 0   | †These authors contributed equally to this work

