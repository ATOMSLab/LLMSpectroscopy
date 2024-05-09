import requests
import pandas as pd

def load_list():
    csv=pd.read_csv("CandidateList_HL.csv")
    csv['CAS']='C'+csv['CAS'].str.replace('-', '').str.join('')
    return  csv.to_dict('records')

def downloadMolecules(molecule):
    #https://webbook.nist.gov/cgi/cbook.cgi?JCAMP=C2919235&Index=0&Type=IR
    url=f"https://webbook.nist.gov/cgi/cbook.cgi?JCAMP={molecule['CAS']}&Type=IR"
    response = requests.get(url,stream=True)
    if response.status_code == 200:
        with open(f"./dataset/{molecule['molecular formula']}", "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        print(f"{molecule['molecular formula']} download successfully!")
    else:
        print(f"download failed. Status code: {response.status_code}")


def getMolecules(molecule_options):
   
    for molecule in molecule_options:
        try: 
            downloadMolecules(molecule)
        except Exception:
            print(Exception)

if (__name__=="__main__"):
    molecules=load_list()
    getMolecules(molecules)