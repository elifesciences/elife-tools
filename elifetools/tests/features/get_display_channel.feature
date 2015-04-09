Feature: Get display channels from the document
  In order to use the display channel of this article
  as a script 
  I will parse the display channel from the xml file
  
  Scenario Outline: Count the number of display channels
    Given I have the document <document>
    When I count the number of display channel
    Then I count the total as <count>
  
  Examples:
    | document                    | count
    | elife-kitchen-sink.xml      | 1     
    | elife00013.xml              | 1       
    | elife_poa_e06828.xml        | 1
    

  Scenario Outline: Get display channel
    Given I have the document <document>
    When I get the display channel
    Then I see list index <idx> as <val>
  
  Examples:
    | document                    | idx | val
    | elife-kitchen-sink.xml      | 0   | Research article
    | elife00013.xml              | 0   | Research article
    | elife_poa_e06828.xml        | 0   | Research article
    