#!/usr/bin/env python
# -*- coding: utf-8 -*-

if '__main__' == __name__:
	from Bencoding import Bdecoder
	import sys
	from pprint import pprint
	if (1 < len(sys.argv)):
		for arg in sys.argv[1:]:
			with open(arg, 'rb') as f:
				# using StringIO may boost performance
				pprint(Bdecoder.parse(f))
			print('')
	else:
		print("\nusage: %s FILE [ FILE ... ]\n" % (sys.argv[0],))
