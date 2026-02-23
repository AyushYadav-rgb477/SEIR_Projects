SEIR Project (Search Engine & Information Retrieval)

This folder contains two Python programs created as part of the Search Engine and Information Retrieval (SEIR) course assignments.
The project demonstrates basic ideas used in search engines such as web page extraction and document similarity detection.

1. Web Page Scraper (scraper.py)

This program takes a URL from the command line and fetches the webpage.

What it does

a) Downloads the webpage
b) Prints the page title
c) Extracts readable body text (removes HTML, scripts and styles)
d)Lists all links present on the page

Run
python scraper.py <URL>


2. Document Similarity using SimHash (simhash.py)

This program compares two webpages and checks how similar their content is.

Working

a) Downloads both webpages
b) Removes HTML tags
c) Splits text into words and counts frequency
d) Converts each word into a 64-bit hash
e) Creates a document fingerprint (SimHash)
f) Compares fingerprints using Hamming similarity

Output

The program prints how many bits are common out of 64.

More common bits → pages are more similar.

Run
python simhash.py <URL1> <URL2>

Example:

python simhash.py https://site1.com https://site2.com
Technologies Used

Python 3

Requests
BeautifulSoup4
Regular Expressions
Collections (Counter)


Purpose

This project helps in understanding:

how search engines extract information from webpages
how duplicate or similar webpages are detected
