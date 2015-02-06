from bs4 import BeautifulSoup
import cgi
import htmlentitydefs
import os
import time
import calendar

import logging
logger = logging.getLogger('myapp')
hdlr = logging.FileHandler(os.getcwd() + os.sep + 'test.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.INFO)


def	swap_en_dashes(textHTMLEntities):
	title = textHTMLEntities.replace("&#8211;", "&#x02013;")#.encode('ascii', 'xmlcharrefreplace')
	return title

def unicodeToHTMLEntities(text):
    """Converts unicode to HTML entities.  For example '&' becomes '&amp;'."""
    returnText = cgi.escape(text).encode('ascii', 'xmlcharrefreplace')
    return returnText

def format_text(title_text):
	textHTMLEntities = unicodeToHTMLEntities(title_text)
	textHTMLEntitiesReverted = swap_en_dashes(textHTMLEntities)
	return textHTMLEntitiesReverted

def flatten(function):
	"""
	Convert or flatten value; if list length is zero then return None,
	if length of a list is 1, convert to a string, otherwise return
	the list as given
	"""
	def wrapper(*args, **kwargs):
		value = function(*args, **kwargs)
		if(type(value) == list and len(value) == 0):
			return None
		elif(type(value) == list and len(value) == 1):
			# If there is only one list element, return a singleton
			return value[0]
		else:
			return value
		return value
	return wrapper

def strip_strings(value):
	"""
	Strip excess whitespace, on strings, and simple lists
	using recursion
	"""
	if (value == None):
		return None
	elif (type(value) == list):
		# List, so recursively strip elements
		for i in range(0, len(value)):
			value[i] = strip_strings(value[i])
		return value
	else:
		try:
			value = value.replace("  ", " ")
			return value.strip()
		except(AttributeError):
			return value
		
def strip_punctuation_space(value):
	"""
	Strip excess whitespace prior to punctuation
	using recursion
	"""
	if (value == None):
		return None
	elif (type(value) == list):
		# List, so recursively strip elements
		for i in range(0, len(value)):
			value[i] = strip_punctuation_space(value[i])
		return value
	else:
		try:
			value = value.replace(" .", ".")
			value = value.replace(" :", ":")
			value = value.replace("( ", "(")
			value = value.replace(" )", ")")
			return value
		except(AttributeError):
			return value
		
def strippen(function):
	"""
	Strip excess whitespace as a decorator
	"""
	def wrapper(*args, **kwargs):
		value = function(*args, **kwargs)
		return strip_strings(value)
	return wrapper

def inten(function):
	"""
	Try to convert to int as a decorator
	"""
	def wrapper(*args, **kwargs):
		value = function(*args, **kwargs)
		if (value == None):
			return None
		else:
			try:
				return int(value)
			except(TypeError):
				return value
	return wrapper

def revert_entities(function):
	"this is the decorator"
	def wrapper(*args, **kwargs):
		text = function(*args, **kwargs)
		formatted_text = format_text(text)
		return formatted_text
	return wrapper

def parse_document(filelocation):
	return parse_xml(open(filelocation))

def parse_xml(xml):
	soup = BeautifulSoup(xml, ["lxml", "xml"])
	return soup

def extract_nodes(soup, nodename, attr = None, value = None):
	tags = soup.find_all(nodename)
	if(attr != None and value != None):
		# Further refine nodes by attributes
		tags_by_value = []
		for tag in tags:
			try:
				if tag[attr] == value:
					tags_by_value.append(tag)
			except KeyError:
				continue
		return tags_by_value
	return tags

def extract_first_node(soup, nodename):
	tags = extract_nodes(soup, nodename)
	try:
		tag = tags[0]
	except(IndexError):
		# Tag not found
		return None
	return tag

def extract_node_text(soup, nodename, attr = None, value = None):
	"""
	Extract node text by nodename, unless attr is supplied
	If attr and value is specified, find all the nodes and search
	  by attr and value for the first node
	"""
	tag_text = None
	if(attr == None):
		tag = extract_first_node(soup, nodename)
		try:
			tag_text = tag.text
		except(AttributeError):
			# Tag text not found
			return None
	else:
		tags = extract_nodes(soup, nodename, attr, value)
		for tag in tags:
			try:
				if tag[attr] == value:
					tag_text = tag.text
			except KeyError:
				continue
	return tag_text

def title(soup):
	return article_title(soup)
	
@revert_entities # make cleaning up the entiteis a decorator, as we may be able to drop all this code later
def article_title(soup):
	title_text = extract_node_text(soup, "article-title")
	return title_text

def doi(soup):
	doi_tags = extract_nodes(soup, "article-id", attr = "pub-id-type", value = "doi")
	for tag in doi_tags:
		# Only look at the doi tag directly inside the article-meta section
		if (tag.parent.name == "article-meta"):
			doi = tag.text
	return doi
		
def pmid(soup):
	pmid = extract_node_text(soup, "article-id", attr = "pub-id-type", value = "pmid")
	return pmid
		
def authors(soup):
	"""Find and return all the authors"""
	tags = extract_nodes(soup, "contrib", attr = "contrib-type", value = "author")
	authors = []
	position = 1
	
	article_doi = doi(soup)
	
	for tag in tags:
		author = {}
		
		# Person id
		try:
			person_id = tag["id"]
			person_id = person_id.replace("author-", "")
			author['person_id'] = int(person_id)
		except(KeyError):
			pass

		# Equal contrib
		try:
			equal_contrib = tag["equal-contrib"]
			if(equal_contrib == 'yes'):
				author['equal_contrib'] = True
		except(KeyError):
			pass
		
		# Correspondence
		try:
			corresponding = tag["corresp"]
			if(corresponding == 'yes'):
				author['corresponding'] = True
		except(KeyError):
			pass
		
		# Surname
		surname = extract_node_text(tag, "surname")
		if(surname != None):
			author['surname'] = surname

		# Given names
		given_names = extract_node_text(tag, "given-names")
		if(given_names != None):
			author['given_names'] = given_names
		
		# Find and parse affiliations
		affs = extract_nodes(tag, "xref", attr = "ref-type", value = "aff")
		if(len(affs) > 0):
			# One or more affiliations
			if(len(affs) > 1):
				# Prepare for multiple affiliations if multiples found
				author['country'] = []
				author['institution'] = []
				author['department'] = []
				author['city'] = []
				
			for aff in affs:
				# Find the matching affiliation detail
				rid = aff['rid']

				aff_node = extract_nodes(soup, "aff", attr = "id", value = rid)
				country = extract_node_text(aff_node[0], "country")
				institution = extract_node_text(aff_node[0], "institution")
				department = extract_node_text(aff_node[0], "named-content", attr = "content-type", value = "department")
				city = extract_node_text(aff_node[0], "named-content", attr = "content-type", value = "city")
				
				# Convert None to empty string if there is more than one affiliation
				if((country == None) and (len(affs) > 1)):
					country = ''
				if((institution == None) and (len(affs) > 1)):
					institution = ''
				if((department == None) and (len(affs) > 1)):
					department = ''
				if((city == None) and (len(affs) > 1)):
					city = ''
					
				# Append values
				try:
					# Multiple values
					author['country'].append(country)
				except(KeyError):
					author['country'] = country
				try:
					# Multiple values
					author['institution'].append(institution)
				except(KeyError):
					author['institution'] = institution
				try:
					# Multiple values
					author['department'].append(department)
				except(KeyError):
					author['department'] = department
				try:
					# Multiple values
					author['city'].append(city)
				except(KeyError):
					author['city'] = city

		# Author - given names + surname
		author_name = ""
		if(given_names != None):
			author_name += given_names + " "
		if(surname != None):
			author_name += surname
		author['author'] = author_name
		
		# Add xref linked correspondence author notes if applicable
		cors = extract_nodes(tag, "xref", attr = "ref-type", value = "corresp")
		if(len(cors) > 0):
			# One or more 
			if(len(cors) > 1):
				# Prepare for multiple values if multiples found
				author['notes_correspondence'] = []
				
			for cor in cors:
				# Find the matching affiliation detail
				rid = cor['rid']

				# Find elements by id
				try:
					corresp_node = soup.select("#" + rid)
					author_notes = corresp_node[0].get_text(" ")
					author_notes = strip_strings(author_notes)
				except:
					continue
				try:
					# Multiple values
					author['notes_correspondence'].append(author_notes)
				except(KeyError):
					author['notes_correspondence'] = author_notes
					
		# Add xref linked footnotes if applicable
		fns = extract_nodes(tag, "xref", attr = "ref-type", value = "fn")
		if(len(fns) > 0):
			# One or more 
			if(len(fns) > 1):
				# Prepare for multiple values if multiples found
				author['notes_footnotes'] = []
				
			for fn in fns:
				# Find the matching affiliation detail
				rid = fn['rid']

				# Find elements by id
				try:
					fn_node = soup.select("#" + rid)
					fn_text = fn_node[0].get_text(" ")
					fn_text = strip_strings(fn_text)
				except:
					continue
				try:
					# Multiple values
					author['notes_footnotes'].append(fn_text)
				except(KeyError):
					author['notes_footnotes'] = fn_text
					
		# Add xref linked other notes if applicable, such as funding detail
		others = extract_nodes(tag, "xref", attr = "ref-type", value = "other")
		if(len(others) > 0):
			# One or more 
			if(len(others) > 1):
				# Prepare for multiple values if multiples found
				author['notes_other'] = []
				
			for other in others:
				# Find the matching affiliation detail
				rid = other['rid']

				# Find elements by id
				try:
					other_node = soup.select("#" + rid)
					other_text = other_node[0].get_text(" ")
					other_text = strip_strings(other_text)
				except:
					continue
				try:
					# Multiple values
					author['notes_other'].append(other_text)
				except(KeyError):
					author['notes_other'] = other_text	

		# If not empty, add position value, append, then increment the position counter
		if(len(author) > 0):
			author['article_doi'] = article_doi
			
			author['position'] = position
			
			# Create a unique about tag value to make fom objects function
			author['about'] = 'author' + '_' + str(position) + '_' + article_doi
			
			authors.append(author)
			position += 1
		
	return authors

def references(soup):
	"""Renamed to refs"""
	return refs(soup)
	
def refs(soup):
	"""Find and return all the references"""
	tags = extract_nodes(soup, "ref")
	refs = []
	position = 1
	
	article_doi = doi(soup)
	
	for tag in tags:
		ref = {}
		
		# etal
		etal = extract_nodes(tag, "etal")
		try:
			if(etal[0]):
				ref['etal'] = True
		except(IndexError):
			pass
		
		# ref - human readable full reference text
		ref_text = tag.get_text(" ")
		ref_text = strip_strings(ref_text)
		# Remove excess space
		ref_text = ' '.join(ref_text.split())
		# Fix punctuation spaces and extra space
		ref['ref'] = strip_punctuation_space(strip_strings(ref_text))
		
		# article_title
		article_title = extract_node_text(tag, "article-title")
		if(article_title != None):
			ref['article_title'] = article_title
			
		# year
		year = extract_node_text(tag, "year")
		if(year != None):
			ref['year'] = year
			
		# source
		source = extract_node_text(tag, "source")
		if(source != None):
			ref['source'] = source
			
		# publication_type
		mixed_citation = extract_nodes(tag, "mixed-citation")
		try:
			publication_type = mixed_citation[0]["publication-type"]
			ref['publication_type'] = publication_type
		except(KeyError, IndexError):
			pass

		# authors
		person_group = extract_nodes(tag, "person-group")
		authors = []
		try:
			name = extract_nodes(person_group[0], "name")
			for n in name:
				surname = extract_node_text(n, "surname")
				given_names = extract_node_text(n, "given-names")
				# Convert all to strings in case a name component is missing
				if(surname is None):
					surname = ""
				if(given_names is None):
					given_names = ""
				full_name = strip_strings(surname + ' ' + given_names)
				authors.append(full_name)
			if(len(authors) > 0):
				ref['authors'] = authors
		except(KeyError, IndexError):
			pass
			
		# volume
		volume = extract_node_text(tag, "volume")
		if(volume != None):
			ref['volume'] = volume
			
		# fpage
		fpage = extract_node_text(tag, "fpage")
		if(fpage != None):
			ref['fpage'] = fpage
			
		# lpage
		lpage = extract_node_text(tag, "lpage")
		if(lpage != None):
			ref['lpage'] = lpage
			
		# collab
		collab = extract_node_text(tag, "collab")
		if(collab != None):
			ref['collab'] = collab
			
		# publisher_loc
		publisher_loc = extract_node_text(tag, "publisher-loc")
		if(publisher_loc != None):
			ref['publisher_loc'] = publisher_loc
		
		# publisher_name
		publisher_name = extract_node_text(tag, "publisher-name")
		if(publisher_name != None):
			ref['publisher_name'] = publisher_name
			
		# If not empty, add position value, append, then increment the position counter
		if(len(ref) > 0):
			ref['article_doi'] = article_doi
			
			ref['position'] = position
			
			# Create a unique about tag value to make fom objects function
			ref['about'] = 'ref' + '_' + str(position) + '_' + article_doi
			
			refs.append(ref)
			position += 1
	
	return refs

def components(soup):
	"""
	Find the components, i.e. those parts that would be assigned
	a unique component DOI, such as figures, tables, etc.
	"""
	components = []
	
	component_types = ["abstract", "fig", "table-wrap", "media", "chem-struct-wrap", "sub-article"]
	
	position = 1
	
	article_doi = doi(soup)
	
	# Find all tags for all component_types, allows the order
	#  in which they are found to be preserved
	tags = soup.find_all(component_types) 
	
	for tag in tags:
		
		component = {}
		
		# Component type is the tag's name
		ctype = tag.name
		
		# First find the doi if present
		if(ctype == "sub-article"):
			object_id = extract_node_text(tag, "article-id", attr = "pub-id-type", value = "doi")
		else:
			object_id = extract_node_text(tag, "object-id", attr = "pub-id-type", value = "doi")
		if(object_id is not None):
			component['doi'] = object_id
			component['doi_url'] = 'http://dx.doi.org/' + object_id
		else:
			# If no object-id is found, then skip this component
			continue

		# Remove the object-id doi before extracting the text
		extracted_tags = []
		try:
			object_id = tag.find_all(["article-id", "object-id"])
			extracted_tags.append(object_id[0].extract())
			#object_id[0].clear()
		except(IndexError):
			pass

		content = strip_strings(tag.get_text(" "))

		# Put the extracted tags back in, hacky as the original order is not preserved
		for et in extracted_tags:
			tag.insert(0, et)
			
		if(content != ""):
			component['content'] = content
	
		if(len(component) > 0):
			component['article_doi'] = article_doi
			component['type'] = ctype
			component['position'] = position
			
			# Use the component DOI as the unique about tag value
			component['about'] = component['doi_url']
			
			components.append(component)
			position += 1
	
	return components

def journal_id(soup):
	"""Find and return the primary journal id"""
	journal_id = extract_node_text(soup, "journal-id", attr = "journal-id-type", value = "hwp")
	return journal_id

@strippen
@flatten
def journal_title(soup):
	"""Find and return the journal title"""
	journal_title = extract_node_text(soup, "journal-title")
	return journal_title

@strippen
def journal_issn(soup, pub_type = None):
	"""
	Find and return the journal ISSN
	typical pub_type values: ppub, epub
	"""
	if (pub_type == None):
		return None
	journal_issn = extract_node_text(soup, "issn", attr = "pub-type", value = pub_type)
	return journal_issn

@strippen
def publisher(soup):
	publisher = extract_node_text(soup, "publisher-name")
	return publisher

@strippen
def abstract(soup):
	"""
	Find the article abstract and format it
	"""

	abstract_soup = []
	# Strip out the object-id so we only have the text
	try:
		abstract_soup = soup.find_all("abstract")
	except(IndexError):
		# No abstract found
		pass

	# Find the desired abstract node, <abstract>
	abstract_node = None
	for tag in abstract_soup:
		try:
			if(tag["abstract-type"] != None):
				# A tag attribute found, skip it
				pass
		except KeyError:
				# No attribute, use this abstract
				abstract_node = tag
				break
	
	# Shortcut: if no abstract found, return none
	if(abstract_node == None):
		return None

	# Allow the contents of certain markup tags, then
	#  remove any tags and their contents not on the allowed list
	allowed_tags = ["italic", "sup", "p"]

	for allowed in allowed_tags:
		tag = abstract_node.find_all(allowed)
		for t in tag:
			t.unwrap()
	
	# Done unwrapping allowed tags, now delete tags and enclosed
	# content of unallowed tags
	all = abstract_node.find_all()

	extracted_tags = []
	for a in all:
		# Extract the tags we do not want text from, and we will insert the tags back later
		#  using clear() will destroy them for good, and breaks the getting components by DOI
		extracted_tags.append(a.extract())
		#a.clear()

	abstract = abstract_node.text

	# Put the extracted tags back in, hacky as the original order is not preserved
	for et in extracted_tags:
		abstract_node.insert(0, et)
	
	return abstract

@flatten
def article_type(soup):
	"""
	Find the article_type from the article tag root XML attribute
	"""
	article_type = None
	article = extract_nodes(soup, "article")
	try:
		article_type = article[0]['article-type']	
	except(KeyError,IndexError):
		# Attribute or tag not found
		return None
	return article_type

def get_article_meta_aff(soup):
	"""
	Find the aff tag in the article-meta
	that is not part of an author contrib-group
	for populating article_institution and article_country
	"""
	aff = None
	try:
		article_meta = extract_nodes(soup, "article-meta")
		aff = extract_nodes(article_meta[0], "aff")
	except(IndexError):
		# Tag not found
		return None
	return aff
	
def article_institution(soup):
	"""
	Find the article_institution from an aff tag in the article-meta
	that is not part of an author contrib-group
	"""
	article_institution = None

	aff = get_article_meta_aff(soup)
	for tag in aff:
		# Only look at the first aff tag that is not part of a contrib-group
		if (tag.parent.name != "contrib-group"):
			article_institution = extract_node_text(tag, "institution")
	return article_institution

def article_country(soup):
	"""
	Find the article_country from an aff tag in the article-meta
	that is not part of an author contrib-group
	"""
	article_country = None

	aff = get_article_meta_aff(soup)
	for tag in aff:
		# Only look at the first aff tag that is not part of a contrib-group
		if (tag.parent.name != "contrib-group"):
			article_country = extract_node_text(tag, "country")
	return article_country

def get_kwd_group(soup):
	"""
	Find the kwd-group sections for further analysis to find
	subject_area, research_organism, and keywords
	"""
	kwd_group = None
	kwd_group = extract_nodes(soup, 'kwd-group')
	return kwd_group

@strippen
def subject_area(soup):
	"""
	Find the subject areas from article-categories subject tags
	"""
	subject_area = []
	try:
		article_meta = extract_nodes(soup, "article-meta")
		article_categories = extract_nodes(article_meta[0], "article-categories")
		subj_group = extract_nodes(article_categories[0], "subj-group")
		for tag in subj_group:
			tags = extract_nodes(tag, "subject")
			for t in tags:
				subject_area.append(t.text)
				
	except(IndexError):
		# Tag not found
		return None
	
	# Remove duplicates
	subject_area = list(set(subject_area))
	return subject_area

@flatten
def research_organism(soup):
	"""
	Find the research-organism from the set of kwd-group tags
	"""
	research_organism = []
	kwd_group = get_kwd_group(soup)
	for tag in kwd_group:
		try:
			if(tag["kwd-group-type"] == "research-organism" or tag["kwd-group-type"] == "Research-organism"):
				tags = extract_nodes(tag, "kwd")
				for t in tags:
					research_organism.append(t.text)
		except KeyError:
			continue
	return research_organism

@flatten
def keywords(soup):
	"""
	Find the keywords from the set of kwd-group tags
	"""
	keywords = []
	kwd_group = get_kwd_group(soup)
	for tag in kwd_group:
		try:
			if(tag["kwd-group-type"] != None):
				# A tag attribute found, check it for correct attribute
				if(tag["kwd-group-type"] == "author-keywords"):
					keywords.append(get_kwd(tag))
		except KeyError:
			# Tag attribute not found, we want this tag value
			keywords.append(get_kwd(tag))

	return keywords

@flatten
def get_kwd(tag):
	"""
	For extracting individual keywords (kwd) from a parent kwd-group
	refactored to use more than once in def keywords
	"""
	keywords = []
	kwd = extract_nodes(tag, "kwd")
	for k in kwd:
		keywords.append(k.text)
	return keywords

@strippen
def correspondence(soup):
	"""
	Find the corresp tags included in author-notes
	for primary correspondence
	"""
	correspondence = None
	try:
		author_notes = extract_nodes(soup, "author-notes")
		correspondence = extract_node_text(author_notes[0], "corresp")
	except(IndexError):
		# Tag not found
		return None
	return correspondence

@flatten
@strippen
def author_notes(soup):
	"""
	Find the fn tags included in author-notes
	"""
	author_notes = []
	try:
		author_notes_section = extract_nodes(soup, "author-notes")
		fn = extract_nodes(author_notes_section[0], "fn")
		for f in fn:
			try:
				if(f['fn-type'] != 'present-address'):
					author_notes.append(f.text)
				else:
					# Throw it away if it is a present-address footnote
					continue
			except(KeyError):
				# Append if the fn-type attribute does not exist
				author_notes.append(f.text)
	except(IndexError):
		# Tag not found
		return None
	return author_notes

def get_ymd(soup):
	"""
	Get the year, month and day from child tags
	"""
	day = extract_node_text(soup, "day")
	month = extract_node_text(soup, "month")
	year = extract_node_text(soup, "year")
	return (day, month, year)

def get_pub_date(soup, pub_type = "ppub"):
	"""
	Find the publishing date for populating
	pub_date_date, pub_date_day, pub_date_month, pub_date_year, pub_date_timestamp
	Default pub_type is ppub, but will revert to epub if tag is not found
	"""
	tz = "UTC"
	
	try:
		pub_date_section = extract_nodes(soup, "pub-date", attr = "pub-type", value = pub_type)
		if(len(pub_date_section) == 0):
			if(pub_type == "ppub"):
				pub_type = "epub"
			pub_date_section = extract_nodes(soup, "pub-date", attr = "pub-type", value = pub_type)
		(day, month, year) = get_ymd(pub_date_section[0])

	except(IndexError):
		# Tag not found, try the other
		return None
	
	date_string = None
	try:
		date_string = time.strptime(year + "-" + month + "-" + day + " " + tz, "%Y-%m-%d %Z")
	except(TypeError):
		# Date did not convert
		pass

	return date_string

def pub_date_date(soup):
	"""
	Find the publishing date pub_date_date in human readable form
	"""
	pub_date = get_pub_date(soup)
	date_string = None
	try:
		date_string = time.strftime("%B %d, %Y", pub_date)
	except(TypeError):
		# Date did not convert
		pass
	return date_string

@inten
def pub_date_day(soup):
	"""
	Find the publishing date pub_date_day
	"""
	pub_date = get_pub_date(soup)
	date_string = None
	try:
		date_string =  time.strftime("%d", pub_date)
	except(TypeError):
		# Date did not convert
		pass
	return date_string

@inten
def pub_date_month(soup):
	"""
	Find the publishing date pub_date_day
	"""
	pub_date = get_pub_date(soup)
	date_string = None
	try:
		date_string = time.strftime("%m", pub_date)
	except(TypeError):
		# Date did not convert
		pass
	return date_string
	
@inten
def pub_date_year(soup):
	"""
	Find the publishing date pub_date_day
	"""
	pub_date = get_pub_date(soup)
	date_string = None
	try:
		date_string = time.strftime("%Y", pub_date)
	except(TypeError):
		# Date did not convert
		pass
	return date_string

def pub_date_timestamp(soup):
	"""
	Find the publishing date pub_date_timestamp, in UTC time
	"""
	pub_date = get_pub_date(soup)
	timestamp = None
	try:
		timestamp = calendar.timegm(pub_date)
	except(TypeError):
		# Date did not convert
		pass
	return timestamp

def get_history_date(soup, date_type = None):
	"""
	Find a date in the history tag for the specific date_type
	typical date_type values: received, accepted
	"""
	if(date_type == None):
		return None
	
	tz = "UTC"
	
	try:
		history_section = extract_nodes(soup, "history")
		history_date_section = extract_nodes(soup, "date", attr = "date-type", value = date_type)
		(day, month, year) = get_ymd(history_date_section[0])
	except(IndexError):
		# Tag not found, try the other
		return None
	return time.strptime(year + "-" + month + "-" + day + " " + tz, "%Y-%m-%d %Z")

def received_date_date(soup):
	"""
	Find the received date received_date_date in human readable form
	"""
	received_date = get_history_date(soup, date_type = "received")
	date_string = None
	try:
		date_string = time.strftime("%B %d, %Y", received_date)
	except(TypeError):
		# Date did not convert
		pass
	return date_string

@inten
def received_date_day(soup):
	"""
	Find the received date received_date_day
	"""
	received_date = get_history_date(soup, date_type = "received")
	date_string = None
	try:
		date_string = time.strftime("%d", received_date)
	except(TypeError):
		# Date did not convert
		pass
	return date_string

@inten
def received_date_month(soup):
	"""
	Find the received date received_date_day
	"""
	received_date = get_history_date(soup, date_type = "received")
	date_string = None
	try:
		date_string = time.strftime("%m", received_date)
	except(TypeError):
		# Date did not convert
		pass
	return date_string
	
@inten
def received_date_year(soup):
	"""
	Find the received date received_date_day
	"""
	received_date = get_history_date(soup, date_type = "received")
	date_string = None
	try:
		date_string = time.strftime("%Y", received_date)
	except(TypeError):
		# Date did not convert
		pass
	return date_string

def received_date_timestamp(soup):
	"""
	Find the received date received_date_timestamp, in UTC time
	"""
	received_date = get_history_date(soup, date_type = "received")
	timestamp = None
	try:
		timestamp = calendar.timegm(received_date)
	except(TypeError):
		# Date did not convert
		pass
	return timestamp
	
def accepted_date_date(soup):
	"""
	Find the accepted date accepted_date_date in human readable form
	"""
	accepted_date = get_history_date(soup, date_type = "accepted")
	date_string = None
	try:
		date_string = time.strftime("%B %d, %Y", accepted_date)
	except(TypeError):
		# Date did not convert
		pass
	return date_string

@inten
def accepted_date_day(soup):
	"""
	Find the accepted date accepted_date_day
	"""
	accepted_date = get_history_date(soup, date_type = "accepted")
	date_string = None
	try:
		date_string = time.strftime("%d", accepted_date)
	except(TypeError):
		# Date did not convert
		pass
	return date_string

@inten
def accepted_date_month(soup):
	"""
	Find the accepted date accepted_date_day
	"""
	accepted_date = get_history_date(soup, date_type = "accepted")
	date_string = None
	try:
		date_string = time.strftime("%m", accepted_date)
	except(TypeError):
		# Date did not convert
		pass
	return date_string
	
@inten
def accepted_date_year(soup):
	"""
	Find the accepted date accepted_date_day
	"""
	accepted_date = get_history_date(soup, date_type = "accepted")
	date_string = None
	try:
		date_string = time.strftime("%Y", accepted_date)
	except(TypeError):
		# Date did not convert
		pass
	return date_string

def accepted_date_timestamp(soup):
	"""
	Find the accepted date accepted_date_timestamp, in UTC time
	"""
	accepted_date = get_history_date(soup, date_type = "accepted")
	timestamp = None
	try:
		timestamp = calendar.timegm(accepted_date)
	except(TypeError):
		# Date did not convert
		pass
	return timestamp

def get_funding_group(soup):
	"""
	Get the funding-group sections for populating
	funding_source lists
	"""
	funding_group_section = extract_nodes(soup, "funding-group")
	return funding_group_section

@flatten
def award_group_funding_source(soup):
	"""
	Find the award group funding sources, one for each
	item found in the get_funding_group section
	"""
	award_group_funding_source = []
	funding_group_section = get_funding_group(soup)
	for fg in funding_group_section:
		funding_source = extract_node_text(fg, "funding-source")
		award_group_funding_source.append(funding_source)
	return award_group_funding_source

@flatten
def award_group_award_id(soup):
	"""
	Find the award group award id, one for each
	item found in the get_funding_group section
	"""
	award_group_award_id = []
	funding_group_section = get_funding_group(soup)
	for fg in funding_group_section:
		award_id = extract_node_text(fg, "award-id")
		award_group_award_id.append(award_id)
	return award_group_award_id

@flatten
def award_group_principle_award_recipient(soup):
	"""
	Find the award group principle award recipient, one for each
	item found in the get_funding_group section
	"""
	award_group_principle_award_recipient = []
	funding_group_section = get_funding_group(soup)
	for fg in funding_group_section:
		principal_award_recipient_text = ""
		principal_award_recipient = extract_nodes(fg, "principal-award-recipient")
		try:
			institution = extract_node_text(principal_award_recipient[0], "institution")
			surname = extract_node_text(principal_award_recipient[0], "surname")
			given_names = extract_node_text(principal_award_recipient[0], "given-names")
			# Concatenate name and institution values if found
			#  while filtering out excess whitespace
			if(given_names):
				principal_award_recipient_text += given_names
			if(principal_award_recipient_text != ""):
				principal_award_recipient_text += " "
			if(surname):
				principal_award_recipient_text += surname
			if(institution and len(institution) > 1):
				if(principal_award_recipient_text != ""):
					principal_award_recipient_text += ", "
				principal_award_recipient_text += institution
		except IndexError:
			continue
		award_group_principle_award_recipient.append(principal_award_recipient_text)
	return award_group_principle_award_recipient

def funding_statement(soup):
	"""
	Find the funding statement (one expected)
	"""
	funding_statement = None
	funding_statement = extract_node_text(soup, "funding-statement")
	return funding_statement

def get_permissions_section(soup):
	"""
	Get the permissions section for populating
	copyright and license data
	"""
	permissions_section = None
	permissions_section = extract_nodes(soup, "permissions")
	return permissions_section

def copyright_statement(soup):
	"""
	Find the copyright statement
	"""
	copyright_statement = None
	try:
		permissions_section = get_permissions_section(soup)
		copyright_statement = extract_node_text(permissions_section[0], "copyright-statement")
	except(IndexError):
		return None
	return copyright_statement

def copyright_year(soup):
	"""
	Find the copyright year
	"""
	copyright_year = None
	try:
		permissions_section = get_permissions_section(soup)
		copyright_year = extract_node_text(permissions_section[0], "copyright-year")
	except(IndexError):
		return None
	try:
		return int(copyright_year)
	except TypeError:
		return copyright_year

def copyright_holder(soup):
	"""
	Find the copyright holder
	"""
	copyright_holder = None
	try:
		permissions_section = get_permissions_section(soup)
		copyright_holder = extract_node_text(permissions_section[0], "copyright-holder")
	except(IndexError):
		return None
	return copyright_holder

def get_license_section(soup):
	"""
	Find the license section, containing the
	license, license-url and license-type
	"""
	license_section = None
	try:
		permissions_section = get_permissions_section(soup)
		license_section = extract_nodes(permissions_section[0], "license")
	except(IndexError):
		return None
	return license_section

def license(soup):
	"""
	Find the license text
	"""
	license = None
	try:
		license_section = get_license_section(soup)
		license = extract_node_text(license_section[0], "license-p")
	except(IndexError):
		return None
	return license

def license_type(soup):
	"""
	Find the license type attribute of the license tag
	"""
	license_type = None
	try:
		license_section = get_license_section(soup)
		license_type = license_section[0]["license-type"]
	except(IndexError):
		return None
	return license_type

def license_url(soup):
	"""
	Find the license url attribute of the license tag
	"""
	license_url = None
	try:
		license_section = get_license_section(soup)
		license_url = license_section[0]["xlink:href"]
	except(IndexError):
		return None
	return license_url

@strippen
def ack(soup):
	"""
	Find the acknowledgements in the ack tag
	"""
	ack = None
	ack = extract_node_text(soup, "ack")
	return ack

@strippen
def conflict(soup):
	"""
	Find the conflict notes in footnote tag
	"""
	conflict = None
	try:
		conflict = extract_node_text(soup, "fn", attr = "fn-type", value = "conflict")
	except KeyError:
		return None
	return conflict