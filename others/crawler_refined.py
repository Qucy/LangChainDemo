import asyncio
import csv
import os
import httpx
from urllib.parse import urlparse
from crawl4ai import AsyncWebCrawler

async def url_to_markdown(url):
    """Convert a URL to markdown format and download any PDF links found."""
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=url)
        pdf_links = []
        
        if result.links and 'internal' in result.links:
            # retrieve pdf links
            for link in result.links['internal']:
                href = link['href']
                if href.endswith('.pdf'):
                    print(f"  PDF link: {href}")
                    pdf_links.append(href)
        
        return result.markdown, pdf_links

async def download_pdf(pdf_url, folder_path):
    """Download a PDF file and save it to the specified folder."""
    try:
        # Extract filename from URL
        parsed_url = urlparse(pdf_url)
        filename = os.path.basename(parsed_url.path)
        
        if not filename.endswith('.pdf'):
            filename += '.pdf'
        
        file_path = os.path.join(folder_path, filename)
        
        # Check if file already exists
        if os.path.exists(file_path):
            print(f"  ✓ PDF already exists at {file_path}, skipping download")
            return True
        
        # Download the PDF file
        async with httpx.AsyncClient() as client:
            print(f"  Downloading PDF: {pdf_url} to {file_path}")
            response = await client.get(pdf_url, follow_redirects=True)
            response.raise_for_status()
            
            # Save the PDF file
            with open(file_path, 'wb') as f:
                f.write(response.content)
                
            print(f"  ✓ PDF saved to {file_path}")
            return True
    except Exception as e:
        print(f"  ✗ Error downloading PDF {pdf_url}: {str(e)}")
        return False

def create_folder_structure(url):
    """Create folder structure based on URL and return the file path."""
    # Parse the URL
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    path = parsed_url.path.strip('/')
    
    # Create folder structure
    folder_path = os.path.join(os.getcwd(), domain, path)
    os.makedirs(folder_path, exist_ok=True)
    
    # Create file name based on URL path
    file_name = domain.replace('.', '_')
    if path:
        file_name += '_' + path.replace('/', '_')
    file_name += '.md'
    
    return os.path.join(folder_path, file_name), folder_path

async def process_csv(csv_file, top_n=None):
    """Process URLs from CSV file and save markdown content."""
    failed_urls = []
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        
        # Limit to top_n rows if specified
        if top_n is not None:
            rows = rows[:min(top_n, len(rows))]
        
        print(f"Processing {len(rows)} URLs...")
        
        for i, row in enumerate(rows):
            url = row['url'].strip()
            section = row['section']
            title = row['title']
            
            print(f"[{i+1}/{len(rows)}] Processing: {url}")
            
            try:
                # Get markdown content and PDF links
                markdown_content, pdf_links = await url_to_markdown(url)
                
                # Filter content after "Top of main content"
                content_parts = markdown_content.split("Top of main content")
                if len(content_parts) > 1:
                    markdown_content = content_parts[1]
                
                # Add metadata at the top
                metadata = f"# {title}\n\n**Section:** {section}\n\n**URL:** {url}\n\n---\n\n"
                markdown_content = metadata + markdown_content
                
                # Create file path and save content
                file_path, folder_path = create_folder_structure(url)
                with open(file_path, 'w', encoding='utf-8') as md_file:
                    md_file.write(markdown_content)
                
                print(f"  ✓ Saved to {file_path}")
                
                # Download PDF files if any
                if pdf_links:
                    print(f"  Found {len(pdf_links)} PDF files to download")
                    download_tasks = [download_pdf(pdf_url, folder_path) for pdf_url in pdf_links]
                    await asyncio.gather(*download_tasks)
                
            except Exception as e:
                error_msg = f"  ✗ Error processing {url}: {str(e)}"
                print(error_msg)
                failed_urls.append({
                    'url': url,
                    'section': section,
                    'title': title,
                    'error': str(e)
                })
        
        # Save failed URLs to a file if any
        if failed_urls:
            failed_file = 'failed_urls.csv'
            print(f"\nSaving {len(failed_urls)} failed URLs to {failed_file}")
            with open(failed_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['url', 'section', 'title', 'error'])
                writer.writeheader()
                writer.writerows(failed_urls)
            print(f"Failed URLs saved to {failed_file}")

async def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Convert URLs from CSV to markdown files')
    parser.add_argument('--csv', default='hsbc_doormat_links.csv', help='Path to CSV file')
    parser.add_argument('--top', type=int, help='Process only top N records')
    
    args = parser.parse_args()
    
    await process_csv(args.csv, args.top)

if __name__ == "__main__":
    asyncio.run(main())