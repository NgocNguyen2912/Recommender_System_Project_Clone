# Import libraries
import requests
from bs4 import BeautifulSoup
import re
import json
from time import sleep
import random
import signal
import sys


# Initial varibles:
PATH = "C:/Users/ADMIN/Processing/DSA-Project/processing/T1_CollectingData/"

# Functions Signal:
def save_and_exit(signum, frame, flag, data, filename):
    if not flag:
        with open(filename, 'w') as f:
            json.dump(data, f)
        print("File saved. Exiting...")
    else:
        print("Writing is already complete. Exiting...")
    sys.exit(0)

# Initial class:
class User_Scraper:
    def __init__(self):
        pass
    
    def scrape_user_ratings(self,container):
        # Initial lists:
        movie_id = []
        user_rating = []
        
        # Regex pattern:
        pattern = r'/title/(\w+)/?'
        
        for content in container:
            movie_tag = content.find('div', class_ = "lister-item-header")
            rating_tag = content.find_all('span', class_= "rating-other-user-rating")
            
            try:
                movie_id_re = re.findall(pattern, str(movie_tag.find('a')['href']))
                movie_id.append(movie_id_re[0])
            except:
                movie_id.append("")
            
            try:
                rating = rating_tag[0].find('span')
                user_rating.append(rating.text)
            except:
                user_rating.append("")
            
        return (movie_id, user_rating)
    
    def scrape_user_inf(self, user_id):
        insert_data = {}
        url = "https://imdb-api.huyvongmongmanh75.workers.dev/user/" + user_id;
        response = requests.get(url)
        data = response.json()
        
        insert_data["user_id"] = user_id
        insert_data["user_name"] = data["name"]
        try:
            insert_data["member_since"] = data["member_since"]
        except:
            insert_data["member_since"] = ""
            
        return insert_data
    
    def scrape_user(self, user_id):
        # Scrape User Information:
        
        user_infor = self.scrape_user_inf(user_id)
        user_infor_path = PATH + f"data/users_inf/{user_id}.json"
        
        flag = False
        # Capture signal SIGINT (Ctrl+C)
        signal.signal(signal.SIGINT, lambda signum, frame: save_and_exit(signum, frame, flag, user_infor, user_infor_path))
        
        with open(user_infor_path, 'w') as json_file:
            json.dump(user_infor, json_file)
            flag = True
    
            
        # Scrape User Ratings:
        # Initial varibles
        data = {}
        users_id = []
        movies_id = []
        users_rating = []
        
        page = requests.get(f"https://www.imdb.com/user/{user_id}/reviews")
        soup = BeautifulSoup(page.text, 'html.parser')
        
        container = soup.find_all('div', class_ = "lister-item-content")
        
        user_ratings = self.scrape_user_ratings(container)
        
        users_id.extend([user_id]*len(user_ratings[0]))
        movies_id.extend(user_ratings[0])
        users_rating.extend(user_ratings[1])
        
        data['user_id'] = users_id
        data['movie_id'] = movies_id
        data['user_rating'] = users_rating
        
        file_path = PATH + "data/pmovie_id.json"
        
        with open(file_path, 'r') as json_file:
           pmovie_id = json.load(json_file)
        
        for movie_id in movies_id:
            if movie_id not in pmovie_id:
                pmovie_id[movie_id] = False
        
        try:
            key_tag = soup.find('div', class_ = "load-more-data")
            next_key = key_tag['data-key']
        
            npage = 0
            while npage < 5:
                npage = npage + 1
                sleep(random.uniform(1,3))
                print(f"Scraping page {npage} !!!")
                
                headers = {
                    'authority': 'www.imdb.com',
                    'accept': '*/*',
                    'accept-language': 'en-US,en;q=0.9',
                    # 'cookie': 'session-id=132-9465593-9579807; ubid-main=135-6830841-7942246; x-main=w0ZaH5Eo3FmqVdfuysdVNtYtfKr3ZcI2HRoZI0XQ0JcXNqFZ4dR4GgtS5NhNzMVX; at-main=Atza|IwEBIOSayYl4Fq5MXlnWj-XCeod479dbf5kNoLnC3G73bhkNsW3WySbj_TBGXn7SJzeRVLAaJPWDpY1lffbqCzw-a4Y-NhZhNMqv5OkiLpxSvYhr-oE6q0affb-aYD31fzp__S9ApxOTsD1fnxcRdGg0c_oQ3_YogUfqGkmX-pV5YO5FlYgcdhX0RwFhAAitQkHNX3SoQzH-Yj41k8K2c_W0_vWyXgPmgi0HS_eyUWKkayADgA; sess-at-main="6tsRA4li+0+CoTNmqSzcYfAM3/wZF4TOP8JKh3ENzNg="; uu=eyJpZCI6InV1ZDA3NDU0MmVmNmIxNGVhODk5YTUiLCJwcmVmZXJlbmNlcyI6eyJmaW5kX2luY2x1ZGVfYWR1bHQiOmZhbHNlfSwidWMiOiJ1cjE3MjkzODc4NSJ9; session-id-time=2082787201l; ad-oo=0; ci=e30; as=%7B%22n%22%3A%7B%22t%22%3A%5B970%2C250%5D%2C%22tr%22%3A%5B300%2C250%5D%2C%22in%22%3A%5B0%2C0%5D%2C%22ib%22%3A%5B0%2C0%5D%7D%7D; session-token=w9h9AEbfJs4c7Zqbg+Wh/5cX+W3elFtxdXlWLDyc0mkNceZ3rhG/qIKmCuR3n+AdL8F+wZyz9b81W/RmdqZcY0PIRoHKWKHulKMDVorLoNSX9Rz5tPrChZqwc1k6lnnYivm/uGXuYdKHWv4Ep4wBaMS7z14cLj+JuqTLMKhx/xyj75AwvcQ08nnQDwvxacAnCG+yN8xT5U9ubPsHaN920nF6TCMcGh5X6iae2QGQV5N8oA4lgEohty282vXklcF09LcgXeKiFvLO2ZmJZPDfsMosPkmxmr+CYpyGgBglLPA+HPUb0qVrMpsTOxWR5meseKZFXmHPfz+Jg1HfxE+/+tjtXqhU/TLk36D3IL+FpFxxCIKHPxTDxI82ec+UD48D; csm-hit=tb:s-7PMMPK9D670VMEFXSRXF|1711187288643&t:1711187289721&adb:adblk_no',
                    'referer': f'https://www.imdb.com/user/{user_id}/reviews',
                    'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Microsoft Edge";v="122"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-origin',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
                    'x-requested-with': 'XMLHttpRequest',
                }
                
                params = {
                    'ref_': 'undefined',
                    'paginationKey': next_key,
                }
            
                page = requests.get(f"https://www.imdb.com/user/{user_id}/reviews/_ajax", headers = headers, params = params)   
                soup = BeautifulSoup(page.text, 'html.parser')
                
                container = soup.find_all('div', class_ = "lister-item-content")
                
                user_ratings = self.scrape_user_ratings(container)
                
                users_id.extend([user_id]*len(user_ratings[0]))
                movies_id.extend(user_ratings[0])
                users_rating.extend(user_ratings[1])
                
                key_tag = soup.find('div', class_ = "load-more-data")
                next_key = key_tag['data-key'] 
                
                data['user_id'] = users_id
                data['movie_id'] = movies_id
                data['user_rating'] = users_rating
                
                
                for movie_id in movies_id:
                    if movie_id not in pmovie_id:
                        pmovie_id[movie_id] = False
        except: 
            pass
        
        file_path_data = PATH + f"data/data_umr/{user_id}.json"
        
        flag = False
        # Capture signal SIGINT (Ctrl+C)
        signal.signal(signal.SIGINT, lambda signum, frame: save_and_exit(signum, frame, flag, data, file_path_data))
                      
        with open(file_path_data, 'w') as json_file:
            json.dump(data, json_file)
            flag = True
        
        flag = False
        # Capture signal SIGINT (Ctrl+C)
        signal.signal(signal.SIGINT, lambda signum, frame: save_and_exit(signum, frame, flag, pmovie_id, file_path))
        
        with open(file_path, 'w') as json_file:
            json.dump(pmovie_id, json_file)
            flag = True

            
            