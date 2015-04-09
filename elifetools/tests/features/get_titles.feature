Feature: parse the title
  In order to parse an xml document 
  as a script 
  I will read the title node

  Scenario Outline: Read the title
    Given I have the document <document>
    When I get the title
    Then I see the string <title>

  Examples:
    | document                            | title
    | elife-kitchen-sink.xml              | "Bacterial regulation of colony development in the closest living\n                    relatives of animals"
    | elife00013.xml                      | A bacterial sulfonolipid triggers multicellular development in the closest living relatives of animals
    | elife_poa_e06828.xml                | Cis and trans RET signaling control the survival and central projection growth of rapidly adapting mechanoreceptors