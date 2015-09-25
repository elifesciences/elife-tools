Feature: get authors from the document
  In order to put my author names in my api
  as a script 
  I will parse the authors from the xml file
  
  Scenario Outline: Count the number of authors
    Given I have the document <document>
    When I count the number of authors 
    Then I count the total as <authors>
  
  Examples:
    | document                    | authors
    | elife-kitchen-sink.xml      | 10       
    | elife00013.xml              | 8       
    | elife_poa_e06828.xml        | 7
    | elife02935.xml              | 53

  Scenario Outline: Get authors
    Given I have the document <document>
    When I get the authors
    And I get the list item <list_item>
    Then I see the string <string>
    

  Examples:
    | document                    | list_item                            | string
    | elife-kitchen-sink.xml      | [0]['person_id']                     | 23
    | elife-kitchen-sink.xml      | [0]['surname']                       | Alegado
    | elife-kitchen-sink.xml      | [0]['given-names']                   | Rosanna A
    | elife-kitchen-sink.xml      | [0]['suffix']                        | Jnr
    | elife-kitchen-sink.xml      | [0]['affiliations'][0]['country']     | United States
    | elife-kitchen-sink.xml      | [0]['affiliations'][0]['institution'] | University of California, Berkeley
    | elife-kitchen-sink.xml      | [0]['affiliations'][0]['dept']        | Department of Molecular and Cell Biology
    | elife-kitchen-sink.xml      | [0]['affiliations'][0]['city']        | Berkeley
    | elife-kitchen-sink.xml      | [0]['affiliations'][1]['country']     | United States
    | elife-kitchen-sink.xml      | [0]['affiliations'][1]['institution'] | Harvard Medical School
    | elife-kitchen-sink.xml      | [0]['affiliations'][1]['dept']        | Department of Biological Chemistry and Molecular Pharmacology
    | elife-kitchen-sink.xml      | [0]['affiliations'][1]['city']        | Boston
    | elife-kitchen-sink.xml      | [0]['author']                        | Rosanna A Alegado
    | elife-kitchen-sink.xml      | [0]['notes-corresp'][0]              | None
    | elife-kitchen-sink.xml      | [0]['group-author-key']              | None
    | elife-kitchen-sink.xml      | [0]['type']                          | author
    | elife-kitchen-sink.xml      | [4]['references']['foot-note'][0]    | fn1
    
    
    | elife-kitchen-sink.xml      | [1]['orcid']                         | http://orcid.org/0000-0002-7361-560X
    | elife-kitchen-sink.xml      | [6]['notes-corresp'][0]              | \n*For\n                        correspondence: jon_clardy@hms.harvard.edu(JC);
    | elife-kitchen-sink.xml      | [8]['affiliations'][0]['institution'] | Stanford University School of Medicine
    | elife-kitchen-sink.xml      | [9]['affiliations'][0]['institution'] | None
    
    | elife00013.xml              | [6]['notes-corresp'][0]              | *For correspondence: jon_clardy@hms.harvard.edu (JC);
    | elife00013.xml              | [0]['notes-fn'][0]                   | †These authors contributed equally to this work
    | elife00013.xml              | [0]['notes-fn'][1]                   | RA: Conception and design, Acquisition of data, Analysis and interpretation of data, Drafting or revising the article
    | elife00013.xml              | [0]['notes-fn'][2]                   | The remaining authors have no competing interests to declare.
    | elife00013.xml              | [0]['article_doi']                   | 10.7554/eLife.00013
    
    | elife00013.xml              | [0]['position']                      | 1
    | elife00013.xml              | [0]['equal-contrib']                 | yes
    | elife00013.xml              | [1]['equal-contrib']                 | yes
    | elife00013.xml              | [2]['equal-contrib']                 | None
    | elife00013.xml              | [0]['corresp']                       | None
    | elife00013.xml              | [1]['corresp']                       | None
    | elife00013.xml              | [6]['corresp']                       | yes
    | elife_poa_e06828.xml        | [0]['person_id']                     | 28783
    | elife_poa_e06828.xml        | [0]['surname']                       | Fleming
    | elife_poa_e06828.xml        | [0]['given-names']                   | Michael S
    | elife_poa_e06828.xml        | [0]['affiliations'][0]['country']     | United States
    | elife_poa_e06828.xml        | [0]['affiliations'][0]['institution'] | University of Pennsylvania
    | elife_poa_e06828.xml        | [0]['affiliations'][0]['dept']        | Department of Neuroscience, Perelman School of Medicine
    | elife_poa_e06828.xml        | [0]['affiliations'][0]['city']        | Philadelphia
    
    | elife02935.xml              | [0]['person_id']                     | 10471
    | elife02935.xml              | [0]['surname']                       | Ju
    | elife02935.xml              | [33]['person_id']                    | None
    | elife02935.xml              | [33]['surname']                      | None
    | elife02935.xml              | [33]['collab']                       | ICGC Breast Cancer Group
    | elife02935.xml              | [33]['affiliations'][0]['institution']| Wellcome Trust Sanger Institute
    | elife02935.xml              | [33]['affiliations'][0]['dept']       | Cancer Genome Project
    | elife02935.xml              | [33]['position']                     | 34
    
    
  Scenario Outline: Count the number of non-byline authors
    Given I have the document <document>
    When I count the number of non-byline authors 
    Then I count the total as <authors>
  
  Examples:
    | document                    | authors
    | elife-kitchen-sink.xml      | 7   
    | elife00013.xml              | 0       
    | elife_poa_e06828.xml        | 0
    | elife02935.xml              | 127
    
    
  Scenario Outline: Get non-byline authors
    Given I have the document <document>
    When I get the non-byline authors
    And I get the list item <list_item>
    Then I see the string <string>
  
  Examples:
    | document                    | list_item                     | string
    | elife-kitchen-sink.xml      | [0]['surname']                | Mullikin
    | elife-kitchen-sink.xml      | [0]['given-names']            | Jim
    | elife-kitchen-sink.xml      | [0]['position']               | 1
    | elife-kitchen-sink.xml      | [0]['group-author-key']       | group-author-id1
    | elife-kitchen-sink.xml      | [0]['type']                   | author non-byline

    | elife02935.xml              | [0]['surname']                | Provenzano
    | elife02935.xml              | [0]['given-names']            | Elena
    | elife02935.xml              | [0]['position']               | 1
    | elife02935.xml              | [0]['group-author-key']       | group-author-id1
    | elife02935.xml              | [0]['type']                   | author non-byline
    
    
  Scenario Outline: Count the number of contributors
    Given I have the document <document>
    When I count the number of contributors
    Then I count the total as <contributors>
  
  Examples:
    | document                    | contributors
    | elife-kitchen-sink.xml      | 19 
    | elife00013.xml              | 9  
    | elife_poa_e06828.xml        | 8
    | elife02935.xml              | 181
    
    
  Scenario Outline: Get contributors
    Given I have the document <document>
    When I get the contributors
    And I get the list item <list_item>
    Then I see the string <string>
    

  Examples:
    | document                    | list_item                                    | string
    | elife-kitchen-sink.xml      | [0]['id']                                    | author-23
    | elife-kitchen-sink.xml      | [0]['type']                                  | author
    | elife-kitchen-sink.xml      | [0]['surname']                               | Alegado
    | elife-kitchen-sink.xml      | [0]['given-names']                           | Rosanna A
    | elife-kitchen-sink.xml      | [0]['suffix']                                | Jnr
    | elife-kitchen-sink.xml      | [0]['references']['present-address'][0]      | pa1
    | elife-kitchen-sink.xml      | [0]['references']['competing-interest'][0]   | conf2
    | elife-kitchen-sink.xml      | [0]['references']['funding'][0]              | par-1
    | elife-kitchen-sink.xml      | [0]['references']['funding'][1]              | par-2
    | elife-kitchen-sink.xml      | [0]['references']['related-object'][0]       | dataro1
    | elife-kitchen-sink.xml      | [0]['references']['related-object'][1]       | dataro2
    | elife-kitchen-sink.xml      | [0]['references']['affiliation'][0]          | aff1
    | elife-kitchen-sink.xml      | [0]['references']['affiliation'][1]          | aff2
    | elife-kitchen-sink.xml      | [0]['references']['equal-contrib'][0]        | equal-contrib
    | elife-kitchen-sink.xml      | [0]['references']['contribution'][0]         | con1
    | elife-kitchen-sink.xml      | [0]['equal-contrib']                         | yes
    
    | elife-kitchen-sink.xml      | [8]['type']                                  | on-behalf-of
    | elife-kitchen-sink.xml      | [8]['on-behalf-of']                          | for the HIV Genome-to-Genome Study and the Swiss HIV Cohort Study
    
    | elife-kitchen-sink.xml      | [9]['type']                                  | author
    | elife-kitchen-sink.xml      | [9]['corresp']                               | yes
    | elife-kitchen-sink.xml      | [9]['group-author-key']                      | group-author-id1
    | elife-kitchen-sink.xml      | [9]['references']['affiliation'][0]          | aff3
    | elife-kitchen-sink.xml      | [9]['references']['contribution'][0]         | con9
    | elife-kitchen-sink.xml      | [9]['references']['competing-interest'][0]   | conf2
    | elife-kitchen-sink.xml      | [9]['references']['funding'][0]              | par-7
    | elife-kitchen-sink.xml      | [9]['references']['email'][0]                | cor3
    | elife-kitchen-sink.xml      | [9]['collab']                                | NISC Comparative Sequencing Program

