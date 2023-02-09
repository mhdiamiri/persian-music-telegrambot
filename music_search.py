import requests as r
import json

base_url = "http://api.codebazan.ir/music/?type=search"

def search_music(query:str, page:int):
    url = base_url + f"&query={query}&page={str(page)}"
    response = r.get(url)
    
    data = []
    
    if response.status_code == 200:
        
        content = json.loads(response.text)
        
        if content["Ok"]:
            
            results = content['Result']
            
            for result in results:
                
                data.append(
                    {
                        "title": result['Title'],
                        "link": result["Link"],
                        "photo": result["Photo"],
                        "d320": result["Music_320"],
                        "d128": result["Music_128"],
                        "page": page,
                     }
                )
    
    return data
