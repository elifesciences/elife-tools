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
    Then I see list index <idx> <attribute> <sidx> as <val>
  
  Examples:
    | document                    | idx | attribute              | sidx | val
    | elife-kitchen-sink.xml      | 0   | person_id              |      | 23
    | elife-kitchen-sink.xml      | 0   | surname                |      | Alegado
    | elife-kitchen-sink.xml      | 0   | given_names            |      | Rosanna A
    | elife-kitchen-sink.xml      | 0   | country                | 0    | United States
    | elife-kitchen-sink.xml      | 0   | institution            | 0    | University of California, Berkeley
    | elife-kitchen-sink.xml      | 0   | department             | 0    | Department of Molecular and Cell Biology
    | elife-kitchen-sink.xml      | 0   | city                   | 0    | Berkeley
    | elife-kitchen-sink.xml      | 0   | country                | 1    | United States
    | elife-kitchen-sink.xml      | 0   | institution            | 1    | Harvard Medical School
    | elife-kitchen-sink.xml      | 0   | department             | 1    | Department of Biological Chemistry and Molecular Pharmacology
    | elife-kitchen-sink.xml      | 0   | city                   | 1    | Boston
    | elife-kitchen-sink.xml      | 0   | author                 |      | Rosanna A Alegado
    | elife-kitchen-sink.xml      | 0   | notes_correspondence   |      | None
    | elife-kitchen-sink.xml      | 0   | group_author_key       |      | None
    
    | elife-kitchen-sink.xml      | 1   | orcid                  |      | http://orcid.org/0000-0002-7361-560X
    | elife-kitchen-sink.xml      | 6   | notes_correspondence   |      | *For\n                        correspondence: jon_clardy@hms.harvard.edu (JC);
    | elife-kitchen-sink.xml      | 8   | institution            |      | Stanford University School of Medicine
    | elife-kitchen-sink.xml      | 9   | institution            |      | None
    
    | elife00013.xml              | 6   | notes_correspondence   |      | *For correspondence: jon_clardy@hms.harvard.edu (JC);
    | elife00013.xml              | 0   | notes_footnotes        | 0    | †These authors contributed equally to this work
    | elife00013.xml              | 0   | notes_footnotes        | 1    | RA: Conception and design, Acquisition of data, Analysis and interpretation of data, Drafting or revising the article
    | elife00013.xml              | 0   | notes_footnotes        | 2    | The remaining authors have no competing interests to declare.
    | elife00013.xml              | 0   | article_doi            |      | 10.7554/eLife.00013
    | elife00013.xml              | 0   | position               |      | 1
    | elife00013.xml              | 0   | equal_contrib          |      | True
    | elife00013.xml              | 1   | equal_contrib          |      | True
    | elife00013.xml              | 2   | equal_contrib          |      | None
    | elife00013.xml              | 0   | corresponding          |      | None
    | elife00013.xml              | 1   | corresponding          |      | None
    | elife00013.xml              | 6   | corresponding          |      | True
    | elife_poa_e06828.xml        | 0   | person_id              |      | 28783
    | elife_poa_e06828.xml        | 0   | surname                |      | Fleming
    | elife_poa_e06828.xml        | 0   | given_names            |      | Michael S
    | elife_poa_e06828.xml        | 0   | country                |      | United States
    | elife_poa_e06828.xml        | 0   | institution            |      | University of Pennsylvania
    | elife_poa_e06828.xml        | 0   | department             |      | Department of Neuroscience, Perelman School of Medicine
    | elife_poa_e06828.xml        | 0   | city                   |      | Philadelphia
    
    
    | elife02935.xml              | 0   | person_id              |      | 10471
    | elife02935.xml              | 0   | surname                |      | Ju
    | elife02935.xml              | 33  | person_id              |      | None
    | elife02935.xml              | 33  | surname                |      | None
    | elife02935.xml              | 33  | collab                 |      | ICGC Breast Cancer Group
    | elife02935.xml              | 33  | institution            |      | Wellcome Trust Sanger Institute
    | elife02935.xml              | 33  | department             |      | Cancer Genome Project
    | elife02935.xml              | 33  | position               |      | 34
    
    
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
    Then I see list index <idx> <attribute> <sidx> as <val>
  
  Examples:
    | document                    | idx | attribute              | sidx | val
    | elife-kitchen-sink.xml      | 0   | surname                |      | Mullikin
    | elife-kitchen-sink.xml      | 0   | given_names            |      | Jim
    | elife-kitchen-sink.xml      | 0   | position               |      | 1
    | elife-kitchen-sink.xml      | 0   | group_author_key       |      | group-author-id1

    | elife02935.xml              | 0   | surname                |      | Provenzano
    | elife02935.xml              | 0   | given_names            |      | Elena
    | elife02935.xml              | 0   | position               |      | 1
    | elife02935.xml              | 0   | group_author_key       |      | group-author-id1