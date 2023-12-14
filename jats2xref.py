"""
Uses the JATS to CrossRef deposit schema transform
(https://github.com/CrossRef/jats-crossref-xslt/)
to reformat JATS metadata documents into CrossRef deposit XML
"""
import lxml.etree as ET
import sys, os
from datetime import datetime
import config

publisher = ET.XSLT.strparam(config.publisher)
email = ET.XSLT.strparam(config.email)
issn = ''
if hasattr(config, 'issn'):
    issn = config.issn
issn = ET.XSLT.strparam(issn)

xsl_filename = sys.argv[1]
xml_filename = sys.argv[2]
if xsl_filename and os.path.exists(xsl_filename) and \
   xml_filename and os.path.exists(xml_filename):
    pass
else:
    print("Usage: {0} xsl_file xml_file".format(sys.argv[0]), file=sys.stderr)
    sys.exit(1)

now = datetime.now()
ts = ET.XSLT.strparam(now.strftime("%Y%m%d%H%M%S"))

xslt = ET.parse(xsl_filename)
transform = ET.XSLT(xslt)
dom = ET.parse(xml_filename)

bibcode = doi = uri = ''

# now compute DOI and URI from the bibcode, if found
# (could be modified to specify both on the command line)
# bibcode is encoded in ADS JATS output as
#    '<article-id pub-id-type="archive">XXX</article-id>'
try:
    bibcode = dom.xpath('//article-id[@pub-id-type="archive"]').pop().text
    if hasattr(config, 'doi_func'):
        doi = config.doi_func(bibcode)
    if hasattr(config, 'uri_func'):
        uri = config.uri_func(bibcode)
except IndexError:
    # assume DOI and URL are already specified in input XML
    pass

doi = ET.XSLT.strparam(doi)
uri = ET.XSLT.strparam(uri)

newdom = transform(dom, timestamp=ts, email=email, registrant=publisher, issn=issn, doi=doi, uri=uri)
print(newdom)

# print(ET.tostring(newdom, pretty_print=True))
