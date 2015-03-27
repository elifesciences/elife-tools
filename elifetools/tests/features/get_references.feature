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
