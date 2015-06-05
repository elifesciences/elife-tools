Feature: Get component DOI from the document
  In order to extract component DOI objects in an article
  as a script 
  I will parse the component DOI from the xml file

  Scenario Outline: Count the number of component DOI
    Given I have the document <document>
    When I count the number of component DOI
    Then I count the total as <count>

  Examples:
    | document                    | count
    | elife-kitchen-sink.xml      | 40
    | elife00013.xml              | 28
    | elife_poa_e06828.xml        | 0


  Scenario Outline: Get the component DOI
    Given I have the document <document>
    When I get the component DOI
    And I get the list item <list_item>
    Then I see the string <string>

  Examples:
    | document                    | list_item                  | string
    | elife-kitchen-sink.xml      | [0]['doi']                 | 10.7554/eLife.00013.001
    | elife-kitchen-sink.xml      | [0]['position']            | 1
    | elife-kitchen-sink.xml      | [0]['type']                | abstract
    
    | elife-kitchen-sink.xml      | [2]['doi']                 | 10.7554/eLife.00013.003
    | elife-kitchen-sink.xml      | [2]['position']            | 3
    | elife-kitchen-sink.xml      | [2]['type']                | fig
    
    | elife-kitchen-sink.xml      | [3]['doi']                 | 10.7554/eLife.00013.004
    | elife-kitchen-sink.xml      | [3]['position']            | 4
    | elife-kitchen-sink.xml      | [3]['type']                | supplementary-material
    
    | elife-kitchen-sink.xml      | [5]['doi']                 | 10.7554/eLife.00013.006
    | elife-kitchen-sink.xml      | [5]['position']            | 6
    | elife-kitchen-sink.xml      | [5]['type']                | media
    
    | elife-kitchen-sink.xml      | [6]['doi']                 | 10.1371/journal.pone.0118223
    | elife-kitchen-sink.xml      | [6]['position']            | 7
    | elife-kitchen-sink.xml      | [6]['type']                | chem-struct-wrap
    
    | elife-kitchen-sink.xml      | [8]['doi']                 | 10.7554/eLife.00013.007
    | elife-kitchen-sink.xml      | [8]['position']            | 9
    | elife-kitchen-sink.xml      | [8]['type']                | table-wrap
    
    | elife-kitchen-sink.xml      | [9]['doi']                 | 10.7554/eLife.00013.008
    | elife-kitchen-sink.xml      | [9]['position']            | 10
    | elife-kitchen-sink.xml      | [9]['type']                | supplementary-material

    | elife-kitchen-sink.xml      | [10]['doi']                | 10.7554/eLife.00013.009
    | elife-kitchen-sink.xml      | [10]['position']           | 11
    | elife-kitchen-sink.xml      | [10]['type']               | boxed-text
    
    | elife00013.xml              | [0]['doi']                 | 10.7554/eLife.00013.001
    | elife00013.xml              | [0]['type']                | abstract
    
    | elife_poa_e06828.xml        | [0]['doi']                 | None
    | elife_poa_e06828.xml        | [0]['type']                | None