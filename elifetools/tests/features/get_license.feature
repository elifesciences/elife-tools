Feature: Parse the article license
  In order to use the license of this article
  as a script 
  I will read the license data

  Scenario Outline: Read the license
    Given I have the document <document>
    When I get the license
    Then I see the string <license>

  Examples:
    | document                          | license   
    | elife00013.xml                    | This article is distributed under the terms of the Creative Commons Attribution License, which permits unrestricted use and redistribution provided that the original author and source are credited.
    
  Scenario Outline: Read the license URL
    Given I have the document <document>
    When I get the URL of the license
    Then I see the string <license_url>

  Examples:
    | document                          | license_url   
    | elife00013.xml                    | http://creativecommons.org/licenses/by/3.0/
    
