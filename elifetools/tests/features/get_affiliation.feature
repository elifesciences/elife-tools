Feature: Get affiliations from the article
  In order to use the affiliations of this article
  as a script 
  I will parse the aff tags from the xml file
  
  Scenario Outline: Get the full affiliation
    Given I have the document <document>
    When I get the full affiliation
    And I get the list item <list_item>
    Then I see the string <string>
  
  Examples:
    | document                    | list_item                | string
    | elife_poa_e06828.xml        | ['aff1']                 | None
    | elife00013.xml              | ['aff1']['dept']         | Department of Molecular and Cell Biology
    | elife00013.xml              | ['aff1']['country']      | United States
    | elife00013.xml              | ['aff1']['institution']  | University of California, Berkeley
    | elife00013.xml              | ['aff1']['city']         | Berkeley
    | elife00013.xml              | ['aff2']['dept']         | Department of Biological Chemistry and Molecular Pharmacology
    | elife00013.xml              | ['aff3']['dept']         | Department of Biochemistry
    | elife09853.xml              | ['aff1']['email']        | labecker@stanford.edu
    