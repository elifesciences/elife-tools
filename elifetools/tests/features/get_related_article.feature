Feature: Get related articles from the document
  In order to use the related articles of this article
  as a script 
  I will parse the related article from the xml file
  
  Scenario Outline: Count the number of related articles
    Given I have the document <document>
    When I count the number of related articles
    Then I count the total as <count>
  
  Examples:
    | document                    | count
    | elife-kitchen-sink.xml      | 1    
    | elife00013.xml              | 1      


  Scenario Outline: Get related articles
    Given I have the document <document>
    When I get the related articles
    And I get the list item <list_item>
    Then I see the string <string>
  
  Examples:
    | document                    | list_item                     | string
    | elife-kitchen-sink.xml      | [0]['ext_link_type']          | doi
    | elife-kitchen-sink.xml      | [0]['related_article_type']   | commentary
    | elife-kitchen-sink.xml      | [0]['xlink_href']             | 10.7554/eLife.00013
    | elife00013.xml              | [0]['ext_link_type']          | doi
    | elife00013.xml              | [0]['related_article_type']   | commentary
    | elife00013.xml              | [0]['xlink_href']             | 10.7554/eLife.00242

