#!/usr/bin/env python

"""
Download all the pdfs linked on a given webpage

Usage -

    python grab_pdfs.py url <path/to/directory>
        url is required
        path is optional. Path needs to be absolute
        will save in the current directory if no path is given
        will save in the current directory if given path does not exist

Requires - requests >= 1.0.4
           beautifulsoup >= 4.0.0

Download and install using
    
    pip install requests
    pip install beautifulsoup4
"""

__author__= 'elssar <elssar@altrawcode.com>'
__modifier__='subbu vincent <subbuvincent@stanford.edu>'
__license__= 'MIT'
__version__= '1.0.0'

from requests import get
from urllib.parse import urljoin
from os import path, getcwd
import html5lib
from bs4 import BeautifulSoup as soup
from sys import argv

def get_page(base_url):
    req= get(base_url)
    if req.status_code==200:
        return req.text
    raise Exception('Error {0}'.format(req.status_code))

def get_all_links(html):
    bs= soup(html, 'html5lib')
    links= bs.findAll('a', href=True)
    return links

def get_pdf(base_url, base_dir):
    html= get_page(base_url)
    links= get_all_links(html)
    if len(links)==0:
        raise Exception('No links found on the webpage')
    
    n_pdfs = 0
    n_links = len(links)
    #First count the number of PDFs linked on this page

    print("Total links found:", n_links)
    print("Now entering search for PDF docs..")

    #for link in links:
        #print("link:",link)
        #print("link exten:", link['href'][-4:])
        #if link['href'][-4:]=='.pdf':
        #    n_pdfs+= 1
            
    #print("FOUND: {0} pdfs".format(n_pdfs))

    #n_pdfs = 0
    #now dump the pdfs into files

    for link in links:
        print("Checking link:",link['href'])

        skip_link = False 

        if link['href'].startswith("mailto:"):
            skip_link = True
        elif link['href'].startswith("javascript:"):
            skip_link = True

        if skip_link == False:
            try:
                content= get(urljoin(base_url, link['href']))
                if content.status_code==200 and content.headers['content-type']=='application/pdf':
                    print("Found pdf!..")
                    n_pdfs+= 1   
                    pdf_file = link['href'].rsplit('/', 1)[-1]
                    print("Saving pdf file:", pdf_file)
                    with open(path.join(base_dir, pdf_file), 'wb') as pdf:
                        pdf.write(content.content)
            except:
                pass
        else: 
            print("Skipping link..")
   
    if n_pdfs==0:
        raise Exception('No pdfs found on the page')
    print ("COMPLETED: {0} pdfs downloaded out of {1} links and saved in {2}".format(n_pdfs, n_links, base_dir))


if __name__=='__main__':
    if len(argv) not in (2, 3):
        print ('Error! Invalid arguments')
        print (__doc__)
        exit(-1)
    arg= ''
    
    print("Subbu Vincent, code to download all PDFs from webpage(s)... starting..")

    url= argv[1]
    if len(argv)==3:
        arg= argv[2]
    base_dir= [getcwd(), arg][path.isdir(arg)]
    
    try:
        print("############################################")
        print("Trying this URL:", url, "Saving here:", base_dir)
        print("############################################")
        get_pdf(url,base_dir)
    except Exception as e:
        print (e)
        exit(-1)