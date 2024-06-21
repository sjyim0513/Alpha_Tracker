import os
import random
import json
import sqlite3
import multiprocessing
import time
from time import sleep
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException



load_dotenv()

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("disable-gpu")
chrome_options.add_argument("disable-infobars")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--log-level=3")
chrome_options.add_argument("--no-sandbox")

chrome_options2 = webdriver.ChromeOptions()
chrome_options2.add_argument('--incognito')

#init driver
#driver = webdriver.Chrome()

alpha_lists = set(['kevinrose', 'garyvee', 'GrantlandOG', 'drawingContext', 'Snoozetoomuch', 'theo2k2_','kdimes00', 'JakeAndBakeNFT', 'CryptoMaestro','0xminion','peachmint00', 'casperdefi', 'Crypto_WooPig', 'OnChainWizard', 'wassiecapital','NFTAura', 'CryptoGarga', 'Shatt_Eth', 'rektmando', 'keung', 'BrandonKangFilm','izebel_eth','BravoZuloo','PangasB','0xJezza','SneakyninjaNFTs','NFTPrada','staying_poor','hype_eth','pman555','financenewsguy','RasterEyes_','_Madkitty_','Slick_NFT','shikione1','zayn_llywelyn','OnlyToasted','3azima85','GreenGeorgeEth','0x_Capital','mikegee','a16zGames','BinanceLabs','animocabrands','DCGco','PanteraCapital','a16zcrypto','adamwgoldberg','blockchaincap','Sfermion_','cryptodetweiler','roybitsir','fomosaurus','Nehemiah_era','0x_d24','coinfund_io','1confirmation','cmsholdings','ElectricCapital','IOSGVC','variantfund','RepublicCrypto','Morningstar_vc','paradigm','AscensiveAsset','egirl_capital','ryancarson'])
alpha_lists_test = (["HsakaTrades", "jimtalbot", "zevza0", "inshallahDAO", "hkgambler", "PigNomics", "conzimp", "frogcap_", "mattomattik", "CryptoCred", "abetrade", "sailingtosunset", "Pentosh1", "tier10k", "yeojoo_L", "ynot", "highmindful", "CL207", "FixedFloatBot", "Aydan_Crypto", "icebergy_", "0xSisyphus", "FreewayHeilig", "life_for_exo9", "Awawat_Trades", "No_man_one", "didgethedunce", "robustus", "eco", "ambergroup_io", "alansilbert", "NickZurick1", "WebbEmotional", "mikejcasey", "BaronDavis", "cburniske", "FordefiHQ", "kspaglia"])
alpha_lists_test_2 = set(['kevinrose', 'garyvee', 'GrantlandOG']) #'drawingContext', 'Snoozetoomuch', "PigNomics", "conzimp"])

#전역변수
alphas_accounts = set([])
alphas_new = set([])

#check with xpath
def check_exists_by_xpath(xpath, driver):
    #timeout = 3
    try:
        driver.find_element(By.XPATH, value=xpath)
    except NoSuchElementException:
        return False
    return True

def check_exists_by_link_text(text, driver):
    try:
        driver.find_element(By.LINK_TEXT,text)
    except NoSuchElementException:
        return False
    return True

def log_in(driver, email, pw, username, wait=3):
    driver.get('https://twitter.com/i/flow/login')
    
    email_xpath = '//input[@autocomplete="username"]'
    password_xpath = '//input[@autocomplete="current-password"]'
    username_xpath = '//input[@data-testid="ocfEnterTextTextInput"]'
    
    sleep(random.uniform(wait, wait + 1))
    
    #enter email/id
    email_el = driver.find_element(by=By.XPATH, value=email_xpath)
    sleep(random.uniform(wait, wait + 1))
    email_el.send_keys(email)
    sleep(random.uniform(wait, wait + 1))
    email_el.send_keys(Keys.RETURN)
    sleep(random.uniform(wait, wait + 1))
    
    #if twitter spotted unusual login case : enter username
    if check_exists_by_xpath(username_xpath, driver):
        username_el = driver.find_element(by=By.XPATH, value=username_xpath)
        print(username_el)
        sleep(random.uniform(wait, wait + 1))
        username_el.send_keys(username)
        sleep(random.uniform(wait, wait + 1))
        username_el.send_keys(Keys.RETURN)
        sleep(random.uniform(wait, wait + 1))
        
    #enter pw
    sleep(random.uniform(wait, wait + 1))
    password_el = driver.find_element(by=By.XPATH, value=password_xpath)
    password_el.send_keys(pw)
    sleep(random.uniform(wait, wait + 1))
    password_el.send_keys(Keys.RETURN)
    sleep(random.uniform(wait, wait + 1))
    
