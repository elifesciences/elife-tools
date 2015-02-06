Feature: get references from the document
  In order to extract the references citied in an article
  as a script 
  I will parse the references from the xml file

  Scenario Outline: Count the number of references
    Given I have the document <document>
    When I count the number of references
    Then I get the total number of references as <references>

  Examples:
    | document                    | references
    | NLM3-sample-for-elife.1.xml | 57
    | NLM3-sample-for-elife.2.xml | 63
    | elife-sample-jun2012.xml    | 15
    | elife_pmc_preview_version_17.xml | 103

  Scenario Outline: Count the number of references from a particular year
    Given I have the document <document>
    When I count references from the year <year>
    Then I get the total number of references as <references>
    
  Examples:
    | document                    | year | references
    | NLM3-sample-for-elife.1.xml | 1979 | 1
    | NLM3-sample-for-elife.2.xml | 1999 | 5
    | elife-sample-jun2012.xml    | 2008 | 2
    
  Scenario Outline: Count the number of references from a particular journal
    Given I have the document <document>
    When I count the number of references from the journal <journal>
    Then I get the total number of references as <references>
    
  Examples:
    | document                    | journal           | references
    | NLM3-sample-for-elife.1.xml | Chromosome Res.   | 1
    | NLM3-sample-for-elife.2.xml | J. Cell Biol.     | 16
    | elife-sample-jun2012.xml    | Am J Trop Med Hyg | 2
    | elife-sample-jun2012.xml    | None              | 2

