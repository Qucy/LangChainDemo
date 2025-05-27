import csv
import re

def convert_txt_to_csv(input_file, output_file):
    # Open the input file
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split the content into chunks based on the source URL pattern
    chunks = re.split(r'(\w+) - Source: (https?://[^\s]+)\s*', content)
    
    # Initialize the CSV data
    csv_data = []
    
    # Process each chunk
    i = 1
    while i < len(chunks):
        category = chunks[i]
        source = chunks[i+1]
        chunk_content = chunks[i+2].strip()
        
        # Split the chunk content into lines
        lines = chunk_content.split('\n')
        
        # Process each line in the chunk
        for line in lines:
            if line.strip():  # Skip empty lines
                parts = line.split(',')
                if len(parts) >= 3:  # Ensure we have at least 3 parts
                    scenario = parts[0].strip()
                    question = parts[1].strip()
                    answer = ','.join(parts[2:]).strip()  # Join remaining parts as answer in case there are commas in the answer
                    
                    # Add to CSV data
                    csv_data.append([
                        category,          # Category
                        'PDF Retrieval',   # Capability
                        scenario,          # Scenarios
                        question,          # Questions
                        source,            # Source
                        answer             # Answer
                    ])
        
        i += 3  # Move to the next chunk
    
    # Write to CSV file
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # Write header
        writer.writerow(['Category', 'Capability', 'Scenarios', 'Questions', 'Source', 'Answer'])
        # Write data
        writer.writerows(csv_data)
    
    print(f"Conversion completed. CSV file saved as {output_file}")

# Execute the conversion
if __name__ == "__main__":
    input_file = "/Users/qucy/Projects/PythonCodePractise/pws_pdf_qa.txt"
    output_file = "/Users/qucy/Projects/PythonCodePractise/pws_pdf_qa.csv"
    convert_txt_to_csv(input_file, output_file)