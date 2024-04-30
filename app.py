from flask import Flask, jsonify,request
import pandas as pd
import requests
import wget
import os
import subprocess 
from bs4 import BeautifulSoup
import roman
app = Flask(__name__)
os.chdir("static")
@app.route('/index')
def hello_world():
    return "hello in bahae api"
def extract_titles(soup):
    """Extrait tous les titres h1, h2, h3, h4 de la soupe donnée."""
    titles = []
    for level in range(1, 5):
        for tag in soup.find_all(f'h{level}'):
            titles.append((level, tag.text))
    return titles
def trouver_h2_h4(soup):
    result = {}
    h1_tags = soup.find_all('h1')
    
    for index, h1_tag in enumerate(h1_tags):
        h1_text = h1_tag.get_text()
        result[h1_text] = {}
        
        next_h1 = None
        if index < len(h1_tags) - 1:
            next_h1 = h1_tags[index + 1]

        h2_tags = h1_tag.find_next_siblings('h2', until=next_h1)
        for h2_index, h2_tag in enumerate(h2_tags):
            h2_text = h2_tag.get_text()
            result[h1_text][f"{index + 1}.{chr(97 + h2_index).upper()}.{h2_text}"] = []

            next_h2 = None
            if h2_index < len(h2_tags) - 1:
                next_h2 = h2_tags[h2_index + 1]

            h3_tags = h2_tag.find_next_siblings(['h3'], until=next_h2)
            for h3_tag in h3_tags:
                h3_text = h3_tag.get_text()
                result[h1_text][f"{index + 1}.{chr(97 + h2_index).upper()}.{h2_text}"][f"{h3_text}"] = []

                next_h3 = None
                h3_index = 0
                if h3_index < len(h3_tags) - 1:
                    next_h3 = h3_tags[h3_index + 1]

                h4_tags = h3_tag.find_next_siblings(['h4'], until=next_h3)
                for h4_tag in h4_tags:
                    result[h1_text][f"{index + 1}.{chr(97 + h2_index).upper()}.{h2_text}"][f"{h3_text}"].append(h4_tag.get_text())

    return json.dumps(result, ensure_ascii=False, indent=4)
def create_numbered_list(titles):
    import roman  # Assuming roman module is imported for roman numeral conversion
    counters = [0, 0, 0, 0]  # Counters for h1, h2, h3, h4
    result = {}
    last_level = 1  # Starting level assumed as h1

    for level, title in titles:
        # Reset lower counters if we ascend a level
        if level > last_level:
            for i in range(level - 1, 4):
                counters[i] = 0

        # Increment the counter for the current level
        counters[level - 1] += 1

        # Construct prefix based on current level
        if level == 1:
            prefix = "0"
        elif level == 2:
            prefix = str(counters[1])
        elif level == 3:
            prefix = f"{counters[1]}{chr(96 + counters[2])}"
        elif level == 4:
            prefix = f"{counters[1]}{chr(96 + counters[2])}-{roman.toRoman(counters[3]).lower()}"

        result[prefix] = title
        last_level = level

    return result
def extract_table_of_contents(soup):
    """
    Extracts the table of contents from a BeautifulSoup object.
    
    Args:
    - soup: BeautifulSoup object representing the parsed HTML
    
    Returns:
    - table_of_contents (dict): A dictionary representing the table of contents
                                with hierarchical structure based on heading tags
    """
    table_of_contents = {}
    current_level = table_of_contents
    
    headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    
    for heading in headings:
        tag_name = heading.name
        title = heading.get_text().strip()
        level = int(tag_name[1])  # Extract the level from the tag name (e.g., 'h1' -> level 1)
        
        # Create a new entry in the table of contents
        current_level[level] = {'title': title, 'subheadings': {}}
        
        # Update the current level based on the hierarchy
        if level == 1:
            current_level = table_of_contents
        else:
            parent_level = level - 1
            # Ensure the parent level exists before accessing it
            if parent_level in current_level:
                current_level = current_level[parent_level]['subheadings']
    
    return table_of_contents 
