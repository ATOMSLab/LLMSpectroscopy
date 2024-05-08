import requests

# essentially modify the code however you want and add the id and names of molecules
molecule_options=[
    {
        "name":"C2H6",
        "id":"C74840"
    }
    ]


def downloadMolecules(molecule):
    url=f"https://webbook.nist.gov/cgi/cbook.cgi?JCAMP={molecule['id']}&Index=1&Type=IR"
    response = requests.get(url,stream=True)
    if response.status_code == 200:
        with open(f"./dataset/C287923", "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        print(f"{molecule['name']} download successfully!")
    else:
        print(f"download failed. Status code: {response.status_code}")


def getMolecules():
    for molecule in molecule_options:
        try:
            return downloadMolecules(molecule)
        except Exception:
            print(Exception)

if (__name__=="__main__"):
    getMolecules()