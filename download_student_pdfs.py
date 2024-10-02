import requests
import os 

folder_path = "student_pdfs"
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

def download_pdf(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as file:
        file.write(response.content)
    print(f"PDF downloaded successfully: {filename}")

# List of PDF URLs and filenames from the students' answer
# pdf_urls is a tuple of URL and filename
pdf_urls = [
    ("https://scholarships.gov.in/pdf/NMMSScheme.pdf", "NMMSScheme.pdf"),
    ("https://www.mygov.in/assets/pdf/pmrf_scheme_document.pdf", "pmrf_scheme_document.pdf"),
    ("https://scholarships.gov.in/pdf/NSS_Scheme.pdf", "NSS_Scheme.pdf"),
    ("https://scholarships.gov.in/pdf/CSS_Scheme.pdf", "CSS_Scheme.pdf"),
    ("https://scholarships.gov.in/pdf/PM_SCHEME_FOR_MINORITIES.pdf", "PM_SCHEME_FOR_MINORITIES.pdf"),
    ("https://scholarships.gov.in/pdf/N_O_S_S_SCHEME.pdf", "N_O_S_S_SCHEME.pdf"),
    ("https://scholarships.gov.in/pdf/N_O_S_S_SCHEME_OBC.pdf", "N_O_S_S_SCHEME_OBC.pdf"),
    ("https://scholarships.gov.in/pdf/NMMSScheme_Divyangjan.pdf", "NMMSScheme_Divyangjan.pdf"),
    ("https://ncert.nic.in/pdf/scholarship/NTSS_Scheme_2021.pdf", "NTSS_Scheme_2021.pdf"),
    ("https://scholarships.gov.in/pdf/CSS_SCHEME_SC.pdf", "CSS_SCHEME_SC.pdf"),
]


# Download PDFs
for url, filename in pdf_urls:
    # print (url, filename)
    download_pdf(url, os.path.join(folder_path, filename))
    # download_pdf(url, filename)
