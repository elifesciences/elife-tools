Feature: Use xmlio library to read, modify and output XML
  In order to use the xml IO component of this module
  as a script 
  I will process some XML using it
  

  Scenario Outline: Parse an XML file to a root element
    Given I have run register_xmlns
    When I use xmlio to parse the <document>
    And I output the xml root
    
  Examples:
    | document              
    | elife-kitchen-sink.xml


  Scenario Outline: Get the tag first instance
    Given I have run register_xmlns
    When I use xmlio to parse the <input_document>
    And I get the first element index of <tag>
    Then I see the string <string>
    
  Examples:
    | input_document        | tag             | string
    | xmlio_input.xml       | inline-graphic  | 2
    | xmlio_input.xml       | italic          | None

  Scenario Outline: Add a tag before
    Given I have the xml <xml>
    And I turn the xml into an element
    When I add tag <tag_name> with text <tag_text> before tag name <before>
    And I convert the element to string
    Then I see the string <string>
    
  Examples:
    | xml         | tag_name  | tag_text | before | string
    | <a><b/></a> | c         | see      | b      | <a><c>see</c><b /></a>

  Scenario Outline: Convert xlink href values in tags
    Given I have run register_xmlns
    And I have the list json <name_map>
    When I use xmlio to parse the <input_document>
    And I convert the xlink href
    And I output the xml root
    Then I compare the string to the document <output_document>
    
  Examples:
    | name_map                                         | input_document      | output_document
    | {"doc1.pdf":"doc-1.pdf","img2.tif":"img-2.tif"}  | xmlio_input.xml     | xmlio_output_convert_xlink.xml