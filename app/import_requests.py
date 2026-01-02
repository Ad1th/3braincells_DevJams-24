# import requests
# from bs4 import BeautifulSoup
# from collections import Counter
# import re
# import webbrowser
# import time
# import json
# import os

# def generate_words_from_prompt(prompt):
#     # Replace spaces in the prompt with underscores to form the Wikipedia URL
#     prompt_query = prompt.replace(' ', '_')
#     global prompt_query
#     url = f'https://en.wikipedia.org/wiki/{prompt_query}'

#     # Fetch the HTML content of the page
#     response = requests.get(url)

#     if response.status_code == 200:
#         # Parse the HTML content using BeautifulSoup
#         soup = BeautifulSoup(response.content, 'html.parser')
#         # Extract all text content from the page
#         text = soup.get_text(separator=' ').lower()
#         # Remove special characters and split the text into words
#         words = re.findall(r'\b\w+\b', text)
#         # Count the frequency of each word
#         word_counts = Counter(words)
#         # Get the 100 most common words, excluding stop words
#         common_words = [word for word, count in word_counts.most_common(100)]
#         return common_words
#     else:
#         print(f"Failed to fetch the page. Status code: {response.status_code}")
#         return []

# def analyze_prompt(prompt, url):  # Add url as a parameter
#     generated_words = generate_words_from_prompt(prompt)
#     print("Generated words based on the prompt:", generated_words)

#     # Use the provided URL instead of a hardcoded one
#     response = requests.get(url)

#     if response.status_code == 200:
#         soup = BeautifulSoup(response.content, 'html.parser')
        
#         # Extract keywords from meta tags
#         keywords_meta = soup.find('meta', attrs={'name': 'keywords'})
#         if keywords_meta:
#             keywords = keywords_meta.get('content', '').split(',')
#             print('Keywords:', [keyword.strip() for keyword in keywords])
#         else:
#             print('No keywords found.')

#         # Extract main headers (h1, h2, etc.)
#         headers = {}
#         for tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
#             headers[tag] = [header.get_text(strip=True) for header in soup.find_all(tag)]

#         # Display headers
#         for tag, content in headers.items():
#             print(f'\n{tag.upper()} Headers:')
#             for header in content:
#                 print(f'- {header}')

#         # Check for existence of specific words in headers
#         search_terms = generated_words
#         found_terms = {
#             term: any(term.lower() in header.lower() for headers in headers.values() for header in headers)
#             for term in search_terms
#         }

#         ctr = sum(found_terms.values())  # Count how many search terms were found

#         for term, found in found_terms.items():
#             print(f"'{term}' found in headers: {found}")

#         # Check if count of found terms meets threshold
#         threshold = 0.4 * len(search_terms)
        
#         if ctr >= threshold:
#             print("Productive")
#         else:
#             print("YOUR DISTRACTED!!")
#             time.sleep(5)  # Wait before opening distracting tab
#             open_distracted_tab()
#     else:
#         print(f"Failed to fetch the page. Status code: {response.status_code}")

# def open_distracted_tab():
#     #import requests
#     #import webbrowser
#     #import json
#     #import os

#     # Function to create an HTML file and display the links
#     def create_html_file(links):
#         # Create an HTML file name
#         html_file_name = 'links.html'
        
#         # Create the HTML content
#         html_content = '''
#         <!DOCTYPE html>
#         <html lang="en">
#         <head>
#             <meta charset="UTF-8">
#             <meta name="viewport" content="width=device-width, initial-scale=1.0">
#             <title>Fetched Links</title>
#         </head>
#         <body>
#             <h1>Fetched Links</h1>
#             <ul>
#         '''

#         for link in links:
#             html_content += f'<li><a href="{link}" target="_blank">{link}</a></li>'

#         html_content += '''
#             </ul>
#         </body>
#         </html>
#         '''

#         # Write the HTML content to a file
#         with open(html_file_name, 'w') as html_file:
#             html_file.write(html_content)

#         # Open the HTML file in the web browser
#         webbrowser.open_new_tab(f'file://{os.path.abspath(html_file_name)}')

#     # Function to get links from the server
#     def fetch_links_from_server(prompt):
#         url = 'http://localhost:3002/gemini'  # Ensure your Node.js server is running on this URL and port
#         headers = {'Content-Type': 'application/json'}
#         data = {'prompt': prompt}

#         try:
#             response = requests.post(url, headers=headers, json=data)

#             if response.status_code == 200:
#                 # Load the response JSON
#                 json_response = response.json()

#                 # Extract links from the response
#                 if 'links' in json_response:
#                     links = json_response['links']
#                     print("Links fetched from server:", links)
#                     return links
#                 else:
#                     print("No links found in the response.")
#                     return []
#             else:
#                 print(f"Failed to fetch the links. Status code: {response.status_code}")
#                 return []
#         except Exception as e:
#             print(f"Error occurred while fetching links: {str(e)}")
#             return []

