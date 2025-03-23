import google.generativeai as genai
from duckduckgo_search import DDGS
from bs4 import BeautifulSoup
from tqdm import tqdm
import requests
import time
from util.file import *

def gemini_handler(chat_obj, prompt, cooldown_rest_sec = 60):
    while True:
        try:
            response = chat_obj.send_message(prompt)
            return response
        except Exception as e:
            print(e)
            for i in tqdm(range(cooldown_rest_sec),    desc="Runtime error...  API cooldown..."):
                time.sleep(1)

api_key = load_info("keys\\google\\gemini-2.0-flash.txt")
max_results = 10
candidate_count = 1
temperature = 0.5
history = []
history_path = "history.pkl"
#history = load_info(history_path)

genai.configure(api_key=api_key)
generation_config = genai.types.GenerationConfig(candidate_count=candidate_count, temperature=temperature)
model = genai.GenerativeModel('gemini-2.0-flash')
chat = model.start_chat(history=history)

print("What topic you want to search?")
keyword = input()

_, save_path = create_folder(keyword)

search_result_list = []

print("Search results will be save to " + save_path + "/" + "search_results.json")
for search_results in tqdm(DDGS().text(keywords=keyword, safesearch="off", timelimit="10d", max_results=max_results), desc="Searching... "): 
    r = requests.get(search_results['href'])
    soup = BeautifulSoup(r.content, 'html.parser')
    content_str = soup.get_text().replace("\n", " ")
    response = gemini_handler(chat, content_str + "\n extract the key message from the text, in 300 words, in 繁體中文")
    #print(response.text)
    briefing = response.text

    response = gemini_handler(chat, "{} {} \n rate the relevance between the text above and the topic : {} from 0 to 100, give only the rating number".format(search_results['title'], search_results['body'], keyword))
    #print(response.text)
    rating = int(response.text)

    search_result_temp = {"title" : search_results['title'], "intro" : search_results['body'], "url" : search_results['href'], "briefing" : briefing, "rating" : rating}

    idx = 0
    for search_result in search_result_list:
        if search_result_temp['rating'] > search_result['rating']:
            break
        idx += 1
    search_result_list.insert(idx, search_result_temp)
    
    save_info_json(save_path + "/" + "search_results.json", {"search_results" : search_result_list})
    save_info_bin(save_path + "/" + history_path, chat.history)