from langchain.tools import tool 
import requests
from dotenv import load_dotenv
import os
from tavily import TavilyClient
from rich import print
from bs4 import BeautifulSoup
from readability import Document
import trafilatura
import re 

#load environment variables from .env file
load_dotenv()

#fetch tavily api key from environment variable and initialize client
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

#For OpenWebNinja, I don't create a client. I just store the API key and use it in request headers.
OPENWEBNINJA_API_KEY = os.getenv("OPENWEBNINJA_API_KEY")






#Tool1 search_jobs - Uses JSearch API to find live job opportunities based on a query.

@tool
def search_jobs(query: str) -> str:
    """
    Search live job opportunities using JSearch API.
    Returns clean structured job results.
    """
    print("search_jobs tool called")
    print(f"Query: {query}")

    headers = {
        "X-API-Key": OPENWEBNINJA_API_KEY
    }

    try:
        response = requests.get(
            "https://api.openwebninja.com/jsearch/search-v2",
            headers=headers,
            params={"query": query},
            timeout=15
        )

        response.raise_for_status()

        results = response.json()

        # OpenWebNinja JSearch structure
        jobs = results.get("data", {}).get("jobs", [])

        if not jobs:
            return "No jobs found."

        out = []

        # Return top 3 jobs
        for job in jobs[:5]:

            title = job.get("job_title", "N/A")

            company = job.get("employer_name", "N/A")

            location = job.get(
                "job_location",
                "N/A"
            )

            employment_type = job.get(
                "job_employment_type",
                "N/A"
            )

            posted = job.get(
                "job_posted_at",
                "N/A"
            )

            remote = job.get(
                "job_is_remote",
                "N/A"
            )

            salary = (
                job.get("job_salary_string") 
                or "Not Available"
            )

            apply_url = (
                job.get("job_apply_link")
                or job.get("job_google_link")
                or "N/A"
            )

            description = job.get(
                "job_description",
                "No description available."
            )

            # Clean description
            description_summary = (
                description
                .replace("\n", " ")
                .replace("\r", " ")
                .strip()
            )[:1500]

            out.append(
                f"""
Job Title: {title}

Company: {company}

Location: {location}

Employment Type: {employment_type}

Posted: {posted}

Remote: {remote}

Salary: {salary}

Apply URL:
{apply_url}

Description Summary:
{description_summary}
"""
            )

        return "\n\n========================\n\n".join(out)

    except requests.exceptions.Timeout:
        return "Request timed out while searching jobs."

    except requests.exceptions.HTTPError as e:
        return f"HTTP error occurred: {str(e)}"

    except Exception as e:
        return f"Error searching jobs: {str(e)}"

   
    
#tool2 extract_skills - Scrapes a job posting URL and extracts clean readable content for skill analysis using multiple strategies.
@tool
def extract_skills(url: str) -> str:
    """
    Scrape a job posting URL and extract clean readable content
    for skill analysis.

    Uses multiple extraction strategies:
    1. Trafilatura (best for article-style content)
    2. Readability-LXML (extracts main content)
    3. Full-page BeautifulSoup fallback
    """

    print("extract_skills tool called")
    print(f"URL: {url}")

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/",
    }

    try:

        # ────────────────────────────────────────────────
        # Fetch job posting webpage
        # ────────────────────────────────────────────────
        response = requests.get(
            url,
            headers=headers,
            timeout=15
        )

        response.raise_for_status()

        html = response.text

        # ────────────────────────────────────────────────
        # Strategy 1 → Trafilatura
        # Best for extracting clean article/job content
        # ────────────────────────────────────────────────
        extracted = trafilatura.extract(
            html,
            include_comments=False,
            include_tables=False
        )

        if extracted and len(extracted.strip()) > 200:
            cleaned = re.sub(r"\s+", " ", extracted)
            return cleaned[:3000]

        # ────────────────────────────────────────────────
        # Strategy 2 → Readability-LXML
        # Extracts the main content from the webpage
        # ────────────────────────────────────────────────
        doc = Document(html)
        clean_html = doc.summary()

        soup = BeautifulSoup(
            clean_html,
            "html.parser"
        )

        # Remove unwanted HTML elements
        for tag in soup([
            "script",
            "style",
            "nav",
            "footer",
            "header",
            "aside",
            "form"
        ]):
            tag.decompose()

        text = soup.get_text(
            separator=" ",
            strip=True
        )

        if text and len(text.strip()) > 200:
            cleaned = re.sub(r"\s+", " ", text)
            return cleaned[:3000]

        # ────────────────────────────────────────────────
        # Strategy 3 → Full Page BeautifulSoup Fallback
        # Last option if other extraction methods fail
        # ────────────────────────────────────────────────
        soup = BeautifulSoup(
            html,
            "html.parser"
        )

        # Remove unnecessary page elements
        for tag in soup([
            "script",
            "style",
            "nav",
            "footer",
            "header",
            "aside",
            "form"
        ]):
            tag.decompose()

        text = soup.get_text(
            separator=" ",
            strip=True
        )

        cleaned = re.sub(
            r"\s+",
            " ",
            text
        )

        if cleaned:
            return cleaned[:3000]

        return "Could not extract meaningful content from the job posting."

    # ────────────────────────────────────────────────
    # Error Handling
    # ────────────────────────────────────────────────

    except requests.exceptions.Timeout:
        return "Request timed out while scraping the job URL."

    except requests.exceptions.HTTPError as e:
        return f"HTTP error occurred: {str(e)}"

    except Exception as e:
        return f"Could not extract skills from URL: {str(e)}"
    


