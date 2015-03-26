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

  Scenario Outline: Get authors
    Given I have the document <document>
    When I get the authors
    Then I see author index <index> <attribute> <subindex> as <val>
  
  Examples:
    | document                    | index | attribute          | subindex | val
    | elife-kitchen-sink.xml      | 0     | person_id          |          | 23
    | elife-kitchen-sink.xml      | 0     | surname            |          | Alegado
    | elife-kitchen-sink.xml      | 0     | given_names        |          | Rosanna A
    | elife-kitchen-sink.xml      | 0     | country            | 0        | United States
    | elife-kitchen-sink.xml      | 0     | institution        | 0        | University of California, Berkeley
    | elife-kitchen-sink.xml      | 0     | department         | 0        | Department of Molecular and Cell Biology
    | elife-kitchen-sink.xml      | 0     | city               | 0        | Berkeley
    | elife-kitchen-sink.xml      | 0     | city               | 1        | Boston
