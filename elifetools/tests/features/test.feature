Feature: Test with lettuce
  In order to use testing service
  as a script 
  I will run a test
  And I will get a successful result

  Scenario: Uppercased strings
    Given I have the string lettuce leaves
    When I convert the string to upper case
    Then I see the string LETTUCE LEAVES