Feature: Parse the correspondence tag from the article
  In order to use the correspondence details of this article
  as a script 
  I will read the correspondence note

  Scenario Outline: Read the correspondence note
    Given I have the document <document>
    When I get the correspondence
    Then I see list index <idx> as <correspondence>

  Examples:
    | document                  | idx      | correspondence   
    | elife00013.xml            | 0        | *For correspondence: jon_clardy@hms.harvard.edu (JC);
    | elife00013.xml            | 1        | *For correspondence: nking@berkeley.edu (NK)
    