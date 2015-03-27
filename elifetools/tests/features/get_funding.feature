Feature: Get funding data from the article
  In order to use the funding data of this article
  as a script 
  I will parse the funding from the xml file
  
  Scenario Outline: Get the funding statement
    Given I have the document <document>
    When I get the funding statement
    Then I see the string <funding_statement>
  
  Examples:
    | document                    | funding_statement   
    | elife00013.xml              | The funders had no role in study design, data collection and interpretation, or the decision to submit the work for publication.
    
    # TODO - Parse the funding and awards list