def find_num_of_follower(driver, alphas):
    #url = f"https://twitter.com/{alpha}/followers_you_follow"
    wait = WebDriverWait(driver, 4)
    print(f"len in follower fuction : {len(alphas)}")
    #follower 전체 주소 찾는 방식 / 전체 가져오는 경우 3개가 추가돼서 나옴
    '''
    elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//a[@aria-hidden='true' and @tabindex='-1' and @role='link' and @class='css-4rbku5 css-18t94o4 css-1dbjc4n r-1niwhzg r-1loqt21 r-1pi2tsx r-1ny4l3l r-o7ynqc r-6416eg r-13qz1uu']")))
    href_values = []
    for ele in elements:
        print(ele)
        href_values.append(ele.get_attribute("href"))   
    
    print(len(href_values))

    # 결과 출력
    for text in href_values:
        print("Text:", text)
    '''
    follower_over_6 = {}
    follower_over_9 = {}
    cnt = 0
    start = 0
    lenght = len(alphas)
    while len(alphas) > 0:
        alpha = alphas.pop(0)
        url = f"https://twitter.com/{alpha}"
        driver.get(url)
        
        try:
            WebDriverWait(driver, 10).until(EC.url_to_be(url))
        except TimeoutException:
            print(f"page load timeout : {alpha}")
            print("페이지 로드 타임아웃\n")

        #이거 리스트 뒤로 보낼 때 여러개 들어가고 그게 다시 나오면서 또 들어가서 무한증식 중 -> set으로 수정
        try: 
            elements = wait.until(EC.presence_of_element_located((By.XPATH, f"//a[@href='/{alpha}/followers_you_follow']/div/div[2]")))
            print(f"!요소를 찾음 : {alpha}")
        except TimeoutException as t:
            print(f"!Timeout load timeout : {alpha}")
            print(f"alpha : {alpha} / 타임아웃 {t}")
            try:
                elements = wait.until(EC.presence_of_element_located((By.XPATH, f'//div[@data-testid="empty_state_header_text"]')))
            except TimeoutException:
                print("대기 시작")
                time.sleep(300) #계정을 바꿔도 타임아웃이 떴을 때 아예 슬립하고 처음 계정으로 다시 로그인 / 돌아와도 타임아웃이라 돌아서 5분 또 기다리면 안됨
                alphas.append(alpha)
                lenght += 1
                print(f"대기 시작시 현재 위치 : {cnt}/{lenght}")
                print(f"남은 리스트 수 : {lenght-cnt}\n")
                start = time.time()
                continue
                
            print(f"타임아웃시 찾은 내용 : {elements.text}")
            if elements.text:
                print(f"비공개 계정 : {alpha}")
                print(f"현재 위치 : {cnt}/{lenght}")
                print(f"남은 리스트 수 : {lenght-cnt}\n")
                continue

        sleep(random.uniform(0.5, 1))
        objects = elements.text.split(" ")[6:]  # 객체를 스페이스로 분할
        flag = 1
        for obj in objects:
            if obj.isdigit():  # 각 객체에서 숫자 확인
                if (int(obj)+2) >= 9:
                    follower_over_9[alpha] = (int(obj)+2)
                elif (int(obj)+2) >= 6:
                    follower_over_6[alpha] = (int(obj)+2)
                print(f"alpha : {alpha} / num of follow with : {int(obj)+2} / right way")
                cnt += 1
                print(f"현재 위치 : {cnt}/{lenght}")
                print(f"남은 리스트 수 : {lenght-cnt}\n")
                end = time.time()
                if start != 0:
                    print(f"다시 시작까지 걸린 시간 : {end-start}")
                flag = 0
                break
                
        if flag == 0:
            continue
        
        span_elements = elements.find_elements(By.TAG_NAME, "span")
        if len(span_elements) == 2:
            cnt += 1
            print(f"alpha : {alpha}  / span 1")
            print(f"현재 위치 : {cnt}/{lenght}")
            print(f"남은 리스트 수 : {lenght-cnt}\n")
            end = time.time()
            if start != 0:
                print(f"다시 시작까지 걸린 시간 : {end-start}")
        elif len(span_elements) == 4:
            cnt += 1
            print(f"alpha : {alpha} / span 2")           
            print(f"현재 위치 : {cnt}/{lenght}")
            print(f"남은 리스트 수 : {lenght-cnt}\n")
            end = time.time()
            if start != 0:
                print(f"다시 시작까지 걸린 시간 : {end-start}")
        elif len(span_elements) == 6:
            cnt += 1
            print(f"alpha : {alpha} / span 3")
            print(f"현재 위치 : {cnt}/{lenght}")
            print(f"남은 리스트 수 : {lenght-cnt}\n")
            end = time.time()
            if start != 0:
                print(f"다시 시작까지 걸린 시간 : {end-start}")
                
    create_tabel()
    #테이블 생성은 나중에 하나로 모아서
    insert_data('over_6', follower_over_6)
    insert_data('over_9', follower_over_9)
    
    return follower_over_6, follower_over_9
    
