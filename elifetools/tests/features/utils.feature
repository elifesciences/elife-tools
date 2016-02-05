Feature: Get utils function responses from unusual input
  In order to use the utils of this module
  as a script 
  I will send data to individual functions for better test coverage
  
  Scenario Outline: Get the first item in a list
    Given I have the list json <json_string>
    When I get the first item
    Then I see the string <string>
  
  Examples:
    | json_string             | string
    | None                    | None     
    | []                      | None      
    | ["bees"]                | bees
    | ["bees","knees"]        | bees
    

  Scenario Outline: Strip punctuation and whitespace from a string
    Given I have the string <string_input>
    When I strip punctuation and space from the string
    Then I see the string <string>
  
  Examples:
    | string_input            | string
    | None                    | None     
    | An : ( example ) .      | An: (example).


  Scenario Outline: Strip punctuation and whitespace from a list
    Given I have the list json <json_string>
    When I strip punctuation and space from the list
    And I get the list item <list_item>
    Then I see the string <string>
  
  Examples:
    | json_string                   | list_item  | string
    | ["bees .","( knees )"]        | [0]        | bees.   
    | ["bees .","( knees )"]        | [1]        | (knees)


  Scenario Outline: Coerce a string to an int
    Given I have the string <string_input>
    And I have the default <default>
    When I coerce the string to an int
    Then I see the string <string>
  
  Examples:
    | string_input                  | default       | string
    | 1                             | 0xDEADBEEF    | 1
    | 1                             | moo           | 1
    | two                           | 0xDEADBEEF    | two
    | two                           | moo           | moo
    
    
  Scenario Outline: Covert numeric dates values to a date struct
    Given I have the date parts <year>, <month>, <day>, <tz>
    And I have the date format <date_format>
    When I get the date struct
    Then I see the date struct from date string <date_string>
  
  Examples:
    | year   | month   | day   | tz       | date_format     | date_string
    | 2015   | 06      | 22    | UTC      | %Y-%m-%d %Z     | 2015-06-22 UTC
    | 2015   | 02      | 31    | UTC      | %Y-%m-%d %Z     | None
    | 2015   | 06      | 0     | UTC      | %Y-%m-%d %Z     | None
    | None   | 06      | 22    | UTC      | %Y-%m-%d %Z     | None
    
  Scenario Outline: Send sibling ordinal function bad input
    Given I have the mock tag
    When I get the sibling ordinal <function>
    Then I see the string <string>
  
  Examples:
    | function                                   | string   
    | tag_media_sibling_ordinal                  | None     
    | tag_supplementary_material_sibling_ordinal | None    
