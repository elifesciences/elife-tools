Feature: Parse the article publisher id
  In order to use the publisher_id of this article
  as a script 
  I will read the article-id publisher-id node

  Scenario Outline: Read the publisher id
    Given I have the document <document>
    When I get the publisher id
    Then I see the string <publisher_id>

  Examples:
    | document                          | publisher_id   
    | elife-kitchen-sink.xml            | 00013
    | elife00013.xml                    | 00013
    | elife_poa_e06828.xml              | 06828