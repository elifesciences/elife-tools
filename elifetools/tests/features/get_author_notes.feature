Feature: Get author notes from the document
  In order to use the author notes of this article
  as a script 
  I will parse the author notes from the xml file
  
  Scenario Outline: Count the number of author notes
    Given I have the document <document>
    When I count the number of author notes
    Then I count the total as <count>
  
  Examples:
    | document                    | count
    | elife-kitchen-sink.xml      | 3    
    | elife00013.xml              | 1      
    | elife00240.xml              | None 

  Scenario Outline: Get author notes
    Given I have the document <document>
    When I get the author notes
    And I get the list item <list_item>
    Then I see the string <string>
  
  Examples:
    | document                    | list_item | string
    | elife-kitchen-sink.xml      | [0]       | \n†\nThese authors contributed equally to this work\n
    | elife-kitchen-sink.xml      | [1]       | \n‡\nThese authors also contributed equally to this work\n
    | elife-kitchen-sink.xml      | [2]       | \n**\nDeceased\n
    | elife00013.xml              | [0]       | †These authors contributed equally to this work

  Scenario Outline: Count the number of full author notes
    Given I have the document <document>
    When I count the number of full author notes
    Then I count the total as <count>

  Examples:
    | document                    | count
    | elife-kitchen-sink.xml      | 6
    | elife00013.xml              | 1
    | elife00240.xml              | None 

  Scenario Outline: Get full author notes
    Given I have the document <document>
    When I get the full author notes
    And I get the list item <list_item>
    Then I see the string <string>

  Examples:
    | document                    | list_item                    | string
    | elife-kitchen-sink.xml      | [0]['id']                    | equal-contrib
    | elife-kitchen-sink.xml      | [0]['fn-type']               | con
    | elife-kitchen-sink.xml      | [0]['text']                  | \n<label>†</label>\n<p>These authors contributed equally to this work</p>\n
    | elife-kitchen-sink.xml      | [2]['id']                    | pa1
    | elife-kitchen-sink.xml      | [2]['fn-type']               | present-address
    | elife-kitchen-sink.xml      | [2]['text']                  | \n<label>¶</label>\n<p>Department of Wellcome Trust, Sanger Institute, London, United Kingdom</p>\n
    | elife-kitchen-sink.xml      | [5]['id']                    | fn1
    | elife-kitchen-sink.xml      | [5]['fn-type']               | deceased
    | elife-kitchen-sink.xml      | [5]['text']                  | \n<label>**</label>\n<p>Deceased</p>\n
    | elife00013.xml              | [0]['id']                    | equal-contrib
    | elife00013.xml              | [0]['fn-type']               | con
    | elife00013.xml              | [0]['text']                  | <label>†</label><p>These authors contributed equally to this work</p>
