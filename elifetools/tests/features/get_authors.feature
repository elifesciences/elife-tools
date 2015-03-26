Feature: get authors from the document
  In order to put my author names in my api
  as a script 
  I will parse the authors from the xml file
  
  Scenario Outline: Count the number of authors
    Given I have the document <document>
    When I count the number of authors 
    Then I count the total authors as <authors>
  
  Examples:
    | document                    | authors
    | elife-kitchen-sink.xml      | 10       
    | elife00013.xml              | 8       
