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
    | elife_poa_e06828.xml              | This article is distributed under the terms of the Creative Commons Attribution License permitting unrestricted use and redistribution provided that the original author and source are credited.
    
  Scenario Outline: Read the license URL
    Given I have the document <document>
    When I get the URL of the license
    Then I see the string <license_url>

  Examples:
    | document                          | license_url   
    | elife00013.xml                    | http://creativecommons.org/licenses/by/3.0/
    | elife_poa_e06828.xml              | http://creativecommons.org/licenses/by/4.0/

  Scenario Outline: Read the full license
    Given I have the document <document>
    When I get the full license
    Then I see the string <string>

  Examples:
    | document                          | string
    | elife-kitchen-sink.xml            | This article is distributed under the terms of the <ext-link ext-link-type="uri" xlink:href="http://creativecommons.org/licenses/by/4.0/">Creative\n                            Commons Attribution License</ext-link>, which permits unrestricted use\n                        and redistribution provided that the original author and source are\n                        credited.
    | elife00013.xml                    | This article is distributed under the terms of the <ext-link ext-link-type="uri" xlink:href="http://creativecommons.org/licenses/by/3.0/">Creative Commons Attribution License</ext-link>, which permits unrestricted use and redistribution provided that the original author and source are credited.
    | elife_poa_e06828.xml              | This article is distributed under the terms of the <ext-link ext-link-type="uri" xlink:href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution License</ext-link> permitting unrestricted use and redistribution provided that the original author and source are credited.