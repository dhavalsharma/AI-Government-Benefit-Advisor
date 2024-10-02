import os
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
#download list of pdf which are under the Specification hyperlink on page https://scholarships.gov.in/All-Scholarships
# and save them in a folder named "student_pdfs" in the current directory.
# The filenames should be the same as the last part of the URL.
# For example, if the URL is https://scholarships.gov.in/pdf/NMMSScheme.pdf, the filename should be NMMSScheme.pdf.
# The download_pdf function should be used to download the PDFs.
def download_pdf(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as file:
        file.write(response.content)
    print(f"PDF downloaded successfully: {filename}")

def create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def crawl_website(url, folder_path, pdf_base_url="https://scholarships.gov.in/public"):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        for link in soup.find_all('a'):
            #and link text is Specifications then download the pdf
            # add above condition to below if condition
            if link.get('href') and link.get('href').endswith('.pdf') and link.text == "Specifications":
                relative_url = link.get('href')
                #https://scholarships.gov.in/public/schemeGuidelines/DEPDGuidelines_1.pdf
                if relative_url.startswith('/'):
                    #use urljoin to join the base url and relative url
                    pdf_url = urljoin(pdf_base_url, relative_url)
                else:
                    pdf_url = relative_url
                pdf_filename = pdf_url.split('/')[-1]
                download_pdf(pdf_url, os.path.join(folder_path, pdf_filename))

def download_student_folder():
    folder_path = "student_pdfs"
    create_folder(folder_path)
    
    starting_url = "https://scholarships.gov.in/All-Scholarships"
    crawl_website(starting_url, folder_path)
download_student_folder()
