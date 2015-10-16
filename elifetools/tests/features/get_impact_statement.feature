Feature: Get impact statement from the document
  In order to parse an xml document 
  as a script 
  I will parse the impact_statement from the xml file

  Scenario Outline: Read the impact statement
    Given I have the document <document>
    When I get the impact statement
    Then I see the string <impact_statement>

  Examples:
    | document                            | impact_statement
    | elife-kitchen-sink.xml              | The chemical nature of RIF-1 may reveal a new class of bacterial signaling molecules.
    | elife00013.xml                      | The development of colonies of cells in choanoflagellates, water-dwelling organisms that feed on bacteria, is triggered by the presence of very low concentrations of a lipid molecule produced by certain types of bacteria.
    
