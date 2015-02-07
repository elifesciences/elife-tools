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
    | elife-sample-jun2012.xml          | 10.7554/eLife.000536
    | NLM3-sample-for-elife.1.xml       | 10.1083/jcb.201106079 
    | NLM3-sample-for-elife.2.xml       | 10.1083/jcb.201106010 
    | elife_pmc_preview_version_17.xml  | 10.7554/eLife.00013 