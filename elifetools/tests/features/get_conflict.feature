Feature: Parse the conflict tags from the article
  In order to use the conflict of interest details of this article
  as a script 
  I will read the conflict footnotes

  Scenario Outline: Read the conflict footnotes
    Given I have the document <document>
    When I get the conflict
    Then I see list index <idx> as <conflict>

  Examples:
    | document                  | idx      | conflict   
    | elife00013.xml            | 0        | JC: Reviewing Editor, eLife.
    | elife00013.xml            | 1        | The remaining authors have no competing interests to declare.
    | elife_poa_e06828.xml      | 0        | The authors declare that no competing interests exist.