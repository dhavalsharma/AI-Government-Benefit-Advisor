import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def create_folder(folder_path):
    """
    Create a folder if it doesn't already exist.
    
    Args:
        folder_path (str): The path to the folder to create.
    """
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def download_pdf(pdf_url, save_path):
    """
    Download a PDF from a given URL and save it to a specified path.
    
    Args:
        pdf_url (str): The URL of the PDF to download.
        save_path (str): The path to save the downloaded PDF.
    """
    response = requests.get(pdf_url)
    with open(save_path, 'wb') as f:
        f.write(response.content)

def crawl_website(starting_url, folder_path):
    """
    Crawl a website starting from a given URL to find and download PDFs.
    
    Args:
        starting_url (str): The URL to start crawling from.
        folder_path (str): The path to the folder to save downloaded PDFs.
    """
    response = requests.get(starting_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all links on the page
    for link in soup.find_all('a'):
        relative_url = link.get('href')
        if relative_url and relative_url.endswith('.pdf'):
            # Check if the URL is relative or absolute
            if relative_url.startswith('/'):
                # Use urljoin to join the base URL and relative URL
                pdf_url = urljoin(starting_url, relative_url)
            else:
                pdf_url = relative_url
            pdf_filename = pdf_url.split('/')[-1]
            download_pdf(pdf_url, os.path.join(folder_path, pdf_filename))

def download_student_folder():
    """
    Download all student PDFs from the scholarships website.
    """
    folder_path = "student_pdfs"
    create_folder(folder_path)
    
    starting_url = "https://scholarships.gov.in/All-Scholarships"
    crawl_website(starting_url, folder_path)

# Start the download process
download_student_folder()