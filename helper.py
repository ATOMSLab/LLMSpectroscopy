
import requests
from html.parser import HTMLParser



#getIsomerSuggestion(C9H20O)
def getIsomerSuggestion(molecule):
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







# getOthernames("Acetic acid, butyl ester")
def getOthernames(name):
 try:
    c_name="%2C+".join(name.replace(',','').split(" "))
    url=f"https://webbook.nist.gov/cgi/cbook.cgi?Name={c_name}&Units=SI"
    response=requests.get(url)
    if (response.status_code==200):
      parse_html_other_other_names(name,response.text)
 except Exception:
    print("NO Other Names for ",name, "found")

def parse_html_other_other_names(name,content):
    data= parse_html(content)
    txt=''.join(data).split('Other names:')[1]
    other_names=txt.split('Permanent link')[0].strip()
    print(f"\033[94m_________________________________________________\n\n Other names for {name} compound include\n_________________________________________________\n","\033[0m",other_names,'\n_________________________________________________\n')
    return other_names

