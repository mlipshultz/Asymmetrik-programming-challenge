import re
import sys

#The business card parser class will be doing all of the heavy lifting in figuring out
#the different pieces of contact information
class BusinessCardParser:
	#We will define a series of private helper functions for parsing out the pieces of contact information.
	def __parseName(self, document):
		matches = []
		#We will have a list of words which will disqaulify a word from being a name.
		#These will either be job title words, or words generally appearing in a company name.
		list_of_disqualif_words = ['software', 'developer', 'analytic', 'tech', 'technology', 'engineer',
		'ltd', 'llc', 'technologies', 'analyst', 'solutions', 'cloud', 'computing']
		#This list could be added to with user input. As users find conflicts they could determine what to
		#add to this list. I left it with some basic words for the sake of time.

		for line in document:
			#Here we want to match any line with 2 or more capitalized words (which can have hyphens)
			regex = re.search(r'^[A-Z][a-z\-]+(\s[A-Z][a-z\-]+)+', line)
			if regex != None:
				matches.append(regex.group(0))

		matches_to_remove = set()
		if not matches:
			return "No name found"
		elif len(matches) == 1:
			return matches[0]
		else:
			for match in matches:
				#We want to look at each word in the matches we found to see if we can find a
				#disqualifying word.
				for name in match.split(' '):
					if name.lower() in list_of_disqualif_words:
						matches_to_remove.add(match)

		for item in matches_to_remove:
			matches.remove(item)

		#This case means we filtered out all potentional matches, we may still want to return a value
		#so the behavior of this could be changed to return when the list has one entry left
		if not matches:
			return "No name found"
		else:
			return matches[0]

	def __parsePhoneNumber(self, document):		
		#If we find a match on this regular expression, we have a possible phone number.
		#It is possible that we find two possible numbers, so we then need to narrow down 
		#to the correct phone number if we do.
		matches = []
		for line in document:
			#We search for something that looks like a phone number using the below regex.
			regex = re.search(r'(\d?).*(\d{3}).*(\d{3}).*(\d{4}).*', line)
			if regex != None:
				matches.append(line)

		if not matches:
			return "No Phone number found"

		#If we have only a single match, take just the digits from that line
		elif len(matches) == 1:
			digits = [character for character in matches[0] if character.isdigit()]
			return ''.join(digits)

		else:		
			#If we have more than one match to the regular expression, we will need to find which
			#is the line we are looking for.
			#By using the characters in "telephone", we can get a good idea of if this is the phone number
			#that we are looking for.
			chars_to_look_for = "telphon"
			max_matches = 0
			most_matched_line = ''
			for match in matches:
				current_matches = 0
				match = match.lower()
				for char in chars_to_look_for:
					if char in match:
						current_matches += 1
				
				if current_matches >= max_matches:
					max_matches = current_matches
					most_matched_line = match

			#We return the digits from the line with the most matching characters to "telephone"
			digits = [character for character in most_matched_line if character.isdigit()]
			return ''.join(digits)
			

	def __parseEmail(self, document):
		for line in document:
			#We will search for a line which any valid characters or dots, an @ sign, more valid characters,
			# a dot, followed by more valid characters.
			regex = re.search(r"[\w\.]+@\w+\.\w+", line)
			if regex != None:
				return regex.group(0)

		#Error case, we return no email if we could not find a anything with our regex.
		return "No email address found"

	def getContactInfo(self, document):
		#First we remove leading and trailing whitespaces. This will remove new line characters.
		document = [line.strip() for line in document]
		phone_number = self.__parsePhoneNumber(document)
		email_address = self.__parseEmail(document)
		name = self.__parseName(document)
		return ContactInfo(name, phone_number, email_address)

#The contact info class will contain a name, phone number, and email address
#and provide getters to those variables.
class ContactInfo:
	def __init__(self, name, phone_number, email_address):
		self.name = name
		self.phone_number = phone_number
		self.email_address = email_address

	def getName(self):
		return self.name

	def getPhoneNumber(self):
		return self.phone_number

	def getEmailAddress(self):
		return self.email_address


def main():
	document = []
	if len(sys.argv) != 2:
		print('Please use 1 input argument which is the text file you would like to parse')
		return
	else:
		try:
			with open(sys.argv[1], 'r') as infile:
				document = infile.readlines()
		except:
			print("Failed to open file: " + sys.argv[1])
			print("Please provide a valid file name")
			return

	parser = BusinessCardParser()	
	contact_info = parser.getContactInfo(document)
	print("Name: {}".format(contact_info.getName()))
	print("Phone: {}".format(contact_info.getPhoneNumber()))
	print("Email: {}".format(contact_info.getEmailAddress()))


if __name__ == "__main__":
	main()