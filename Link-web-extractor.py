import requests
from bs4 import BeautifulSoup
import urllib.parse

def get_link_descriptions(url):
    # Create a session object
    session = requests.Session()
    # Send a GET request to the URL using session
    response = session.get(url)
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'lxml')
    # Find all the <a> tags within the <div class="post-body"> section
    post_body = soup.find('div', class_='post-body')
    links = post_body.find_all('a')
    # Extract the links and descriptions
    link_descriptions = []
    for link in links:
        link_url = link['href']
        link_text = link.get_text()
        link_descriptions.append({'url': link_url, 'description': link_text})
    return link_descriptions

def get_destination_url(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        skip_button = soup.find('a', id='skip_button')
        if skip_button:
            destination_url = skip_button['href']
            return destination_url
        else:
            return url
    except requests.exceptions.RequestException:
        return url

def is_valid_link(url: str) -> bool:
    """
    Check if a given URL is valid by sending a HEAD request and checking the response status code and content type.

    :param url: The URL to check.
    :return: True if the URL is valid, False otherwise.
    """
    try:
        # Create a modified URL to handle special characters in query parameters
        modified_url = urllib.parse.quote(url, safe=':/')

        response = requests.head(modified_url, allow_redirects=True, timeout=5)

        if response.status_code != 200:
            return False

        content_type = response.headers.get('Content-Type')
        if content_type is not None and not content_type.startswith('text/html'):
            return False

        # Additional checks specific to your use case can be added here

        return True
    except requests.exceptions.RequestException:
        return False

def main():
    while True:
        # Get URL from user input
        url = input('Enter the URL: ')#E.g: 'https://komikdownloadz.blogspot.com/2015/08/senarai-z.html?m=1'

        # Check if the URL is valid
        if is_valid_link(url):
            break
        else:
            print('Error: Invalid URL. Please enter a valid URL.')
    
    # Define the output file name from user input.
    output_file = input('Enter the output file name: ') + '.txt' + '\n' #E.g:'link_descriptions.txt'

    link_descriptions = get_link_descriptions(url)
    num_links = len(link_descriptions)

    print(f'{num_links} links fetch from {url}.\n')

    # Print the deshortened link URLs and descriptions with validity status and write the results to a text file
    with open(output_file, 'w') as f:
        lines = []
        lines.append(f'{num_links} links fetch from {url}.')
        for item in link_descriptions:
            deshortened_url = get_destination_url(item['url'])
            is_valid = is_valid_link(deshortened_url)
            validity_status = 'Valid' if is_valid else 'Error'

            print('URL:', deshortened_url)
            lines.append('URL: {}\n'.format(deshortened_url))
            print('Description:', item['description'])
            lines.append('Description: {}\n'.format(item['description']))
            print('Status:', validity_status, '\n')
            lines.append('Status: {}\n'.format(validity_status))
            lines.append('\n')
        f.writelines(lines)
    print("Results have been written to:", output_file)

if __name__ == '__main__':
    main()