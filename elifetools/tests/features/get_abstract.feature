Feature: Get abstract from the article
  In order to use the abstract text of this article
  as a script 
  I will parse the abstract from the xml file
  
  Scenario Outline: Get the abstract in text format
    Given I have the document <document>
    When I get the abstract
    Then I see the string <abstract>
  
  Examples:
    | document                    | abstract   
    | elife00013.xml              | Bacterially-produced small molecules exert profound influences on animal health, morphogenesis, and evolution through poorly understood mechanisms. In one of the closest living relatives of animals, the choanoflagellate Salpingoeca rosetta, we find that rosette colony development is induced by the prey bacterium Algoriphagus machipongonensis and its close relatives in the Bacteroidetes phylum. Here we show that a rosette inducing factor (RIF-1) produced by A. machipongonensis belongs to the small class of sulfonolipids, obscure relatives of the better known sphingolipids that play important roles in signal transmission in plants, animals, and fungi. RIF-1 has extraordinary potency (femtomolar, or 10−15 M) and S. rosetta can respond to it over a broad dynamic range—nine orders of magnitude. This study provides a prototypical example of bacterial sulfonolipids triggering eukaryotic morphogenesis and suggests molecular mechanisms through which bacteria may have contributed to the evolution of animals.