def get_alpha_follow(alphas, driver, scroll_inc, verbose=1, wait=2, limit=float('inf')):
    """ get the following or followers of a list of alpha """
    alpha_followings = []
    for alpha in alphas:
        
        '''
        # if the login fails, find the new log in button and log in again.
        if check_exists_by_link_text("Log in", driver):
            print("Login failed. Retry...")
            login = driver.find_element(By.LINK_TEXT, "Log in")
            sleep(random.uniform(wait - 0.5, wait + 0.5))
            driver.execute_script("arguments[0].click();", login)
            sleep(random.uniform(wait - 0.5, wait + 0.5))
            sleep(wait)
            log_in(driver, wait)
            sleep(wait)
        # case 2 
        if check_exists_by_xpath('//input[@name="session[username_or_email]"]', driver):
            print("Login failed. Retry...")
            sleep(wait)
            log_in(driver, wait)
            sleep(wait)
        '''
        print("Crawling " + alpha + " " + 'following')
        driver.get('https://twitter.com/' + alpha + '/' + 'following')
        sleep(random.uniform(wait - 0.5, wait + 0.5))
        # check if we must keep scrolling
        follows_elem = []
        scroll_amount = scroll_inc
        
        while True:
            primaryColumn = driver.find_element(By.XPATH, '//div[contains(@data-testid,"primaryColumn")]')
            # extract only the Usercell
            page_cards = primaryColumn.find_elements(By.XPATH, '//div[contains(@data-testid,"UserCell")]')
            for card in page_cards:
                # get the following or followers element
                element = card.find_element(By.XPATH, './/div[1]/div[1]/div[1]//a[1]')
                follow_elem = element.get_attribute('href')
                # append to the list
                elem = str(follow_elem).split('/')[-1]
                follows_elem.append(elem)

            del follows_elem[-3:]
            
            driver.execute_script(f"window.scrollTo(0, {scroll_amount});")

            # 일시적인 대기 (내용 로딩을 기다리기 위해)
            sleep(0.5)
            
            scroll_amount += scroll_inc

            # 스크롤바가 끝에 다다랐을 경우 종료
            if scroll_amount >= driver.execute_script("return document.documentElement.scrollHeight"):
                break
        follows_elem = list(set(follows_elem))
        alpha_followings.extend(follows_elem)
        
    follows_alphas = {}
    for ele in alpha_followings:
        if ele not in follows_alphas:
            follows_alphas[ele] = 1
            print(f"new count is : {ele}")
        else:
            follows_alphas[ele] += 1
            print(f"{ele} count is : {follows_alphas[ele]}") 
            
    # follows_alphas가 딕셔너리인 경우
    follows_alphas = {key: value for key, value in follows_alphas.items() if value != 1}

    make_json(follows_alphas, 'duplicate list', 2)
    
    '''
    for ele in follows_elem:
        if ele not in follows_alphas:
            follows_alphas[ele] = 1
            print(f"new count is : {ele}")
        else:
            follows_alphas[ele] += 1
            print(f"{ele} count is : {follows_alphas[ele]}")
                
    print(f"follows_elem len : {len(follows_elem)}\n")    
        
    print(follows_alphas)
    abc = list(set(abc))
    print(f"len of abc : {len(abc)}")
    print(f"len before set : {len(follows_elem)}")
    follows_elem = list(set(follows_elem))
    print(f"len after set : {len(follows_elem)}\n")
    
    for key, value in follows_alphas.items():
        if value >= 9:
            follows_over_9[key] = value
        elif value >= 6:
            follows_over_6[key] = value
    print(f"follows over 6 is {len(follows_over_6)}\n")
    print(f"follows over 9 is {len(follows_over_9)}")

    return (follows_over_6, follows_over_9)
    '''

