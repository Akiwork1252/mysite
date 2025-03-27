import json
import os
import re

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

# 学習トピック作成
def ai_generate_learning_task(title, current_level='', target_level=''):

    client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

    prompt = f'''
以下の<ユーザー入力>と<作成ルール>に基づいて学習タスクを生成してください。
<ユーザー入力>
タイトル:{title}
現在のレベル:{current_level}
目標到達レベル:{target_level}
<作成ルール>
1,出力例のように、JSON形式のデータで生成してください。
2,sub_topicは、学習時間が長くならないように、できるだけ細分化してください。(1時間以内)
3,タイトル以外は入力が任意です。空でも無視してください。
<出力例>
[
  {{
    "main_topic": "Python基本文法",
    "sub_topics": [
      {{
        "sub_topic": "Python基本文法(変数)"
      }},
      {{
        "sub_topic": "Python基本文法(データ型)"
      }}
    ]
  }},
  {{
    "main_topic": "Python基本構文",
    "sub_topics": [
      {{
        "sub_topic": "Python基本構文(if文)"
      }}
    ]
  }}
]
'''

    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {'role': 'system', 'content': 'あなたは数学者です。'},
            {'role': 'user', 'content': prompt}
        ],
        max_tokens=1000,
        temperature=0.7
    )

    raw_content = response.choices[0].message.content.strip()

    # 不要な出力を削除
    raw_content = raw_content.replace('```json', '').replace('```', '').strip()

    if not raw_content:
        print('AIから空のレスポンスが返されました。')
        return []
    
    # 正規表現でJSON部分を抽出
    json_match = re.search(r'\[.*\]', raw_content, re.DOTALL)

    if not json_match:
        print('JSONデータが見つかりませんでした。')
        generated_topic = []
    else:
        # JSON部分を解析
        json_str = json_match.group(0)
        try:
            generated_topic = json.loads(json_str)
        except json.JSONDecodeError:
            print('JSONの解析に失敗しました。')
            generated_topic = []

    return generated_topic
        


if __name__ == '__main__':
    title = 'Python株価予測'
    current_level = 'Python未経験'
    target_level = ''
    generate_learning_topic(title, current_level)
