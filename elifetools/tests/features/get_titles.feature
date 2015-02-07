Feature: parse the title
  In order to parse an xml document 
  as a script 
  I will read the title node

  Scenario Outline: Read the title
    Given I have the document <document>
    When I get the title
    Then I see the string <title>

  Examples:
    | document                            | title
    | NLM3-sample-for-elife.1.xml         | CENP-C recruits M18BP1 to centromeres to promote CENP-A chromatin assembly
    | NLM3-sample-for-elife.2.xml         | Arf6 regulates AP-1B&#x02013;dependent sorting in polarized epithelial cells
    | elife-sample-jun2012.xml            | Prophylactic Platelets in Dengue: Survey Responses Highlight Lack of an Evidence Base
    | elife_pmc_preview_version_17.xml    | Bacterial regulation of colony development in the closest living relatives of animals