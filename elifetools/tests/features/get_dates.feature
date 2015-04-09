Feature: Parse the dates from the article
  In order to use the dates of this article publication
  as a script 
  I will read the pub date and history dates

  Scenario Outline: Read the pub date
    Given I have the document <document>
    When I get the pub date date
    Then I see the string <pub_date>

  Examples:
    | document                  | pub_date   
    | elife00013.xml            | October 15, 2012
    | elife_poa_e06828.xml      | None

  Scenario Outline: Read the pub date day
    Given I have the document <document>
    When I get the pub date day
    Then I see the string <pub_day>

  Examples:
    | document                  | pub_day 
    | elife00013.xml            | 15
    | elife_poa_e06828.xml      | None

  Scenario Outline: Read the pub date month
    Given I have the document <document>
    When I get the pub date month
    Then I see the string <pub_month>

  Examples:
    | document                  | pub_month 
    | elife00013.xml            | 10
    | elife_poa_e06828.xml      | None
    
  Scenario Outline: Read the pub date year
    Given I have the document <document>
    When I get the pub date year
    Then I see the string <pub_year>

  Examples:
    | document                  | pub_year 
    | elife00013.xml            | 2012
    | elife_poa_e06828.xml      | None
    
  Scenario Outline: Read the pub date timestamp
    Given I have the document <document>
    When I get the pub date timestamp
    Then I see the string <timestamp>

  Examples:
    | document                  | timestamp 
    | elife00013.xml            | 1350259200
    | elife_poa_e06828.xml      | None
    
    
    
    
  Scenario Outline: Read the received date
    Given I have the document <document>
    When I get the received date date
    Then I see the string <received_date>

  Examples:
    | document                  | received_date
    | elife00013.xml            | May 22, 2012
    | elife_poa_e06828.xml      | February 03, 2015

  Scenario Outline: Read the received date day
    Given I have the document <document>
    When I get the received date day
    Then I see the string <received_day>

  Examples:
    | document                  | received_day 
    | elife00013.xml            | 22
    | elife_poa_e06828.xml      | 3

  Scenario Outline: Read the received date month
    Given I have the document <document>
    When I get the received date month
    Then I see the string <received_month>

  Examples:
    | document                  | received_month 
    | elife00013.xml            | 5
    | elife_poa_e06828.xml      | 2
    
  Scenario Outline: Read the received date year
    Given I have the document <document>
    When I get the received date year
    Then I see the string <received_year>

  Examples:
    | document                  | received_year 
    | elife00013.xml            | 2012
    | elife_poa_e06828.xml      | 2015
    
  Scenario Outline: Read the received date timestamp
    Given I have the document <document>
    When I get the received date timestamp
    Then I see the string <timestamp>

  Examples:
    | document                  | timestamp 
    | elife00013.xml            | 1337644800
    | elife_poa_e06828.xml      | 1422921600
    
    
    
    
    
    
  Scenario Outline: Read the accepted date
    Given I have the document <document>
    When I get the accepted date date
    Then I see the string <accepted_date>

  Examples:
    | document                  | accepted_date
    | elife00013.xml            | July 18, 2012
    | elife_poa_e06828.xml      | April 01, 2015

  Scenario Outline: Read the accepted date day
    Given I have the document <document>
    When I get the accepted date day
    Then I see the string <accepted_day>

  Examples:
    | document                  | accepted_day 
    | elife00013.xml            | 18
    | elife_poa_e06828.xml      | 1

  Scenario Outline: Read the accepted date month
    Given I have the document <document>
    When I get the accepted date month
    Then I see the string <accepted_month>

  Examples:
    | document                  | accepted_month 
    | elife00013.xml            | 7
    | elife_poa_e06828.xml      | 4
    
  Scenario Outline: Read the received date year
    Given I have the document <document>
    When I get the accepted date year
    Then I see the string <accepted_year>

  Examples:
    | document                  | accepted_year 
    | elife00013.xml            | 2012
    | elife_poa_e06828.xml      | 2015
    
  Scenario Outline: Read the accepted date timestamp
    Given I have the document <document>
    When I get the accepted date timestamp
    Then I see the string <timestamp>

  Examples:
    | document                  | timestamp 
    | elife00013.xml            | 1342569600
    | elife_poa_e06828.xml      | 1427846400
    

    
    