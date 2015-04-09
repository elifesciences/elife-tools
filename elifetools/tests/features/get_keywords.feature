Feature: Get keywords from the document
  In order to use the keywords of this article
  as a script 
  I will parse the keywords from the xml file
  
  Scenario Outline: Count the number of keywords
    Given I have the document <document>
    When I count the number of keywords
    Then I count the total as <count>
  
  Examples:
    | document                    | count
    | elife-kitchen-sink.xml      | 4     
    | elife00013.xml              | 4       
    | elife_poa_e06828.xml        | 4   

  Scenario Outline: Get keywords
    Given I have the document <document>
    When I get the keywords
    Then I see list index <idx> as <val>
  
  Examples:
    | document                    | idx | val
    | elife-kitchen-sink.xml      | 0   | Salpingoeca rosetta
    | elife-kitchen-sink.xml      | 1   | Algoriphagus
    | elife-kitchen-sink.xml      | 2   | bacterial sulfonolipid
    | elife-kitchen-sink.xml      | 3   | multicellular development
    | elife00013.xml              | 0   | Salpingoeca rosetta
    | elife00013.xml              | 1   | Algoriphagus
    | elife00013.xml              | 2   | bacterial sulfonolipid
    | elife00013.xml              | 3   | multicellular development
    | elife_poa_e06828.xml        | 0   | neurotrophins
    | elife_poa_e06828.xml        | 1   | RET signaling
    | elife_poa_e06828.xml        | 2   | DRG neuron development
    | elife_poa_e06828.xml        | 3   | cis and trans activation

