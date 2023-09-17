from pathlib import Path
from typing import IO, Any, Dict, Union

import requests
from bs4 import BeautifulSoup, element
from PyPDF2 import PdfReader
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def extract_data(data: Dict[str, Any]) -> Dict[str, str]:
    cv = load_pdf(data["cv"])
    linkedin_data = extract_data_from_url(data["url"])

    return {"cv": cv} | linkedin_data | {"other": data["other"]}


def load_pdf(pdf: Union[str, IO, Path]) -> str:
    if pdf:
        pdf_reader = PdfReader(pdf)
        return "CV/RESUME: " + "\n".join(
            page.extract_text() for page in pdf_reader.pages
        )
    else:
        return "RESUME: Not provided"


def extract_data_from_url(url: str) -> Dict[str, Any]:
    html = requests.get(url).text
    soup = BeautifulSoup(html, features="html.parser")

    job_title = soup.find("title").get_text().split("|")[0]
    job_description = soup.find(
        "div", {"class": "description__text"}
    ).get_text()

    company_info = extract_company_info_from_job_html(soup)

    return {
        "job_title": "JOB TITLE: " + job_title,
        "job_description": "JOB DESCRIPTION: " + job_description,
        "company_info": "COMPANY INFO: " + company_info,
    }


def extract_company_info_from_job_html(soup: BeautifulSoup) -> element.Tag:
    link_company = soup.find("a", {"class": "sub-nav-cta__optional-url"}).get(
        "href"
    )

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    driver.get(link_company)

    # Obtenez le contenu de la page après que JavaScript ait pu se charger
    page_source = driver.page_source

    # Analysez le contenu HTML avec BeautifulSoup
    soup = BeautifulSoup(page_source, "html.parser")
    driver.quit()

    company_info = (
        soup.find(
            "div", {"class": "core-section-container__content break-words"}
        )
        .find("p", class_="text-color-text")
        .get_text()
    )

    return company_info
