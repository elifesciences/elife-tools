Feature: parse the article pmid
  In order to use the pmid of this article
  as a script 
  I will read the pmid article-id node

  Scenario Outline: Read the pmid
    Given I have the document <document>
    When I get the pmid 
    Then I see the number <number>

  Examples:
    | document                         | number   
    | NLM3-sample-for-elife.1.xml      | 21911481 
    | NLM3-sample-for-elife.2.xml      | 21911479
    | elife_pmc_preview_version_17.xml | None