def extract_title(soup):
    """
    Extracts the title from a BeautifulSoup object.
    
    Args:
    - soup: BeautifulSoup object representing the parsed HTML
    
    Returns:
    - title (str): The text of the title tag, or None if not found
    """
    title_tag = soup.title
    if title_tag:
        return title_tag.get_text().strip()
    else:
        return None    
def extract_meta_tags(soup):
    """
    Extracts meta tags from a BeautifulSoup object.
    
    Args:
    - soup: BeautifulSoup object representing the parsed HTML
    
    Returns:
    - meta_tags (dict): A dictionary containing meta tag names as keys and their content as values,
                        with numerical keys for multiple occurrences of the same tag
    """
    meta_tags = {}
    meta_elements = soup.find_all('meta')
    for i, meta in enumerate(meta_elements, start=1):
        name = meta.get('name', f'meta_{i}')
        content = meta.get('content', '')
        meta_tags[name] = content.strip()
    return meta_tags    
def scrape_headings_from_html(soup):
    # Parse the HTML content
    
    # Find all heading tags (h1, h2, h3, h4, h5, h6)
    headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6','p','a'])
    
    # Initialize a dictionary to store headings
    headings_dict = {}
    
    # Loop through the heading tags
    for heading in headings:
        # Get the tag name (e.g., 'h1', 'h2', etc.)
        tag_name = heading.name
        
        # Get the text of the heading
        heading_text = heading.get_text().strip()
        
        # Get the numerical order of the heading
        order = len(headings_dict.get(tag_name, [])) + 1
        
        # Add the heading text to the dictionary
      #  if tag_name not in headings_dict:
       #     headings_dict[tag_name] = {}
       # headings_dict[tag_name][order] = heading_text
        headings_dict[tag_name+"_i_"+str(order)] = heading_text
    
    return headings_dict    
def get_html_text(url):
   tst= []
   ers= []
   try: 
    prefixes = [ 'https://','http://','https://www.',  'http://www.']
    if "//" in url :   
        prefixes=['']
    for prefix in prefixes:
        
        try:
            if "//" in url :
                testedurl= url
                
            else: 
                testedurl = prefix + url
                
            tst.append(testedurl)  
            print("-----------------",tst)
            response = requests.get(testedurl, allow_redirects=True)
           
            if response.status_code == 200:
                soup=BeautifulSoup(response.text)
                fj={'status': 'success','titles':trouver_h2_h4(soup),'titre':extract_title(soup),'metas':extract_meta_tags(soup),'final':str(response.url),'prefix':prefix, 'data': soup.get_text()}#,'tst':str(tst),'testedurl':testedurl,'lasturl':str(list(map(lambda a:a.url,response.history))),
                
                fj.update(scrape_headings_from_html(soup))
                
                return  jsonify(fj)

        except Exception as e:#requests.RequestException
            print(f"Error occurred while trying {prefix + url}: {e}")
            ers.append(e)
    return jsonify({'status': 'failed','ers':str(ers),'tst':str(tst),'lasturl':'', 'data': '','prefix':'','testedurl':testedurl})
   except Exception as problem:
           return jsonify({'status': 'failed','tst':str(tst),"error":str(problem),'lasturl':'', 'data': '','prefix':'','testedurl':testedurl})

def get_html(url):
    prefixes = ['http://', 'https://', 'http://www.', 'https://www.']
    
    for prefix in prefixes:
        try:
            response = requests.get(prefix + url)
            if response.status_code == 200:
                return response.text
        except Exception as e:#requests.RequestException
            print(f"Error occurred while trying {prefix + url}: {e}")
    
    return "nothing worked"


@app.errorhandler(404)
def tasktest(name):
 try:   
  return get_html_text(request.url.replace(r"https://test2-bblm.onrender.com/",""))
 except Exception as me:
  return str(me)   
