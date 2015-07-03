Feature: Get media tag data from the document
  In order to extract media from an article
  as a script 
  I will parse the media tag and details from the xml file

  Scenario Outline: Count the number of media
    Given I have the document <document>
    When I count the number of media
    Then I count the total as <count>

  Examples:
    | document                    | count
    | elife-kitchen-sink.xml      | 6
    | elife00013.xml              | 0
    | elife00007.xml              | 4
    | elife00240.xml              | 0
    | elife02935.xml              | 6
    | elife_poa_e06828.xml        | 0


