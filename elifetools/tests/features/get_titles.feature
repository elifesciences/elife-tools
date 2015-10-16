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
    | elife-kitchen-sink.xml              | Bacterial regulation of colony development in the closest living\n                    relatives of animals
    | elife00013.xml                      | A bacterial sulfonolipid triggers multicellular development in the closest living relatives of animals
    | elife_poa_e06828.xml                | Cis and trans RET signaling control the survival and central projection growth of rapidly adapting mechanoreceptors
    

  Scenario Outline: Read the full title
    Given I have the document <document>
    When I get the full title
    Then I see the string <title>

  Examples:
    | document                            | title
    | elife-kitchen-sink.xml              | Bacterial regulation of colony development in the closest living\n                    relatives of animals
    | elife00013.xml                      | A bacterial sulfonolipid triggers multicellular development in the closest living relatives of animals
    | elife_poa_e06828.xml                | <italic>Cis</italic> and <italic>trans</italic> RET signaling control the survival and central projection growth of rapidly adapting mechanoreceptors
    
  Scenario Outline: Read the short title
    Given I have the document <document>
    When I get the short title
    Then I see the string <title>

  Examples:
    | document                            | title
    | elife-kitchen-sink.xml              | Bacterial regulation
    | elife00013.xml                      | A bacterial sulfonol
    | elife_poa_e06828.xml                | Cis and trans RET si
    
    
  Scenario Outline: Read the slug title
    Given I have the document <document>
    When I get the slug title
    Then I see the string <title>
    
  Examples:
    | document                            | title
    | elife-kitchen-sink.xml              | bacterial-regulation-of-colony-development-in-the-closest-living-relatives-of-animals
    | elife00013.xml                      | a-bacterial-sulfonolipid-triggers-multicellular-development-in-the-closest-living-relatives-of-animals
    | elife_poa_e06828.xml                | cis-and-trans-ret-signaling-control-the-survival-and-central-projection-growth-of-rapidly-adapting-mechanoreceptors