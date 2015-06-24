Feature: Get competing interests from the document
  In order to use the author contributions of this article
  as a script 
  I will parse the competing interests from the xml file
  
  Scenario Outline: Count the number of competing interests
    Given I have the document <document>
    When I count the number of competing interests
    Then I count the total as <count>
  
  Examples:
    | document                    | count
    | elife-kitchen-sink.xml      | 2
    | elife00013.xml              | 2
    | elife00240.xml              | 1
    | elife_poa_e06828.xml        | 1
    | elife00190.xml              | None
    
  Scenario Outline: Get competing interests
    Given I have the document <document>
    When I get the competing interests
    And I get the list item <list_item>
    Then I see the string <string>
  
  Examples:
    | document                    | list_item                    | string
    | elife-kitchen-sink.xml      | [0]['id']                    | conf1
    | elife-kitchen-sink.xml      | [0]['fn-type']               | conflict
    | elife-kitchen-sink.xml      | [0]['text']                  | \n<p>JC: Reviewing editor, <italic>eLife</italic>.</p>\n
