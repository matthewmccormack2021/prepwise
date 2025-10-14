"""
Web scraping service for extracting job information from job posting URLs.
"""

import requests
from bs4 import BeautifulSoup
import html2text
import re
from typing import Dict, Optional
from loguru import logger


class JobScraper:
    """Web scraper for extracting job information from various job posting sites."""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.html_converter = html2text.HTML2Text()
        self.html_converter.ignore_links = False
        self.html_converter.ignore_images = True
        
    def extract_job_info(self, url: str) -> Dict[str, Optional[str]]:
        """
        Extract job title and description from a job posting URL.
        
        Args:
            url: The URL of the job posting
            
        Returns:
            Dictionary containing 'title', 'description', and 'company' if found
        """
        try:
            logger.info(f"Scraping job posting from: {url}")
            
            # Validate URL
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
                
            # Fetch the webpage
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract job information based on common patterns
            job_info = {
                'title': self._extract_title(soup, url),
                'description': self._extract_description(soup, url),
                'company': self._extract_company(soup, url),
                'url': url
            }
            
            logger.info(f"Successfully extracted job info: {job_info['title']}")
            return job_info
            
        except requests.RequestException as e:
            logger.error(f"Failed to fetch URL {url}: {str(e)}")
            return {'error': f'Failed to fetch URL: {str(e)}'}
        except Exception as e:
            logger.error(f"Error scraping {url}: {str(e)}")
            return {'error': f'Error scraping job posting: {str(e)}'}
    
    def _extract_title(self, soup: BeautifulSoup, url: str) -> Optional[str]:
        """Extract job title using various selectors."""
        # Common selectors for job titles
        title_selectors = [
            'h1.job-title',
            'h1[data-testid="job-title"]',
            'h1.jobTitle',
            '.job-title h1',
            '.job-header h1',
            'h1',
            '.title',
            '[data-testid="job-title"]',
            '.jobTitle',
            'h2.job-title',
            'h3.job-title'
        ]
        
        for selector in title_selectors:
            element = soup.select_one(selector)
            if element:
                title = element.get_text(strip=True)
                if title and len(title) > 3:  # Basic validation
                    return title
        
        # Try to extract from meta tags
        meta_title = soup.find('meta', property='og:title')
        if meta_title and meta_title.get('content'):
            return meta_title['content'].strip()
            
        # Try page title
        title_tag = soup.find('title')
        if title_tag:
            title_text = title_tag.get_text(strip=True)
            # Clean up common title patterns
            title_text = re.sub(r'\s*-\s*(Indeed|LinkedIn|Glassdoor|Monster|ZipRecruiter).*', '', title_text)
            if title_text and len(title_text) > 3:
                return title_text
                
        return None
    
    def _extract_description(self, soup: BeautifulSoup, url: str) -> Optional[str]:
        """Extract job description using various selectors."""
        # Common selectors for job descriptions
        desc_selectors = [
            '.job-description',
            '.jobDescription',
            '[data-testid="job-description"]',
            '.job-details',
            '.job-content',
            '.description',
            '.job-summary',
            '.job-body',
            '.job-requirements',
            '.job-responsibilities',
            '.description-content',
            '.job-post-description'
        ]
        
        description_text = None
        
        for selector in desc_selectors:
            element = soup.select_one(selector)
            if element:
                # Remove script and style elements
                for script in element(["script", "style"]):
                    script.decompose()
                
                # Convert to text
                description_text = self.html_converter.handle(str(element)).strip()
                if description_text and len(description_text) > 100:  # Basic validation
                    break
        
        # If no specific selector worked, try to find large text blocks
        if not description_text:
            # Look for divs with lots of text content
            divs = soup.find_all('div')
            for div in divs:
                text_content = div.get_text(strip=True)
                if len(text_content) > 200 and self._looks_like_job_description(text_content):
                    description_text = text_content
                    break
        
        # Clean up the description
        if description_text:
            description_text = re.sub(r'\n\s*\n', '\n\n', description_text)  # Normalize line breaks
            description_text = re.sub(r'[ \t]+', ' ', description_text)  # Normalize spaces
            return description_text[:5000]  # Limit length
            
        return None
    
    def _extract_company(self, soup: BeautifulSoup, url: str) -> Optional[str]:
        """Extract company name using various selectors."""
        # Common selectors for company names
        company_selectors = [
            '.company-name',
            '.companyName',
            '[data-testid="company-name"]',
            '.employer-name',
            '.job-company',
            '.company',
            '.employer',
            '.company-link',
            'a[data-testid="company-name"]'
        ]
        
        for selector in company_selectors:
            element = soup.select_one(selector)
            if element:
                company = element.get_text(strip=True)
                if company and len(company) > 1:
                    return company
        
        # Try to extract from meta tags
        meta_company = soup.find('meta', property='og:site_name')
        if meta_company and meta_company.get('content'):
            return meta_company['content'].strip()
            
        return None
    
    def _looks_like_job_description(self, text: str) -> bool:
        """Check if text looks like a job description."""
        job_keywords = [
            'responsibilities', 'requirements', 'qualifications', 'experience',
            'skills', 'education', 'degree', 'years of experience', 'salary',
            'benefits', 'full-time', 'part-time', 'remote', 'on-site',
            'candidate', 'position', 'role', 'team', 'department'
        ]
        
        text_lower = text.lower()
        keyword_count = sum(1 for keyword in job_keywords if keyword in text_lower)
        
        # If we find multiple job-related keywords, it's likely a job description
        return keyword_count >= 3


# Global scraper instance
job_scraper = JobScraper()


def scrape_job_posting(url: str) -> Dict[str, Optional[str]]:
    """
    Convenience function to scrape job information from a URL.
    
    Args:
        url: The URL of the job posting
        
    Returns:
        Dictionary containing job information or error details
    """
    return job_scraper.extract_job_info(url)
