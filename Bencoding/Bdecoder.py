'''
BitTorrent metainfo file decoder module

This module is developed based on section 7, "Metainfo File Structure", of
the Bittorrent Protocol Specification v1.0 which is available at:

	https://wiki.theory.org/BitTorrentSpecification#Metainfo_File_Structure
'''

def __getUpto(stream, s):
	'''
	get contents upto character s whereas s is discarded
	'''
	out = []
	c = stream.read(1)
	while(s != c and 0 != len(c)):
		out.append(c)
		c = stream.read(1)
	if (s != c and s is not None):
		raise Exception('Invalid format: expected \'%s\' not found' % (s,))
	return out

def __getInt(stream):
	'''
	parse contents as int
	'''
	s = ''.join(v for v in __getUpto(stream, 'e'))
	if ('0' == s[0] and '0' != s):
		raise Exception('Invalid format: zeroes padded integer')
	try:
		return int(s)
	except Exception as ex:
		raise Exception('Invalid format: integer expected')

def __parseUpto(stream, s=None):
	'''
	parse contents upto character s whereas s is discarded
	'''
	out = []
	c = stream.read(1)
	while(s != c and 0 != len(c)):
		# dictionary
		if 'd' == c:
			out.append(__parseDict(stream))
		# list
		elif 'l' == c:
			out.append(__parseList(stream))
		# integer
		elif 'i' == c:
			out.append(__getInt(stream))
		# byte string
		elif c in '0123456789':
			i = int(c + ''.join(v for v in __getUpto(stream, ':')))
			out.append(stream.read(i))
		else:
			raise Exception('Invalid format: unknown identifier')
		c = stream.read(1)
	if (s != c and s is not None):
		raise Exception('Invalid format: incomplete structure')
	return out

def __parseList(stream):
	'''
	parse contents as list
	'''
	return __parseUpto(stream, 'e')

def __parseDict(stream):
	'''
	parse contents as dictionary
	'''
	l = __parseList(stream)
	if (0 != len(l) % 2):
		raise Exception('Invalid format: dangling dictionary key')
	d = dict(zip(l[0::2], l[1::2]))
	return d

def __validate(data):
	'''
	validate parsed BitTorrent metainfo data
	'''
	if (1 < len(data)):
		raise Exception('Invalid format: sequential data at top level')
	minfo = data[0]
	if 'announce' not in minfo:
		raise Exception('Insufficient info: \'announce\'')
	if 'info' not in minfo:
		raise Exception('Insufficient info: \'info\'')
	if 'name' not in minfo['info']:
		raise Exception('Insufficient info: \'info->name\'')
	# multiple file mode
	if 'files' in minfo['info']:
		for f in minfo['info']['files']:
			if 'path' not in f:
				raise Exception('Insufficient info: \'info->files->path\'')
			if 'length' not in f:
				raise Exception('Insufficient info: \'info->files->length\'')
	# single file mode
	else:
		if 'length' not in minfo['info']:
			raise Exception('Insufficient info: \'info->length\'')
	return minfo

def parse(stream):
	'''
	parse raw data from stream
	'''
	return __validate(__parseUpto(stream))