#     # Main function to get the prompt, fetch links, and display them in HTML
# def main():
#     prompt = prompt_query
#     links = fetch_links_from_server(prompt)

#     if links:
#         print("Creating HTML file with fetched links...")
#         create_html_file(links)
#     else:
#         print("No valid links to display.")

# if __name__ == "__main__":
#     main()



# # Example usage (this will be replaced by your frontend input)
# # analyze_prompt("Your task here")  # Call this function with user input from frontend

import requests
from bs4 import BeautifulSoup
from collections import Counter
import re
import webbrowser
import time
import json
import os

# Function to generate common words from a Wikipedia page based on a prompt
def generate_words_from_prompt(prompt):
    # Replace spaces in the prompt with underscores to form the Wikipedia URL
    prompt_query = prompt.replace(' ', '_')
    url = f'https://en.wikipedia.org/wiki/{prompt_query}'

    # Fetch the HTML content of the Wikipedia page
    response = requests.get(url)

    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        # Extract all text content from the page and clean it
        text = soup.get_text(separator=' ').lower()
        # Remove special characters and split the text into words
        words = re.findall(r'\b\w+\b', text)
        # Count the frequency of each word
        word_counts = Counter(words)
        # Return the 100 most common words
        common_words = [word for word, count in word_counts.most_common(100)]
        return common_words
    else:
        print(f"Failed to fetch the Wikipedia page. Status code: {response.status_code}")
        return []

# Function to analyze a given URL and compare it to the prompt's generated words
def analyze_prompt(prompt, url):
    # Generate common words from the Wikipedia page related to the prompt
    generated_words = generate_words_from_prompt(prompt)
    print("Generated words based on the prompt:", generated_words)

    # Fetch the HTML content of the provided URL
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract keywords from the meta tags
        keywords_meta = soup.find('meta', attrs={'name': 'keywords'})
        if keywords_meta:
            keywords = keywords_meta.get('content', '').split(',')
            print('Keywords:', [keyword.strip() for keyword in keywords])
        else:
            print('No keywords found.')

        # Extract main headers (h1, h2, etc.)
        headers = {}
        for tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            headers[tag] = [header.get_text(strip=True) for header in soup.find_all(tag)]

        # Display the headers
        for tag, content in headers.items():
            print(f'\n{tag.upper()} Headers:')
            for header in content:
                print(f'- {header}')

        # Check for existence of generated words in headers
        found_terms = {
            term: any(term.lower() in header.lower() for headers in headers.values() for header in headers)
            for term in generated_words
        }

        # Count how many search terms were found in the headers
        ctr = sum(found_terms.values())

        # Output results
        for term, found in found_terms.items():
            print(f"'{term}' found in headers: {found}")

        # Check if the number of found terms meets the 40% threshold
        threshold = 0.4 * len(generated_words)
        if ctr >= threshold:
            print("Productive")
        else:
            print("You're distracted!")
            time.sleep(5)  # Pause for 5 seconds before opening the distracting tab
            open_distracted_tab(prompt)
    else:
        print(f"Failed to fetch the page. Status code: {response.status_code}")

# Function to fetch and display distracting links from a local server
def open_distracted_tab(prompt):
    def fetch_links_from_server(prompt):
        url = 'http://localhost:3002/gemini'  # Ensure your Node.js server is running on this URL and port
        headers = {'Content-Type': 'application/json'}
        data = {'prompt': prompt}

        try:
            response = requests.post(url, headers=headers, json=data)

            if response.status_code == 200:
                # Load the response JSON
                json_response = response.json()

                # Extract links from the response
                if 'links' in json_response:
                    links = json_response['links']
                    print("Links fetched from server:", links)
                    return links
                else:
                    print("No links found in the response.")
                    return []
            else:
                print(f"Failed to fetch the links. Status code: {response.status_code}")
                return []
        except Exception as e:
            print(f"Error occurred while fetching links: {str(e)}")
            return []

    def create_html_file(links):
        # Generate HTML file content with links
        html_file_name = 'links.html'
        html_content = '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Fetched Links</title>
        </head>
        <body>
            <h1>Fetched Links</h1>
            <ul>
        '''
        for link in links:
            html_content += f'<li><a href="{link}" target="_blank">{link}</a></li>'

        html_content += '''
            </ul>
        </body>
        </html>
        '''

        # Write the HTML content to a file
        with open(html_file_name, 'w') as html_file:
            html_file.write(html_content)

        # Open the HTML file in the web browser
        webbrowser.open_new_tab(f'file://{os.path.abspath(html_file_name)}')

    # Fetch the links based on the prompt and create the HTML file
    links = fetch_links_from_server(prompt)
    if links:
        create_html_file(links)
    else:
        print("No valid links to display.")

# Example usage of the analyze_prompt function
if __name__ == "__main__":
    prompt = "Your task here"
    url = "https://example.com"  # Replace with the actual URL you want to analyze
    analyze_prompt(prompt, url)