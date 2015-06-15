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
    | elife-kitchen-sink.xml      | 42
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
    | elife00013.xml              | table-wrap    | 3
    | elife_poa_e06828.xml        | abstract      | 0

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
    | elife00013.xml              | [1]['type']                | abstract
    | elife00013.xml              | [1]['content']             | All animals, including humans, evolved in a world filled with bacteria. Although bacteria are most familiar as pathogens, some bacteria produce small molecules that are essential for the biology of animals and other eukaryotes, although the details of the ways in which these bacterial molecules are beneficial are not well understood. The choanoflagellates are water-dwelling organisms that use their whip-like flagella to move around, feeding on bacteria. They can exist as one cell or a colony of multiple cells and, perhaps surprisingly, are the closest known living relatives of animals. This means that experiments on these organisms have the potential to improve our understanding of animal development and the transition from egg to embryo to adult. Alegado et al. have explored how the morphology of Salpingoeca rosetta, a colony-forming choanoflagellate, is influenced by its interactions with various species of bacteria. In particular, they find that the development of multicellularity in S. rosetta is triggered by the presence of the bacterium Algoriphagus machipongonensis as well as its close relatives. They also identify the signaling molecule produced by the bacteria to be C32H64NO7S; this lipid molecule is an obscure relative of the sphingolipid molecules that have important roles in signal transmission in animals, plants, and fungi. Moreover, Alegado et al. show that S. rosetta can respond to this molecule – which they call rosette-inducing factor (RIF-1) – over a wide range of concentrations, including concentrations as low as 10−17 M. The work of Alegado et al. suggests that interactions between S. rosetta and Algoriphagus bacteria could be a productive model system for studying the influences of bacteria on animal cell biology, and for investigating the mechanisms of signal delivery and reception. Moreover, the molecular mechanisms revealed by this work leave open the possibility that bacteria might have contributed to the evolution of multicellularity in animals. DOI: http://dx.doi.org/10.7554/eLife.00013.002
    | elife00013.xml              | [2]['type']                | fig
    | elife00013.xml              | [4]['type']                | table-wrap
    | elife00013.xml              | [28]['type']               | sub-article
    | elife00013.xml              | [28]['doi']                | 10.7554/eLife.00013.029
    | elife00013.xml              | [28]['label']              | None
    | elife00013.xml              | [28]['full_label']         | None
    | elife00013.xml              | [28]['title']              | Decision letter
    | elife00013.xml              | [28]['full_title']         | Decision letter

    | elife02304.xml              | [0]['doi']                    | 10.7554/eLife.02304.001
    | elife02304.xml              | [0]['position']               | 1
    | elife02304.xml              | [0]['type']                   | abstract
    | elife02304.xml              | [0]['parent_type']            | None
    | elife02304.xml              | [0]['parent_parent_type']     | None
    | elife02304.xml              | [0]['label']                  | None
    | elife02304.xml              | [0]['full_label']             | None
    | elife02304.xml              | [0]['title']                  | None
    | elife02304.xml              | [0]['full_title']             | None
    
    | elife02304.xml              | [1]['label']                  | None
    | elife02304.xml              | [1]['full_label']             | None
    | elife02304.xml              | [1]['title']                  | eLife digest
    | elife02304.xml              | [1]['full_title']             | eLife digest
    
    | elife02304.xml              | [6]['doi']                    | 10.7554/eLife.02304.007
    | elife02304.xml              | [6]['position']               | 7
    | elife02304.xml              | [6]['type']                   | fig
    | elife02304.xml              | [6]['parent_type']            | fig
    | elife02304.xml              | [6]['parent_parent_type']     | None
    | elife02304.xml              | [6]['label']                  | Figure 2—figure supplement 2.
    | elife02304.xml              | [6]['full_label']             | Figure 2—figure supplement 2.
    | elife02304.xml              | [6]['title']                  | Alanine scanning of PfLDH specificity loop.
    | elife02304.xml              | [6]['full_title']             | Alanine scanning of <italic>Pf</italic>LDH specificity loop.
    | elife02304.xml              | [6]['caption']                | Logarithm of pyruvate kcat/KM of PfLDH and each mutant. Labels on x-axis describe the mutation tested in the WT PfLDH background.
    | elife02304.xml              | [6]['full_caption']           | Logarithm of pyruvate k<sub>cat</sub>/K<sub>M</sub> of <italic>Pf</italic>LDH and each mutant. Labels on x-axis describe the mutation tested in the WT <italic>Pf</italic>LDH background.
    
    | elife02304.xml              | [7]['doi']                    | 10.7554/eLife.02304.008
    | elife02304.xml              | [7]['position']               | 8
    | elife02304.xml              | [7]['ordinal']                | 1
    | elife02304.xml              | [7]['type']                   | supplementary-material
    | elife02304.xml              | [7]['parent_type']            | fig
    | elife02304.xml              | [7]['parent_ordinal']         | 5
    | elife02304.xml              | [7]['parent_parent_type']     | fig
    | elife02304.xml              | [7]['parent_parent_ordinal']  | 3
    | elife02304.xml              | [7]['label']                  | Figure 2—figure supplement 2—source data 1.
    | elife02304.xml              | [7]['full_label']             | Figure 2—figure supplement 2—source data 1.
    | elife02304.xml              | [7]['title']                  | Kinetic parameters for PfLDH alanine-scan.
    | elife02304.xml              | [7]['full_title']             | Kinetic parameters for PfLDH alanine-scan.
    | elife02304.xml              | [7]['caption']                | None
    | elife02304.xml              | [7]['full_caption']           | None
    
    | elife05502.xml              | [3]['doi']                   | 10.7554/eLife.05502.004
    | elife05502.xml              | [3]['position']              | 4
    | elife05502.xml              | [3]['ordinal']               | 2
    | elife05502.xml              | [3]['type']                  | fig
    | elife05502.xml              | [3]['parent_type']           | None
    | elife05502.xml              | [3]['parent_ordinal']        | None
    | elife05502.xml              | [3]['label']                  | Figure 2.
    | elife05502.xml              | [3]['full_label']             | Figure 2.
    | elife05502.xml              | [3]['title']                  | Knockdown (KD) of BMP signaling components results in completely ventralized (dpp-, tld-RNAi) or completely dorsalized (sog-, tsg-RNAi) embryos.
    | elife05502.xml              | [3]['full_title']             | Knockdown (KD) of BMP signaling components results in completely ventralized (<italic>dpp-, tld-</italic>RNAi) or completely dorsalized (<italic>sog-</italic>, <italic>tsg-</italic>RNAi) embryos.
    | elife05502.xml              | [3]['caption']                | Expression of twi (A, E, I, M, Q), sim (B, F, J, N, R) and sog (C, G, K, O, S) in wild type (wt) embryos (A–C), dpp-RNAi embryos (E–G), sog-RNAi embryos (I–K), tsg-RNAi embryos (M–O) and tld-RNAi embryos (Q–S) monitored by whole mount in situ hybridization (ISH). The view is lateral with the dorsal side pointing up (A–C), ventral (K), or not determined as the expression is DV-symmetric (E–G, I, J, M–O, Q–S). Embryos are at the blastoderm stage (∼26–32 hpf: A, C, E–G, I–K, M, O, Q, S), or at the beginning of anatrepsis (posterior invagination of the embryo, ∼33–37 hpf) (B). Scale bar (A) corresponds to 200 µm. For phenotype frequencies and confirmation of KD see Figure 2—figure supplement 2 and Figure 5—figure supplement 1. (D, H, L, P, T) Simulations of the reaction diffusion system described in Box 1 on a two-dimensional cylinder (Figure 10). Depicted is one half of the cylinder surface stretching from the dorsal (D) to the ventral (V) midline. Blue: sog expression (η). Gray: BMP concentration (b). (D) In wt sog expression is confined to a ventral stripe. (H) Loss of BMP (b = 0) leads to uniform derepression of sog. (L) Loss of sog (s = 0) leads to uniformly high levels of BMP. (P) Loss of Tsg was modeled by assuming that no Sog-BMP complexes are formed (k+ = 0). This results in high BMP signaling throughout the embryo. (T) Loss of Tld was modeled by reducing the degradation constant of Sog (αs) by 90%. As Sog-BMP complexes are not degraded, BMP is not released, causing uniform derepression of sog.
    | elife05502.xml              | [3]['full_caption']           | Expression of <italic>twi</italic> (<bold>A</bold>, <bold>E</bold>, <bold>I</bold>, <bold>M</bold>, <bold>Q</bold>), <italic>sim</italic> (<bold>B</bold>, <bold>F</bold>, <bold>J</bold>, <bold>N</bold>, <bold>R</bold>) and <italic>sog</italic> (<bold>C</bold>, <bold>G</bold>, <bold>K</bold>, <bold>O</bold>, <bold>S</bold>) in wild type (wt) embryos (<bold>A</bold>–<bold>C</bold>), <italic>dpp</italic>-RNAi embryos (<bold>E</bold>–<bold>G</bold>), <italic>sog</italic>-RNAi embryos (<bold>I</bold>–<bold>K</bold>), <italic>tsg</italic>-RNAi embryos (<bold>M</bold>–<bold>O</bold>) and <italic>tld</italic>-RNAi embryos (<bold>Q</bold>–<bold>S</bold>) monitored by whole mount in situ hybridization (ISH). The view is lateral with the dorsal side pointing up (<bold>A</bold>–<bold>C</bold>), ventral (<bold>K</bold>), or not determined as the expression is DV-symmetric (<bold>E</bold>–<bold>G</bold>, <bold>I</bold>, <bold>J</bold>, <bold>M</bold>–<bold>O</bold>, <bold>Q</bold>–<bold>S</bold>). Embryos are at the blastoderm stage (∼26–32 hpf: <bold>A</bold>, <bold>C</bold>, <bold>E</bold>–<bold>G</bold>, <bold>I</bold>–<bold>K</bold>, <bold>M</bold>, <bold>O</bold>, <bold>Q</bold>, <bold>S</bold>), or at the beginning of anatrepsis (posterior invagination of the embryo, ∼33–37 hpf) (<bold>B</bold>). Scale bar (<bold>A</bold>) corresponds to 200 µm. For phenotype frequencies and confirmation of KD see <xref ref-type="fig" rid="fig2s2">Figure 2—figure supplement 2</xref> and <xref ref-type="fig" rid="fig5s1">Figure 5—figure supplement 1</xref>. (<bold>D</bold>, <bold>H</bold>, <bold>L</bold>, <bold>P</bold>, <bold>T</bold>) Simulations of the reaction diffusion system described in <xref ref-type="boxed-text" rid="box1">Box 1</xref> on a two-dimensional cylinder (<xref ref-type="fig" rid="fig10">Figure 10</xref>). Depicted is one half of the cylinder surface stretching from the dorsal (D) to the ventral (V) midline. Blue: <italic>sog</italic> expression (<italic>η</italic>). Gray: BMP concentration (<bold><italic><bold>b</bold></italic></bold>). (<bold>D</bold>) In wt <italic>sog</italic> expression is confined to a ventral stripe. (<bold>H</bold>) Loss of BMP (<italic>b</italic> = 0) leads to uniform derepression of <italic>sog</italic>. (<bold>L</bold>) Loss of <italic>sog</italic> (<italic>s</italic> = 0) leads to uniformly high levels of BMP. (<bold>P</bold>) Loss of Tsg was modeled by assuming that no Sog-BMP complexes are formed (<italic>k</italic><sub><italic>+</italic></sub> = 0). This results in high BMP signaling throughout the embryo. (<bold>T</bold>) Loss of Tld was modeled by reducing the degradation constant of Sog (<italic>α</italic><sub><italic>s</italic></sub>) by 90%. As Sog-BMP complexes are not degraded, BMP is not released, causing uniform derepression of <italic>sog</italic>.
    
    | elife05502.xml              | [13]['doi']                   | 10.7554/eLife.05502.014
    | elife05502.xml              | [13]['position']              | 14
    | elife05502.xml              | [13]['ordinal']               | 1
    | elife05502.xml              | [13]['type']                  | boxed-text
    | elife05502.xml              | [13]['parent_type']           | None
    | elife05502.xml              | [13]['parent_ordinal']        | None
    | elife05502.xml              | [13]['label']                 | Box 1.
    | elife05502.xml              | [13]['full_label']            | Box 1.
    | elife05502.xml              | [13]['title']                 | Temporal progression of pattern formation.
    | elife05502.xml              | [13]['full_title']            | Temporal progression of pattern formation.
    
    
    | elife05502.xml              | [14]['doi']                   | 10.7554/eLife.05502.015
    | elife05502.xml              | [14]['position']              | 15
    | elife05502.xml              | [14]['ordinal']               | 12
    | elife05502.xml              | [14]['type']                  | fig
    | elife05502.xml              | [14]['parent_type']           | boxed-text
    | elife05502.xml              | [14]['parent_ordinal']        | 1
    | elife05502.xml              | [14]['label']                 | Box figure 1.
    | elife05502.xml              | [14]['full_label']            | Box figure 1.
    | elife05502.xml              | [14]['title']                 | Temporal progression of pattern formation.
    | elife05502.xml              | [14]['full_title']            | Temporal progression of pattern formation.
    
    | elife00380.xml              | [43]['doi']                    | 10.7554/eLife.00380.044
    | elife00380.xml              | [45]['caption']                | None
    | elife00380.xml              | [45]['full_caption']           | None
    
    | elife-kitchen-sink.xml      | [5]['doi']                    | 10.7554/eLife.00013.006
    | elife-kitchen-sink.xml      | [5]['type']                   | media
    | elife-kitchen-sink.xml      | [5]['ordinal']                | 1
    | elife-kitchen-sink.xml      | [5]['parent_type']            | None
    | elife-kitchen-sink.xml      | [35]['doi']                   | 10.7554/eLife.00013.034
    | elife-kitchen-sink.xml      | [35]['parent_type']           | None
    | elife-kitchen-sink.xml      | [36]['doi']                   | 10.7554/eLife.00013.035
    | elife-kitchen-sink.xml      | [36]['parent_type']           | None
    | elife-kitchen-sink.xml      | [37]['doi']                   | 10.7554/eLife.00013.036
    | elife-kitchen-sink.xml      | [37]['parent_type']           | None
    
    | elife-kitchen-sink.xml      | [38]['doi']                   | 10.7554/eLife.00013.037
    | elife-kitchen-sink.xml      | [38]['type']                  | sub-article
    | elife-kitchen-sink.xml      | [38]['parent_type']           | None
    
    #| elife-kitchen-sink.xml      | [39]['doi']                   | 10.7554/eLife.00013.038
    #| elife-kitchen-sink.xml      | [39]['type']                  | fig
    #| elife-kitchen-sink.xml      | [39]['parent_type']           | None
    #
    #| elife-kitchen-sink.xml      | [40]['doi']                   | 10.7554/eLife.00013.039
    #| elife-kitchen-sink.xml      | [40]['type']                  | table-wrap
    #| elife-kitchen-sink.xml      | [40]['parent_type']           | sub-article
    
  Scenario Outline: Count the number of components permissions
    Given I have the document <document>
    When I get the components
    And I count permissions of components index <index>
    Then I count the total as <permissions>
    
  Examples:
    | document                    | index                  | permissions
    | elife-kitchen-sink.xml      | 10                     | 0
    | elife-kitchen-sink.xml      | 11                     | 2
    
    
  Scenario Outline: Get the components permissions
    Given I have the document <document>
    When I get the components
    And I get the list item <list_item>
    Then I see the string <string>
  
  Examples:
    | document                    | list_item                                       | string
    | elife-kitchen-sink.xml      | [10]['permissions'][0]['copyright_statement']   | None
    | elife-kitchen-sink.xml      | [11]['permissions'][0]['copyright_statement']   | © 1977 Thieme Medical Publishers. All Rights Reserved.
    | elife-kitchen-sink.xml      | [11]['permissions'][0]['copyright_year']        | 1977
    | elife-kitchen-sink.xml      | [11]['permissions'][0]['copyright_holder']      | Thieme Medical Publishers
    | elife-kitchen-sink.xml      | [11]['permissions'][0]['license']               | Figure 1, lower panel, is reproduced from Hughes and Sperandio, 2008 with permission.
    | elife-kitchen-sink.xml      | [11]['permissions'][0]['full_license']          | Figure 1, lower panel, is reproduced from <xref ref-type="bibr" rid="bib45">Hughes and Sperandio, 2008</xref> with permission.
    | elife-kitchen-sink.xml      | [11]['permissions'][0]['license_url']           | None
    | elife-kitchen-sink.xml      | [11]['permissions'][1]['copyright_statement']   | © 2007 Elsevier Masson SAS. All rights reserved
    | elife-kitchen-sink.xml      | [11]['permissions'][1]['copyright_year']        | 2007
    | elife-kitchen-sink.xml      | [11]['permissions'][1]['copyright_holder']      | Elsevier Masson SAS
    | elife-kitchen-sink.xml      | [11]['permissions'][1]['license']               | The patient figure in Figure 6, part A is reproduced from \n                                Koropatnick et al., 2004, European Journal of Medical Genetics with permission.
    | elife-kitchen-sink.xml      | [11]['permissions'][1]['full_license']          | The patient figure in Figure 6, part <bold>A</bold> is reproduced from \n                                <xref ref-type="bibr" rid="bib58">Koropatnick et al., 2004</xref>, <italic>European Journal of Medical Genetics</italic> with permission.
    | elife-kitchen-sink.xml      | [11]['permissions'][1]['license_url']           | None