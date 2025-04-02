import json
import os
import re

from dotenv import load_dotenv
from openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate



load_dotenv()

# ==== タスク作成 ====
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
    print(f'raw_content: {raw_content}')

    if not raw_content:
        print('AIから空のレスポンスが返されました。')
        return []
    
    # 正規表現でJSON部分を抽出
    json_match = re.search(r'\[.*\]', raw_content, re.DOTALL)

    if not json_match:
        print('JSONデータが見つかりませんでした。')
        generated_task = []
    else:
        # JSON部分を解析
        json_str = json_match.group(0)
        try:
            generated_task = json.loads(json_str)
        except json.JSONDecodeError:
            print('JSONの解析に失敗しました。')
            generated_task = []
    print(f'generated_task:  {generated_task}')

    return generated_task
        

# ==== 講義 ====
def lectures_by_ai(title, user_input):
    
    def get(self, request, *args, **kwargs):
        llm = ChatOpenAI(
            model='gpt-4o-mini',
            temperature=0.7,
            max_completion_tokens=1000,
        )

        prompt_template = ChatPromptTemplate.from_template(
            'あなたは優秀な教師です。以下のタイトルに基づいて講義を行なってください。\n'
            'タイトル:{title}\n'
            '出力は以下のルールに基づいて行なってください。'
            '<ルール>\n'
        )

    


if __name__ == '__main__':
    title = 'Python株価予測'
    current_level = 'Python未経験'
    target_level = ''
