import json
import re
from typing import List, Dict
from bs4 import BeautifulSoup
import httpx
import pandas as pd
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
COOKIE = "fs_uid=#o-1CMWCC-na1#1b96ef5e-7a47-4f3a-a693-4c7faa813c48:7a5b9c1d-1e5e-4c3e-aa42-8cb55d5e3c58:1717604684751::1#/1748951869; pingAvailable=ping; visid_incap_39856=tXdKg2DlSEm81YEXuPd5RGuRYGYAAAAAQUIPAAAAAAAHEuET3xaLhLRoxcxpOJ2C; _gcl_au=1.1.1357943881.1717604696; _caid=6498663a-f5c7-4f73-905d-ba56b5242ed3; _ga=GA1.1.192790557.1717604696; com.silverpop.iMAWebCookie=d8b8a4a1-a855-ca3c-3b14-700693413651; SLISYNC=1; nlbi_39856=QgswBNYinSsIyPUTIf4MxAAAAAAQ3n7PqrSh0GOW0Olmqaf8; AMCVS_1CD915E05D4AC0EE0A495F86%40AdobeOrg=1; AMCV_1CD915E05D4AC0EE0A495F86%40AdobeOrg=1075005958%7CMCIDTS%7C19884%7CMCMID%7C07779636820406473963761150528935243664%7CMCAAMLH-1718545024%7C3%7CMCAAMB-1718545024%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1717947424s%7CNONE%7CvVersion%7C4.4.1; sli_tracking_beacon_id=6665b003bd7d4; s_cc=true; BVBRANDID=a4df9659-d4d2-4699-a79d-6052cd03e32c; BVImplmain_site=12739; _cavisit=18ffd7c531d|; reese84=3:NqY+0Ox4wmwRMsv2X9NO5g==:MDxR+q9UFEE86I3+y+Ipy6xJDZI7NZ/Zm0fCqDk4/JLyGrykVpZts40AF2FbOIxBMyXnIKVkH/E2jKk0zqiPaVqW4Ol56Kq4GKJQ5r5EQcOVPVdB05TpeMlftKfCfkc9DglHjS6jcN9sVqeOtq+ovGXG6GCLqT3Jo5HQIBv8hAbPIn7HmZkoTg4fpUsfc07xBEx13mrztMgeljW7YolS8WElitfUeVbvzX8wOteK8jK+ovFo5Aj2CpNRcOUI72sr4s/STFfUkPsF15aiZ9aHGJnYSsytqbLkxOqbO9ehnQkq72omxzxeg0to1spmgoO/D8OIOVVrqZis78GKlK0rEF2JqPNOH6yXymZ1hEGuRQT9X7dLXT5qooLyoWwpbcjT5z1otgVbqJ+YyGl8qhtFCUEj/lhmuBbTSnxNnGBPrBGxQ466XKDq72R3OYcIG+ow6kHyuHMC26HeNnxi7Qz4B9R2vzJi3DkLL7VR7JFkfTw=:2iPpm+JxipaLhzi38qAXw4Cf04ESA/uU9yPS9HuUL4Q=; incap_ses_309_39856=AJK9bte8SEhS807w6slJBHXKZWYAAAAA9NF5HHCrEC24BQI2/VqhbA==; nlbi_39856_2147483392=HwjeDYGAMHDk2QLqIf4MxAAAAADFdDcQ905XfKHqg0vknUKd; _ga_1TGPPBVB9S=GS1.1.1717946960.8.1.1717946970.50.0.0; ___utmvc=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; forterToken=b296196d055943cbaafa7294c701eaeb_1717946969285__UDF43-m4_21ck_; com.silverpop.iMA.session=40d2ab86-a802-645b-6a0a-7cb77240ad91; com.silverpop.iMA.page_visit=1756588495:; s_tp=22486; SLIBeacon=fUICUSKHQS1717946973391GHHBCXWNV; s_ppv=Heat%2520Pump%2520Systems%2C14%2C8%2C3151; s_getNewRepeat=1717946984334-Repeat; s_sq=theecommstorehnprod%3D%2526c.%2526a.%2526activitymap.%2526page%253DHeat%252520Pump%252520Systems%2526link%253DKelvinator%2525203.9kW%252520Window%25252FWall%252520Cooling%252520Only%252520Air%252520Conditioner%2526region%253D__next%2526pageIDType%253D1%2526.activitymap%2526.a%2526.c%2526pid%253DHeat%252520Pump%252520Systems%2526pidt%253D1%2526oid%253Dhttps%25253A%25252F%25252Fwww.harveynorman.com.au%25252Fkelvinator-3-9kw-window-wall-cooling-only-air-conditioner.html%2526ot%253DA"
HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en,vi;q=0.9,en-US;q=0.8",
    "Cache-Control": "no-cache",
    "Cookie": COOKIE,
    "Pragma": "no-cache",
    "Priority": "u=0, i",
    "Referer": "https://www.harveynorman.com.au/heating-cooling-air-treatment/air-condition",
    "Sec-Ch-Ua": "\"Google Chrome\";v=\"125\", \"Chromium\";v=\"125\", \"Not.A/Brand\";v=\"24\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": USER_AGENT,
}

