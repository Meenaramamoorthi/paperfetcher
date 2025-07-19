# fetch.py

from typing import List, Dict
import requests
import xml.etree.ElementTree as ET
import re
import logging

logger = logging.getLogger(__name__)
HEADERS = {"User-Agent": "paperfetcher/1.0"}


def search_pubmed(query: str) -> List[str]:
    logger.info("Searching PubMed with query: %s", query)
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": 100
    }
    resp = requests.get(url, params=params, headers=HEADERS)
    resp.raise_for_status()
    ids = resp.json()["esearchresult"].get("idlist", [])
    return ids


def fetch_details(pubmed_ids: List[str]) -> List[Dict]:
    logger.info("Fetching details for %d PubMed IDs", len(pubmed_ids))
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        "db": "pubmed",
        "id": ",".join(pubmed_ids),
        "retmode": "xml"
    }
    resp = requests.get(url, params=params, headers=HEADERS)
    resp.raise_for_status()
    root = ET.fromstring(resp.text)
    return parse_articles(root)


def parse_articles(root: ET.Element) -> List[Dict]:
    papers = []
    for article in root.findall(".//PubmedArticle"):
        try:
            pmid = article.findtext(".//PMID")
            title = article.findtext(".//ArticleTitle")
            pub_date = article.findtext(".//PubDate/Year") or "N/A"

            authors = article.findall(".//Author")
            non_academic_authors = []
            company_affiliations = []
            email = None

            for author in authors:
                affil = author.findtext("AffiliationInfo/Affiliation") or ""
                name = f"{author.findtext('ForeName', '')} {author.findtext('LastName', '')}".strip()

                if is_industry_affiliation(affil):
                    non_academic_authors.append(name)
                    company_affiliations.append(affil)

                if not email and "@" in affil:
                    email_match = re.search(r"[\w\.-]+@[\w\.-]+", affil)
                    if email_match:
                        email = email_match.group(0)

            if non_academic_authors:
                papers.append({
                    "PubmedID": pmid,
                    "Title": title,
                    "Publication Date": pub_date,
                    "Non-academic Author(s)": "; ".join(non_academic_authors),
                    "Company Affiliation(s)": "; ".join(set(company_affiliations)),
                    "Corresponding Author Email": email or "N/A"
                })
        except Exception as e:
            logger.warning("Skipping paper due to error: %s", e)
            continue
    return papers


def is_industry_affiliation(affil: str) -> bool:
    academic_keywords = ["university", "college", "institute", "school", "hospital", "center"]
    affil_lower = affil.lower()
    return not any(kw in affil_lower for kw in academic_keywords)
