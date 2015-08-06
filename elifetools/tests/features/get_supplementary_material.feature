Feature: Get supplementary material data from the document
  In order to extract supplementary material from an article
  as a script 
  I will parse the supplementary material from the xml file

  Scenario Outline: Count the number of supplementary material
    Given I have the document <document>
    When I count the number of supplementary material
    Then I count the total as <count>

  Examples:
    | document                    | count
    | elife-kitchen-sink.xml      | 5
    | elife00013.xml              | 0
    | elife00005.xml              | 2
    | elife02304.xml              | 8
    | elife_poa_e06828.xml        | 0

  Scenario Outline: Get the supplementary material
    Given I have the document <document>
    When I get the supplementary material
    And I get the list item <list_item>
    Then I see the string <string>
  
  Examples:
    | document                    | list_item                        | string
    | elife-kitchen-sink.xml      | [0]['type']                      | supplementary-material
    | elife-kitchen-sink.xml      | [0]['asset']                     | data
    | elife-kitchen-sink.xml      | [0]['component_doi']             | 10.7554/eLife.00013.004
    | elife-kitchen-sink.xml      | [0]['label']                     | Figure 1—source data 1.
    | elife-kitchen-sink.xml      | [0]['full_label']                | Figure 1—source data 1.
    | elife-kitchen-sink.xml      | [0]['sibling_ordinal']           | 1
    | elife-kitchen-sink.xml      | [0]['ordinal']                   | 1
    | elife-kitchen-sink.xml      | [0]['position']                  | 1
    
    | elife-kitchen-sink.xml      | [1]['asset']                     | data
    | elife-kitchen-sink.xml      | [1]['ordinal']                   | 2
    | elife-kitchen-sink.xml      | [1]['sibling_ordinal']           | 1
    
    | elife-kitchen-sink.xml      | [2]['asset']                     | supp
    | elife-kitchen-sink.xml      | [2]['ordinal']                   | 3
    | elife-kitchen-sink.xml      | [2]['sibling_ordinal']           | 1
    
    | elife-kitchen-sink.xml      | [3]['asset']                     | supp
    | elife-kitchen-sink.xml      | [3]['ordinal']                   | 4
    | elife-kitchen-sink.xml      | [3]['sibling_ordinal']           | 2
    
    | elife-kitchen-sink.xml      | [4]['asset']                     | code
    | elife-kitchen-sink.xml      | [4]['ordinal']                   | 5
    | elife-kitchen-sink.xml      | [4]['sibling_ordinal']           | 1
    
    | elife02304.xml              | [0]['component_doi']             | 10.7554/eLife.02304.008
    | elife02304.xml              | [0]['asset']                     | data
    | elife02304.xml              | [0]['ordinal']                   | 1
    | elife02304.xml              | [0]['sibling_ordinal']           | 1
    
    | elife02304.xml              | [1]['component_doi']             | 10.7554/eLife.02304.015
    | elife02304.xml              | [1]['asset']                     | data
    | elife02304.xml              | [1]['ordinal']                   | 2
    | elife02304.xml              | [1]['sibling_ordinal']           | 1
    
    | elife02304.xml              | [2]['component_doi']             | 10.7554/eLife.02304.017
    | elife02304.xml              | [2]['asset']                     | data
    | elife02304.xml              | [2]['ordinal']                   | 3
    | elife02304.xml              | [2]['sibling_ordinal']           | 1
    
    | elife02304.xml              | [3]['component_doi']             | 10.7554/eLife.02304.020
    | elife02304.xml              | [3]['asset']                     | data
    | elife02304.xml              | [3]['ordinal']                   | 4
    | elife02304.xml              | [3]['sibling_ordinal']           | 1
    
    | elife02304.xml              | [4]['component_doi']             | 10.7554/eLife.02304.021
    | elife02304.xml              | [4]['asset']                     | data
    | elife02304.xml              | [4]['ordinal']                   | 5
    | elife02304.xml              | [4]['sibling_ordinal']           | 2
    
    | elife02304.xml              | [5]['component_doi']             | 10.7554/eLife.02304.032
    | elife02304.xml              | [5]['asset']                     | data
    | elife02304.xml              | [5]['ordinal']                   | 6
    | elife02304.xml              | [5]['sibling_ordinal']           | 1
    
    | elife02304.xml              | [6]['component_doi']             | 10.7554/eLife.02304.033
    | elife02304.xml              | [6]['asset']                     | supp
    | elife02304.xml              | [6]['ordinal']                   | 7
    | elife02304.xml              | [6]['sibling_ordinal']           | 1
    
    | elife02304.xml              | [7]['component_doi']             | 10.7554/eLife.02304.034
    | elife02304.xml              | [7]['asset']                     | supp
    | elife02304.xml              | [7]['ordinal']                   | 8
    | elife02304.xml              | [7]['sibling_ordinal']           | 2
    
    