def create_tabel():
    conn = sqlite3.connect("following_list.db")
    cursor = conn.cursor()
    
    cursor.execute('CREATE TABLE IF NOT EXISTS over_6 (twitter_handle TEXT PRIMARY KEY, follower_count INT)')  
    cursor.execute('CREATE TABLE IF NOT EXISTS over_9 (twitter_handle TEXT PRIMARY KEY, follower_count INT)')
    
    conn.commit
    conn.close
    
def insert_data(path, data):
    conn = sqlite3.connect("following_list.db")
    cursor = conn.cursor()
    print(path)
    if data != None:
        for key, value in data.items():
            print(key, value)
            cursor.execute('INSERT OR IGNORE INTO {} (twitter_handle, follower_count) VALUES (?, ?)'.format(path), (key, value))
      
    conn.commit
    conn.close
    
def check_duplicate(list):

    duplicates = []
    seen = set()

    for item in list:
        if item in seen:
            duplicates.append(item)
        else:
            seen.add(item)

    print("중복된 문자열:", duplicates)

def make_json(followings, file_path, indent_num=None):
    
    if file_path == None:
        file_path = 'output/' +  'Alpha_followings.json'
    else:
        file_path = 'output/' + f'{file_path}.json'

    with open(file_path, 'w') as f:
        json.dump(followings, f, indent=indent_num)
        print(f"file saved in {file_path}")

def find_with_multiprocess(email, pw, username, data):
    driver = webdriver.Chrome(options=chrome_options2)
    log_in(driver, email, pw, username)
    print(f"len of data in find_with_multi : {len(data)}")
    follow_over_6, follow_over_9 = find_num_of_follower(driver, data)
    print(f"이게 6명 이상 : {follow_over_6}\n")
    print(f"이게 9명 이상 : {follow_over_9}\n")

def start():
    email = os.getenv("TWITTER_EMAIL").split(",")
    pw = os.getenv("TWITTER_PW").split(",")  
    username = os.getenv("TWITTER_USERNAME").split(",") 
    
    with open("output\Alpha_followings.json", 'r') as f:
        json_data = json.load(f)
    
    total = len(json_data)
    id_len = 2#len(email)
 
    quotient = total // id_len
    remainder = total % id_len

    variables = [{} for _ in range(id_len)]
    start = 0
    for i in range(id_len):
        end = start + quotient
        if i < remainder:
            end += 1
        variables[i] = json_data[start:end]
        start = end

    accounts = []
    for num in range(0, id_len):
        accounts.append({"email": email[num], "pw": pw[num], "username": username[num], "data": variables[num]})
    start = time.time()
    processes = []
    for account in accounts:
        process = multiprocessing.Process(target=find_with_multiprocess, args=(account["email"], account["pw"], account["username"], account["data"]))
        print(account)
        print(process)
        print("\n")
        processes.append(process)
        process.start()
        
    for process in processes:
        process.join()
    end = time.time()
    print(f"전체 걸린 시간 : {end-start}")
