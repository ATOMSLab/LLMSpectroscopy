
import requests
from html.parser import HTMLParser



#getIsomerSuggestion(C4H8O)
def getIsomerSuggestion(molecule):
 try:
    response=requests.get(f"https://webbook.nist.gov/cgi/cbook.cgi?Formula={molecule}&MatchIso=on&NoIon=on&Units=SI")
    if(response.status_code==200):
        suggestions=parse_html(response.text,molecule)
        suggestions.pop()
        return suggestions
 except Exception:
        print("no suggestions available")
        
 
def parse_html(content,molecule):
    parser = HTMLParser()
    data = []
    def handle_data(data_str):
        data.append(data_str)
    parser.handle_data = handle_data
    parser.feed(content)
    txt=''.join(data).strip().split('Click on the name to see more data.')[1].strip().split('©')[0].replace('\n', '')
    return txt.split(f'({molecule})')

   