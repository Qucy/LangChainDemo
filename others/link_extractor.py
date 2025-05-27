import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time # To add a small delay between requests

def get_links_from_url(current_url, base_domain_path):
    """Fetches and parses a URL, returning all valid sub-links found on that page."""
    links_on_page = set()
    try:
        # Add a small delay to be polite to the server
        time.sleep(0.5) 
        response = requests.get(current_url, timeout=10) # Added timeout
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        parsed_base_url = urlparse(base_domain_path) # The original base URL for comparison

        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            absolute_url = urljoin(current_url, href) # Join with current_url being processed
            parsed_absolute_url = urlparse(absolute_url)

            # Clean up the URL (remove fragment and trailing slash for consistent comparison)
            cleaned_url = parsed_absolute_url._replace(fragment="").geturl()
            if cleaned_url.endswith('/'):
                cleaned_url = cleaned_url[:-1]

            # Check if the link is under the same domain and starts with the same base path
            if parsed_absolute_url.netloc == parsed_base_url.netloc and \
               parsed_absolute_url.path.startswith(parsed_base_url.path):
                links_on_page.add(cleaned_url)
                
    except requests.exceptions.Timeout:
        print(f"Timeout while fetching URL {current_url}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {current_url}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while processing {current_url}: {e}")
        
    return list(links_on_page)

def crawl_site_dfs(start_url):
    """Performs a Depth-First Search crawl starting from start_url to find all sub-links."""
    all_found_links = set() # To store all unique links found during the crawl
    to_visit_stack = [start_url.rstrip('/')] # Stack for DFS, remove trailing slash for consistency
    visited_urls = set() # To keep track of visited URLs

    # The base domain and path to constrain the crawl
    parsed_start_url = urlparse(start_url)
    base_domain_path = f"{parsed_start_url.scheme}://{parsed_start_url.netloc}{parsed_start_url.path.rstrip('/')}"

    max_links_to_find = 100 # Safety break to prevent excessively long crawls

    while to_visit_stack and len(all_found_links) < max_links_to_find:
        current_url = to_visit_stack.pop() # Get the next URL to visit (DFS)

        if current_url in visited_urls:
            continue
        
        print(f"Visiting: {current_url}")
        visited_urls.add(current_url)
        all_found_links.add(current_url) # Add the visited URL itself to the list of found links

        new_links = get_links_from_url(current_url, base_domain_path)
        
        for link in new_links:
            cleaned_link = link.rstrip('/') # Normalize by removing trailing slash
            if cleaned_link not in visited_urls and cleaned_link not in to_visit_stack:
                # Add to stack only if it's within the base_domain_path constraint
                parsed_link = urlparse(cleaned_link)
                if parsed_link.netloc == parsed_start_url.netloc and \
                   parsed_link.path.startswith(parsed_start_url.path.rstrip('/')):
                    to_visit_stack.append(cleaned_link)
    
    if len(all_found_links) >= max_links_to_find:
        print(f"\nReached maximum link limit ({max_links_to_find}). Stopping crawl.")

    return list(all_found_links)

if __name__ == "__main__":
    target_url = 'https://www.about.hsbc.com.hk/'
    # Ensure target_url ends with a slash if it's a directory-like path for consistent path checking
    if not urlparse(target_url).path.endswith('/') and not '.' in urlparse(target_url).path.split('/')[-1]:
        target_url += '/'
        
    # Extract the last non-empty path segment from the URL
    path_segments = [seg for seg in urlparse(target_url).path.split('/') if seg]
    category = path_segments[-1] if path_segments else 'unknown'
    
    print(f"Starting DFS crawl from: {target_url}")
    
    extracted_links = crawl_site_dfs(target_url)
    
    if extracted_links:
        print("\n--- All Extracted Sub-links ---")
        for link in sorted(list(extracted_links)): # Sort for consistent output
            print(f"{category},{category},{link}")
        print(f"\nTotal unique links found: {len(extracted_links)}")
    else:
        print("No sub-links found or an error occurred during the crawl.")