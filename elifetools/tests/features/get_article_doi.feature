Feature: parse the article DOI
  In order to use the DOI of this article
  as a script 
  I will read the DOI article-id node

  Scenario Outline: Read the DOI
    Given I have the document <document>
    When I get the doi
    Then I see the identifier <identifier>

  Examples:
    | document                          | identifier   
    | elife-kitchen-sink.xml            | 10.7554/eLife.00013
    | elife00013.xml                    | 10.7554/eLife.00013
    | elife_poa_e06828.xml              | 10.7554/eLife.06828