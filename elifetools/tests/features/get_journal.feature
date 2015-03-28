Feature: Parse the journal from the article
  In order to use the journal data of this article
  as a script 
  I will read the journal data

  Scenario Outline: Read the journal id
    Given I have the document <document>
    When I get the journal id
    Then I see the string <journal_id>

  Examples:
    | document                          | journal_id   
    | elife00013.xml                    | elife
    | elife-kitchen-sink.xml            | eLife
    
    
  Scenario Outline: Read the journal issn
    Given I have the document <document>
    And I have the pub format <pub_format>
    When I get the issn of the journal
    Then I see the string <journal_issn>

  Examples:
    | document                          | pub_format  | journal_issn   
    | elife00013.xml                    | electronic  | 2050-084X
    
    
  Scenario Outline: Read the journal title
    Given I have the document <document>
    When I get the journal title
    Then I see the string <journal_title>

  Examples:
    | document                          | journal_title   
    | elife00013.xml                    | eLife
    
    
  Scenario Outline: Read the publisher name
    Given I have the document <document>
    When I get the publisher name
    Then I see the string <publisher_name>

  Examples:
    | document                          | publisher_name   
    | elife00013.xml                    | eLife Sciences Publications, Ltd
    