Feature: Get acknowledgements from the article
  In order to use the acknowledgements of this article
  as a script 
  I will parse the acknowledgements from the xml file
  
  Scenario Outline: Get the acknowledgements
    Given I have the document <document>
    When I get the acknowledgements
    Then I see the string <acknowledgements>
  
  Examples:
    | document                    | acknowledgements   
    | elife00013.xml              | AcknowledgementsWe thank Michael Fischbach, Richard Losick, and Russell Vance for critical reading of the manuscript. NK is a Fellow in the Integrated Microbial Biodiversity Program of the Canadian Institute for Advanced Research.
    