def _get_total_page(url: str) -> int:
    response = httpx.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')

    total_page = soup.find("div", class_="ProductCardContainerPagination_sf-product-card-container__pagination__6p65N").find_all('a')[-1].text.strip()
    total_page = int(total_page)
    print("Total page:" + str(total_page)) 
    return total_page

def extract_model_and_kw(text):
    # Regular expression to find the model (all words before kW)
    model_pattern = r"^(.*?)\s\d+\.\d+kW"
    
    # Regular expression to find the power (kW)
    kw_pattern = r"\d+\.\d+kW"
    
    model = re.search(model_pattern, text)
    if model:
        model = model.group(1)
    
    kw = re.search(kw_pattern, text)
    if kw:
        kw = kw.group()
    
    return model, kw

def extract_comment_count(text):
    # Remove non-digit characters from the text and convert to integer
    number = int(''.join(filter(str.isdigit, text)))
    return number

def get_data_from_main_page(url: str) -> List[Dict[str, any]]:
    data = []
    response = httpx.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    data_we_want = soup.find('script', id='__NEXT_DATA__').text
    json_data = json.loads(data_we_want)
    asset_list = json_data['props']['pageProps']['pageProps']['pageData']['productsData']['items']
    print("Total item:" + str(len(asset_list)))
    for asset in asset_list:
        product_id = asset['id']
        product_name = asset['name']
        manuffature , kw = extract_model_and_kw(product_name)
        base_url = 'https://www.harveynorman.com.au'
        url_key = asset['url_key']
        url_suffix = asset['url_suffix']
        url_link = f'{base_url}/{url_key}{url_suffix}'
        price = float(asset['price_range']['minimum_price']['final_price']['value'])
        ratings = asset.get("ratings", "")
        if ratings:
            commnet_count = int(ratings.get("count", 0))
        comments = []
        if commnet_count > 0:    
            comments = get_comments_from_asset_page(product_id)

        data.append({
            "manuffature": manuffature,
            "kw": kw,
            "commnet_count": commnet_count,
            "price": price,
            "url_link": url_link,
            "comments" : comments,
        })

    return data

