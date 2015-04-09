Feature: Get components from the document
  In order to extract the components in an article
  as a script 
  I will parse the components from the xml file

  Scenario Outline: Count the number of components
    Given I have the document <document>
    When I count the number of components
    Then I count the total as <components>

  Examples:
    | document                    | components
    | elife-kitchen-sink.xml      | 44
    | elife00013.xml              | 30
    | elife_poa_e06828.xml        | 0

  Scenario Outline: Count the number of components by type
    Given I have the document <document>
    When I count components of the type <type>
    Then I count the total as <components>
    
  Examples:
    | document                    | type          | components
    | elife-kitchen-sink.xml      | abstract      | 2
    | elife-kitchen-sink.xml      | fig           | 25
    | elife-kitchen-sink.xml      | sub-article   | 2
    | elife00013.xml              | abstract      | 2
    | elife00013.xml              | fig           | 23
    | elife00013.xml              | sub-article   | 2


  Scenario Outline: Get the components
    Given I have the document <document>
    When I get the components
    And I get the list item <list_item>
    Then I see the string <string>

  Examples:
    | document                    | list_item                  | string
    | elife00013.xml              | [0]['type']                | abstract
    | elife00013.xml              | [0]['doi']                 | 10.7554/eLife.00013.001
    | elife00013.xml              | [0]['doi_url']             | http://dx.doi.org/10.7554/eLife.00013.001
    | elife00013.xml              | [0]['position']            | 1
    | elife00013.xml              | [0]['article_doi']         | 10.7554/eLife.00013
    | elife00013.xml              | [0]['content']             | Bacterially-produced small molecules exert profound influences on animal health, morphogenesis, and evolution through poorly understood mechanisms. In one of the closest living relatives of animals, the choanoflagellate Salpingoeca rosetta, we find that rosette colony development is induced by the prey bacterium Algoriphagus machipongonensis and its close relatives in the Bacteroidetes phylum. Here we show that a rosette inducing factor (RIF-1) produced by A. machipongonensis belongs to the small class of sulfonolipids, obscure relatives of the better known sphingolipids that play important roles in signal transmission in plants, animals, and fungi. RIF-1 has extraordinary potency (femtomolar, or 10−15 M) and S. rosetta can respond to it over a broad dynamic range—nine orders of magnitude. This study provides a prototypical example of bacterial sulfonolipids triggering eukaryotic morphogenesis and suggests molecular mechanisms through which bacteria may have contributed to the evolution of animals. DOI: http://dx.doi.org/10.7554/eLife.00013.001
    | elife00013.xml              | [1]['content']             | All animals, including humans, evolved in a world filled with bacteria. Although bacteria are most familiar as pathogens, some bacteria produce small molecules that are essential for the biology of animals and other eukaryotes, although the details of the ways in which these bacterial molecules are beneficial are not well understood. The choanoflagellates are water-dwelling organisms that use their whip-like flagella to move around, feeding on bacteria. They can exist as one cell or a colony of multiple cells and, perhaps surprisingly, are the closest known living relatives of animals. This means that experiments on these organisms have the potential to improve our understanding of animal development and the transition from egg to embryo to adult. Alegado et al. have explored how the morphology of Salpingoeca rosetta, a colony-forming choanoflagellate, is influenced by its interactions with various species of bacteria. In particular, they find that the development of multicellularity in S. rosetta is triggered by the presence of the bacterium Algoriphagus machipongonensis as well as its close relatives. They also identify the signaling molecule produced by the bacteria to be C32H64NO7S; this lipid molecule is an obscure relative of the sphingolipid molecules that have important roles in signal transmission in animals, plants, and fungi. Moreover, Alegado et al. show that S. rosetta can respond to this molecule – which they call rosette-inducing factor (RIF-1) – over a wide range of concentrations, including concentrations as low as 10−17 M. The work of Alegado et al. suggests that interactions between S. rosetta and Algoriphagus bacteria could be a productive model system for studying the influences of bacteria on animal cell biology, and for investigating the mechanisms of signal delivery and reception. Moreover, the molecular mechanisms revealed by this work leave open the possibility that bacteria might have contributed to the evolution of multicellularity in animals. DOI: http://dx.doi.org/10.7554/eLife.00013.002
    | elife00013.xml              | [2]['type']                | fig
    
    