
import requests
from html.parser import HTMLParser
import re

#i.e et_isomer_suggestion(C9H20O)
def get_isomer_suggestion(molecule):
 try:
    response=requests.get(f"https://webbook.nist.gov/cgi/cbook.cgi?Formula={molecule}&MatchIso=on&NoIon=on&Units=SI")
    if(response.status_code==200):
        suggestions=parse_html_suggestions(response.text,molecule)
        suggestions.pop()
        print(f"""\033[94m
_________________________________________________\n\n The number of  possible Isomers is {len(suggestions)}\n_________________________________________________
        ""","\033[0m","\n".join(suggestions),'\n_________________________________________________')
        return suggestions
 except Exception:
        print("no suggestions available") 
        return []     

# html cleaning and parsign

def parse_html(content):
    parser = HTMLParser()
    data = []
    def handle_data(data_str):
        data.append(data_str)
    parser.handle_data = handle_data
    parser.feed(content)
    return data

def parse_html_suggestions(content,molecule):
    parser = HTMLParser()
    data = parse_html(content)
    txt=''.join(data).strip().split('Click on the name to see more data.')[1].strip().split('©')[0].replace('\n', '')
    return txt.split(f'({molecule})')


def parse_html_other_other_names(name,content):
    data= parse_html(content)
    txt=''.join(data).split('Other names:')[1]
    other_names=txt.split('Permanent link')[0].strip()
    return other_names.replace("\n","").lower().split(';')


# get_other_names("Acetic acid, butyl ester")
def get_other_names(name):
 try:
    c_name="%2C+".join(name.replace(',','').split(" "))
    url=f"https://webbook.nist.gov/cgi/cbook.cgi?Name={c_name}&Units=SI"
    response=requests.get(url)
    if (response.status_code==200):
      return parse_html_other_other_names(name,response.text)
 except Exception:
    print("NO Other Names for ",name, "found")
    return []

def clean_molecule_name(name):
    cleaned_name = re.sub(r'[^a-zA-Z0-9\s]', '', name.replace("n-", ""))
    return cleaned_name.replace(" ", "").lower()
# cross_check_molecule("acetic acid n-butyl ester","acetic acid, butyl ester")
def cross_check_molecule(llmgeneration, correct_molecule):
    options=get_other_names(correct_molecule)
    llmcleaned = clean_molecule_name(llmgeneration)
    for molecule in options:
        cleaned = clean_molecule_name(molecule)
        if cleaned == llmcleaned:
            print("\033[92mThe molecules were a match\033[0m")
            print(llmgeneration,"\n",correct_molecule)
            return True

    print("\033[91mThe molecules were not a match\033[0m")
    print(f"\033[94m_________________________________________________\n\n [INFO] llmgeneration: {llmgeneration} \n [INFO] Options of correct name :\n_________________________________________________\n","\033[0m","\n".join(options),'\n\033[94m_________________________________________________\033[0m\n')
    return False
