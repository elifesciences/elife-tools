Feature: Parse the correspondence tag from the article
  In order to use the correspondence details of this article
  as a script 
  I will read the correspondence note

  Scenario Outline: Read the correspondence note
    Given I have the document <document>
    When I get the correspondence
    And I get the list item <list_item>
    Then I see the string <string>

  Examples:
    | document                  | list_item  | string   
    | elife00013.xml            | [0]        | *For correspondence: jon_clardy@hms.harvard.edu (JC);
    | elife00013.xml            | [1]        | *For correspondence: nking@berkeley.edu (NK)
    | elife-kitchen-sink.xml    | [0]        | \n*For\n                        correspondence: jon_clardy@hms.harvard.edu (JC);
    | elife_poa_e06828.xml      | [0]        | None
    
  Scenario Outline: Read the full correspondence note
    Given I have the document <document>
    When I get the full correspondence
    And I get the list item <list_item>
    Then I see the string <string>

  Examples:
    | document                  | list_item                 | string
    | elife00013.xml            | ['cor1']                  | jon_clardy@hms.harvard.edu
    | elife-kitchen-sink.xml    | ['cor1']                  | jon_clardy@hms.harvard.edu
    | elife_poa_e06828.xml      | ['cor1']                  | None
    
    
