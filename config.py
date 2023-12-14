"""
Simple configuration file which provides information to create CrossRef deposit files
from ADS JATS records
"""

import re

# name and email of the publisher registering these records in CrossRef
publisher = 'Publisher via the NASA Astrophysics Data System'
email =	'adshelp@cfa.harvard.edu'

# use the ISSN found in the source document
issn = ''

# these is the SI prefix that ADS can use for registering in CrossRef
doi_prefix = '10.5479/ADS/bib'
ads_prefix = 'https://ui.adsabs.harvard.edu/abs'

# create a DOI from the bibcode
def doi_func(bibcode):
    shortbib = re.sub(r'\.+','.',bibcode)
    return doi_prefix + '/' + shortbib

def uri_func(bibcode):
    escaped = bibcode.replace('&','%26')
    return ads_prefix + '/' + escaped