# TOOL - 3

@tool
def salary_research(
    job_title: str,
    location: str,
    years_of_experience: str
) -> str:
    """
    Fetch salary insights for a given job title,
    location and years of experience using
    OpenWebNinja Job Salary API.
    """

    print("salary_research tool called")
    print(f"Job Title: {job_title}")
    print(f"Location: {location}")
    print(f"Experience: {years_of_experience}")

    headers = {
        "X-API-Key": OPENWEBNINJA_API_KEY
    }

    try:

        response = requests.get(
            "https://api.openwebninja.com/job-salary-data/job-salary",
            headers=headers,
            params={
                "job_title": job_title,
                "location": location,
                "location_type": "CITY",
                "years_of_experience": years_of_experience
            },
            timeout=15
        )

        response.raise_for_status()

        data = response.json()

        salary_data = data.get("data", [])

        if not salary_data:
            return (
                f"No salary information found for "
                f"{job_title} in {location}."
            )

        salary = salary_data[0]

        return f"""
Role: {salary.get('job_title', 'N/A')}

Location: {salary.get('location', 'N/A')}

Median Salary:
{salary.get('median_salary', 'N/A')}

Salary Range:
{salary.get('min_salary', 'N/A')} - {salary.get('max_salary', 'N/A')}

Base Salary Range:
{salary.get('min_base_salary', 'N/A')} - {salary.get('max_base_salary', 'N/A')}

Additional Compensation:
{salary.get('median_additional_pay', 'N/A')}

Currency:
{salary.get('salary_currency', 'N/A')}

Salary Period:
{salary.get('salary_period', 'N/A')}

Confidence:
{salary.get('confidence', 'N/A')}

Source:
{salary.get('publisher_name', 'N/A')}
"""

    except requests.exceptions.Timeout:
        return "Salary API request timed out."

    except requests.exceptions.HTTPError as e:
        return f"HTTP error occurred: {str(e)}"

    except Exception as e:
        return f"Could not fetch salary data: {str(e)}"
    
    
#TOOL - 4 

@tool
def find_courses(skill: str) -> str:
    """
    Search for the best courses, certifications,
    tutorials and learning resources for a skill.

    Returns:
    - Course recommendations
    - Certification resources
    - Tutorial links
    - Learning materials
    """
    print("find_courses tool called")
    print(f"Skill Input: {skill}")

    try:

        # ────────────────────────────────────────────────
        # Build search query
        # ────────────────────────────────────────────────
        query = (
            f"Best {skill} courses certifications "
            f"tutorials learning roadmap"
        )

        # ────────────────────────────────────────────────
        # Search learning resources using Tavily API
        # ────────────────────────────────────────────────
        results = tavily.search(
            query=query,
            max_results=5
        )

        out = []

        # ────────────────────────────────────────────────
        # Format search results
        # ────────────────────────────────────────────────
        for r in results["results"]:

            out.append(
                f"Title: {r['title']}\n"
                f"URL: {r['url']}\n"
                f"Snippet: {r['content'][:300]}\n"
            )

        return "\n--------------------\n".join(out)

    # ────────────────────────────────────────────────
    # Error Handling
    # ────────────────────────────────────────────────

    except Exception as e:
        return f"Could not find learning resources: {str(e)}"