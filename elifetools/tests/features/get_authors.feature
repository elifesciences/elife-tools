Feature: get authors from the document
	In order to put my author names in my api
	as a script 
	I will parse the authors from the xml file
	
  Scenario Outline: Count the number of authors
    Given I have the document <document>
		When I count the number of authors 
		Then I count the total authors as <authors>
	
  Examples:
    | document                    | authors
		| NLM3-sample-for-elife.1.xml | 4       
    | NLM3-sample-for-elife.2.xml | 3       
    | elife-sample-jun2012.xml    | 26
    | elife_pmc_preview_version_17.xml    | 10 