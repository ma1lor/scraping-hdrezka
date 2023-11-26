import json
import requests
from bs4 import BeautifulSoup
import os 



list = []
add_url = ''


def parse(pages):
    if pages == 'y':
        url = f'https://hdrezka.ag/films/page/1'
        headers = {
            "Accept": "*/*",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36 OPR/89.0.4447.64"
        }
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, 'lxml')

        text = soup.find('div', class_ ='b-navigation').text[-6:]
        pages = int(text.strip().split()[-1])
    else:
        pages = int(pages)
    
    
    page = 1

    while(page < pages):
        add_url = f'page/{page}/'
        url = f'https://hdrezka.ag/films/{add_url}'
        headers = {
            "Accept": "*/*",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36 OPR/89.0.4447.64"
        }
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, 'lxml')
        with open(f'templates/test{page}.html', 'w') as file:
            file.write(r.text)
        with open(f'templates/test{page}.html') as file:
            info = file.read()
        soup = BeautifulSoup(info, 'lxml')
        for name in soup.find_all(class_='b-content__inline_item-link'):
            try:
                name.find("div").text.split(', ')[2]
                list.append({
                    'title' : name.find("a").text,
                    'year' : name.find("div").text.split(', ')[0],
                    'country' : name.find("div").text.split(', ')[1],
                    'genre': name.find("div").text.split(', ')[2],
                    'link' : name.find('a').get('href')
                })

            except:
                list.append({
                    'title' : name.find("a").text,
                    'year' : name.find("div").text.split(', ')[0],
                    'country' : name.find("div").text.split(', ')[1],


            })
        print(f'# Page{page} is parced succesfully! {pages - page} left.')
        page+=1




    with open("list.json", "w") as file:
        json.dump(list, file, indent=4, ensure_ascii=False)
    print('Parcing is done. Look at json file.')


def clear_folder():
    folder_path = '/home/ma1lor/parcing hdrezka/templates'
    try:
        for entry in os.listdir(folder_path):
            entry_path = os.path.join(folder_path, entry)

            if os.path.isfile(entry_path):
                os.remove(entry_path)

    except: pass




def main():
    pages = input('Do you want to parce all pages(write y) or input how much pages you want to parce: ')
    clear_folder()
    parse(pages)
    
if __name__ == "__main__":
    main()