def get_comments_from_asset_page(product_id: str) -> List[Dict[str, str]]:
    comments = []
    try:
        url = f"https://api.bazaarvoice.com/data/batch.json?passkey=da3svyw8zpgow5xy2pct27s8r&apiversion=5.5&displaycode=12739-en_au&resource.q0=products&filter.q0=id%3Aeq%3A{product_id}&stats.q0=reviews&filteredstats.q0=reviews&filter_reviews.q0=contentlocale%3Aeq%3Aen*%2Cen_AU&filter_reviewcomments.q0=contentlocale%3Aeq%3Aen*%2Cen_AU&resource.q1=reviews&filter.q1=isratingsonly%3Aeq%3Afalse&filter.q1=productid%3Aeq%3A{product_id}&filter.q1=contentlocale%3Aeq%3Aen*%2Cen_AU&sort.q1=relevancy%3Aa1&stats.q1=reviews&filteredstats.q1=reviews&include.q1=authors%2Cproducts%2Ccomments&filter_reviews.q1=contentlocale%3Aeq%3Aen*%2Cen_AU&filter_reviewcomments.q1=contentlocale%3Aeq%3Aen*%2Cen_AU&filter_comments.q1=contentlocale%3Aeq%3Aen*%2Cen_AU&limit.q1=1&offset.q1=0&limit_comments.q1=8&resource.q2=reviews&filter.q2=productid%3Aeq%3A{product_id}&filter.q2=contentlocale%3Aeq%3Aen*%2Cen_AU&limit.q2=100&resource.q3=reviews&filter.q3=productid%3Aeq%3A{product_id}&filter.q3=isratingsonly%3Aeq%3Afalse&filter.q3=issyndicated%3Aeq%3Afalse&filter.q3=rating%3Agt%3A3&filter.q3=totalpositivefeedbackcount%3Agte%3A3&filter.q3=contentlocale%3Aeq%3Aen*%2Cen_AU&sort.q3=totalpositivefeedbackcount%3Adesc&include.q3=authors%2Creviews%2Cproducts&filter_reviews.q3=contentlocale%3Aeq%3Aen*%2Cen_AU&limit.q3=100&resource.q4=reviews&filter.q4=productid%3Aeq%3A{product_id}&filter.q4=isratingsonly%3Aeq%3Afalse&filter.q4=issyndicated%3Aeq%3Afalse&filter.q4=rating%3Alte%3A3&filter.q4=totalpositivefeedbackcount%3Agte%3A3&filter.q4=contentlocale%3Aeq%3Aen*%2Cen_AU&sort.q4=totalpositivefeedbackcount%3Adesc&include.q4=authors%2Creviews%2Cproducts&filter_reviews.q4=contentlocale%3Aeq%3Aen*%2Cen_AU&limit.q4=100&callback=BV._internal.dataHandler0"
        response = httpx.get(url, headers=HEADERS)
        if response.status_code == 200:
            print("Get comment success for product_id: " + str(product_id))
            start_index = response.text.find('{')
            end_index = response.text.rfind('}')
            json_data = response.text[start_index:end_index+1]
            json_data = json.loads(json_data) 

        else:
            print("Error:", response.status_code)


        comment_list = json_data['BatchedResults']['q2']['Results']
        for comment_data in comment_list:
            name = comment_data.get("UserNickname", "")
            city = comment_data.get("UserLocation", "")
            comment = comment_data.get("ReviewText", "")
            
            ratings = comment_data.get("SecondaryRatings", "")
            star = None
            if ratings:
                quality = ratings.get("Quality", "")
                if quality:
                    star = quality.get("Value", "")
            if comment is not None:
                comments.append({
                    "comment": comment,
                    "star": star,
                    "name": name,
                    "city": city,
                })
    except Exception as e:
        print(e)
        get_comments_from_asset_page(product_id=product_id)
    return comments

def get_data(base_url: str) -> pd.DataFrame:
    data = []
    total_page = _get_total_page(base_url) + 1
    for page in range(1, total_page):
        url = f'{base_url}?p={page}'
        data.extend(get_data_from_main_page(url))
    # df_final = pd.DataFrame(data)
    print(len(data))
    print("Export output to result.json")
    with open("result.json", 'w') as json_file:
        json.dump(data, json_file)

    return data

url = 'https://www.harveynorman.com.au/heating-cooling-air-treatment/air-conditioning/split-system-airconditioners'
get_data(url)
