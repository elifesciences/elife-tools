Feature: Parse the copyright from the article
  In order to use the journal data of this article
  as a script 
  I will read the copyright data

  Scenario Outline: Read the copyright statement
    Given I have the document <document>
    When I get the copyright statement
    Then I see the string <copyright_statement>

  Examples:
    | document                          | copyright_statement   
    | elife00013.xml                    | © 2012, Alegado et al
   
   
  Scenario Outline: Read the copyright year
    Given I have the document <document>
    When I get the copyright year
    Then I see the string <copyright_year>

  Examples:
    | document                          | copyright_year
    | elife00013.xml                    | 2012
    
    
   Scenario Outline: Read the copyright holder
    Given I have the document <document>
    When I get the copyright holder
    Then I see the string <copyright_holder>

  Examples:
    | document                          | copyright_holder
    | elife00013.xml                    | Alegado et al
   
        
