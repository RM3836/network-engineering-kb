import requests
import pandas as pd
import time
import random
import re
from requests.exceptions import RequestException

# -------------------------- 配置项（适配原项目逻辑） --------------------------
# 替换为有效Cookie（从浏览器m.weibo.cn获取）
COOKIE = 'SCF=ApW3ofaFvU-ht7ATWIVLr9RBPCU8iag8oVajn6_9aIGp-AcUjUuIxTFLPCSXS7OgtM2THQmO-jdwQ8sDJCwJGPc.; SUB=_2A25EXgtQDeRhGe9P6lYQ8SnJzzyIHXVnEgKYrDV8PUNbmtAbLWPVkW9NdMTF6GrzuYU8Em_b8Dagqm5kbcrOGNjO; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWxuuqp_gmSX7viQhhpLjUX5NHD95Q4eK2XeK2NSKB7Ws4DqcjMi--NiK.Xi-2Ri--ciKnRi-zN1K2pSh2pS0-Xe5tt; ALF=02_1770129408; SINAGLOBAL=6657173873401.803.1767537410716; ULV=1767537410718:1:1:1:6657173873401.803.1767537410716:; PC_TOKEN=34b7f817a8; XSRF-TOKEN=tLJ4eti2AriSfQVoun2SPGhO; WBPSESS=eNIzJ6Er9uPT7vfqaF4QTn_c5kC4AR7uBwxOqKKELDVF7LIZp7TeatXPTFXbVruQ1mz7llrxi-U8vDMggF6hgeiUW3jE_wuelQuRXIk_tnZ9T18xmHNqbl3n8atOtA9Q6Ezngo3vRIKCFyowax5rDg=='
# 原项目核心URL（统一使用type=1的containerid，保证数据结构一致）
BASE_URL = 'https://m.weibo.cn/api/container/getIndex'
PARAMS = {
    'containerid': '100103type=1&q=机票',  # 统一type=1，和翻页URL保持一致
    'page_type': 'searchall',
    'page': 1  # 初始页数
}
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Cookie': COOKIE.encode('utf-8').decode('latin-1'),  # 手动转码，解决编码问题
    'Referer': 'https://m.weibo.cn/',
    'X-Requested-With': 'XMLHttpRequest'
}


TEXT_PATTERN = re.compile(r'[A-Za-z0-9\!\%\[\]\,\。\<\=\"\:\/\?\&\-\>\_\;]+')

# -------------------------- 核心函数 --------------------------
def clean_text(text):
    """清洗文本，处理空值"""
    if not text:
        return ""
    return TEXT_PATTERN.sub("", text).strip()

def crawl_page(page_num):
    """爬取单页数据"""
    # 更新页数参数
    PARAMS['page'] = page_num
    try:
        # 随机延迟1-3秒，模拟人工翻页
        time.sleep(random.uniform(1, 3))
        response = requests.get(
            url=BASE_URL,
            params=PARAMS,
            headers=HEADERS,
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except RequestException as e:
        print(f"第{page_num}页请求失败：{str(e)}")
        return None

# -------------------------- 主程序 --------------------------
if __name__ == "__main__":
    columns = ['网名', '国家', '省会', '城市', '手机终端', '文本']
    df = pd.DataFrame(columns=columns)
    total_pages = 20  # 原项目提的100页大概率超限，先爬20页测试
    empty_page_count = 0  # 空页计数，连续3页空则停止
    
    for page_num in range(1, total_pages + 1):
        print(f"\n===== 开始爬取第{page_num}页 =====")
        json_data = crawl_page(page_num)
        
        # 1. 检查接口返回是否有效
        if not json_data or 'data' not in json_data:
            print(f"第{page_num}页无有效数据")
            empty_page_count += 1
            if empty_page_count >= 3:
                print("连续3页无数据，停止爬取")
                break
            continue
        
        card_list = json_data['data'].get('cards', [])
        if not card_list:
            print(f"第{page_num}页无cards数据")
            empty_page_count += 1
            if empty_page_count >= 3:
                print("连续3页无数据，停止爬取")
                break
            continue
        
        # 2. 提取当前页数据
        page_data = []
        for card in card_list:
            mblog = None
            # 适配原项目的card_group/mblog两种结构
            if 'card_group' in card and card['card_group']:
                mblog = card['card_group'][0].get('mblog')
            elif 'mblog' in card:
                mblog = card.get('mblog')
            
            if not mblog:
                continue  # 无微博数据则跳过
            
            # 提取字段（全空值保护）
            screen_name = mblog.get('user', {}).get('screen_name', '')
            country = mblog.get('status_country', '')
            province = mblog.get('status_province', '')
            city = mblog.get('status_city', '')
            source = mblog.get('source', '')
            text = clean_text(mblog.get('text', ''))
            
            page_data.append([screen_name, country, province, city, source, text])
        
        # 3. 添加到DataFrame
        if page_data:
            empty_page_count = 0  # 重置空页计数
            page_df = pd.DataFrame(page_data, columns=columns)
            df = pd.concat([df, page_df], ignore_index=True)
            print(f"第{page_num}页成功提取{len(page_data)}条数据")
        else:
            print(f"第{page_num}页无可用微博数据")
            empty_page_count += 1
            if empty_page_count >= 3:
                print("连续3页无数据，停止爬取")
                break
    
    # 4. 保存数据（UTF-8编码避免中文乱码）
    df.to_csv('微博机票相关数据.csv', index=False, encoding='utf-8-sig')
    print(f"\n爬取完成！总计获取{len(df)}条有效数据")
    print("前5条数据预览：")
    print(df.head())

from sqlalchemy import create_engine



engine = create_engine('mysql+pymysql://root:123456@localhost:3306/weibo')

# 写入MySQL
df.to_sql(
    name='weibo_ticket_data',  # MySQL里的表名
    con=engine,
    if_exists='replace',
    index=False
)
print("数据已经成功导入MySQL数据库！")

import jieba
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt

# 读取数据
df=pd.read_csv('微博机票相关数据.csv', encoding='utf-8-sig')
texts=df['文本'].dropna().tolist()

# 预处理
stopwords=set(pd.read_csv('stopwords.txt', header=None)[0].tolist())
def clean_text(text):
    # 修复正则表达式（加re.sub）
    text = re.sub(r'http\S+|@\w+|#\w+', '', str(text)).strip()
    words = jieba.lcut(text)
    return [w for w in words if len(w)>=2 and w not in stopwords]

# 词频统计
all_words = []
for text in texts:
    all_words.extend(clean_text(text))
word_freq=Counter(all_words).most_common(20)

# 可视化
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.figure(figsize=(12,6))
words = [w[0] for w in word_freq]
counts = [w[1] for w in word_freq]
plt.bar(words, counts)
plt.title('机票舆情TOP20热词')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()




