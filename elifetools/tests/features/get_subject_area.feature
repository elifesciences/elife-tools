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


  Scenario Outline: Get subject area
    Given I have the document <document>
    When I get the subject area
    Then I see list index <idx> as <val>
  
  Examples:
    | document                    | idx | val
    | elife-kitchen-sink.xml      | 0   | Research article
    | elife-kitchen-sink.xml      | 1   | Cell biology
    | elife-kitchen-sink.xml      | 2   | Computer science
    | elife00013.xml              | 0   | Research article
    | elife00013.xml              | 1   | Cell biology