'''
    """
    #follower는 alpha 전체가 follow 하는 계정들
    window_height = driver.execute_script("return window.innerHeight")
    print(window_height)
    scroll_inc = window_height
    alpha_followings = get_alpha_follow(alpha_lists_test_2, driver, scroll_inc, verbose=1, wait=2, limit=50)
    print(len(alpha_followings))
    make_json(alpha_followings, file_path=None)
    end_time = time.time()
    print(f"first time : {end_time-start_time}")
    """
    with open("output\Alpha_followings.json", 'r') as f:
        json_data = json.load(f)
    
    start_time_m = time.time()
    follow_over_6, follow_over_9 = find_num_of_follower(driver, json_data)
    end_time_m = time.time()
    print(follow_over_6, follow_over_9)
    print(f"find num of all follow : {end_time_m-start_time_m}")
    
    end_time2 = time.time()
    print(f"all end time : {end_time2-start_time2}")
'''
def count_duplicate(alphas, driver, scroll_inc, verbose=1, wait=2, limit=float('inf')):
    """ get the following or followers of a list of alpha """
    alpha_followings = []
    for alpha in alphas:

        print("Crawling " + alpha + " " + 'following')
        driver.get('https://twitter.com/' + alpha + '/' + 'following')
        sleep(random.uniform(wait - 0.5, wait + 0.5))
        # check if we must keep scrolling
        follows_elem = []
        scroll_amount = scroll_inc
        
        while True:
            primaryColumn = driver.find_element(By.XPATH, '//div[contains(@data-testid,"primaryColumn")]')
            # extract only the Usercell
            page_cards = primaryColumn.find_elements(By.XPATH, '//div[contains(@data-testid,"UserCell")]')
            for card in page_cards:
                # get the following or followers element
                element = card.find_element(By.XPATH, './/div[1]/div[1]/div[1]//a[1]')
                follow_elem = element.get_attribute('href')
                # append to the list
                elem = str(follow_elem).split('/')[-1]
                follows_elem.append(elem)

            del follows_elem[-3:]
            
            driver.execute_script(f"window.scrollTo(0, {scroll_amount});")

            # 일시적인 대기 (내용 로딩을 기다리기 위해)
            sleep(0.5)
            
            scroll_amount += scroll_inc

            # 스크롤바가 끝에 다다랐을 경우 종료
            if scroll_amount >= driver.execute_script("return document.documentElement.scrollHeight"):
                break
        follows_elem = list(set(follows_elem))
        alpha_followings.extend(follows_elem)
        
    follows_alphas = {}
    
    for ele in alpha_followings:
        if ele not in follows_alphas:
            follows_alphas[ele] = 1
            print(f"new count is : {ele}")
        else:
            follows_alphas[ele] += 1
            print(f"{ele} count is : {follows_alphas[ele]}") 
            
    # follows_alphas가 딕셔너리인 경우
    follows_alphas = {key: value for key, value in follows_alphas.items() if value != 1}

    make_json(follows_alphas, 'duplicate list', 2)
   
def start2():
    
    driver = webdriver.Chrome(options=chrome_options2)
    log_in(driver, wait=2)

    start_time = time.time()
    start_time2 = time.time()
    
    #follower는 alpha 전체가 follow 하는 계정들
    window_height = driver.execute_script("return window.innerHeight")
    scroll_inc = window_height
    count_duplicate(alpha_lists_test_2, driver, scroll_inc, verbose=1, wait=2, limit=50)

if __name__ == '__main__':
    start()