Feature: Get author contributions from the document
  In order to use the author contributions of this article
  as a script 
  I will parse the author contributions from the xml file
  
  Scenario Outline: Count the number of author contributions
    Given I have the document <document>
    When I count the number of author contributions
    Then I count the total as <count>
  
  Examples:
    | document                    | count
    | elife-kitchen-sink.xml      | 9
    | elife00013.xml              | 8
    | elife00240.xml              | None


  Scenario Outline: Get author contributions
    Given I have the document <document>
    When I get the author contributions
    And I get the list item <list_item>
    Then I see the string <string>
  
  Examples:
    | document                    | list_item                    | string
    | elife-kitchen-sink.xml      | [0]['id']                    | con1
    | elife-kitchen-sink.xml      | [0]['fn-type']               | con
    | elife-kitchen-sink.xml      | [0]['text']                  | \n<p>RAA, Conception and design, Acquisition of data, Analysis and interpretation\n                        of data, Drafting or revising the article</p>\n
