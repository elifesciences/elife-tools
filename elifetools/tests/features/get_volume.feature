Feature: Get volume from the article
  In order to use the volume of this article
  as a script 
  I will parse the volume from the xml file
  
  Scenario Outline: Get the volume
    Given I have the document <document>
    When I get the volume
    Then I see the string <volume>
  
  Examples:
    | document                    | volume   
    | elife00013.xml              | 1
    | elife_poa_e06828.xml        | None
