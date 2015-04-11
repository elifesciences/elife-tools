Feature: Parse the collection data from the article
  In order to use the date of this collection article publication
  as a script 
  I will read the collection data

  Scenario Outline: Read the collection year
    Given I have the document <document>
    When I get the collection year
    Then I see the string <year>

  Examples:
    | document                  | year
    | elife-kitchen-sink.xml    | 2014
    | elife00013.xml            | 2012
    | elife_poa_e06828.xml      | None


  Scenario Outline: Determine if article is POA or not
    Given I have the document <document>
    When I get the is poa
    Then I see the string <is_poa>

  Examples:
    | document                  | is_poa
    | elife-kitchen-sink.xml    | False
    | elife00013.xml            | False
    | elife_poa_e06828.xml      | True
