Feature: Parse the article type from the article
  In order to use the article type of this article
  as a script 
  I will read the article type

  Scenario Outline: Read the article type
    Given I have the document <document>
    When I get the article type
    Then I see the string <article_type>

  Examples:
    | document                          | article_type   
    | elife00013.xml                    | research-article
    | elife_poa_e06828.xml              | research-article