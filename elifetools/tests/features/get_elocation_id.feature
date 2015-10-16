Feature: Get elocation-id from the article
  In order to use the elocation-id of this article
  as a script 
  I will parse the elocation-id from the xml file
  
  Scenario Outline: Get the elocation-id
    Given I have the document <document>
    When I get the elocation-id
    Then I see the string <elocation-id>
  
  Examples:
    | document                    | elocation-id
    | elife00013.xml              | e00013
    | elife_poa_e06828.xml        | e06828
