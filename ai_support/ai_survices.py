import json
import os
import re

from dotenv import load_dotenv
from openai import OpenAI
from langchain.chains.llm import LLMChain
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate



load_dotenv()

# タスク生成
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
            {'role': 'system', 'content': 'あなたは最適な学習プランを提案するAIアシスタントです。'},
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
        

# レクチャー生成
def lectures_by_ai(title, user_input):
    llm = ChatOpenAI(model='gpt-4o-mini', temperature=0.7, max_completion_tokens=1000,)

    prompt_text = (
        'あなたは優秀な教師です。以下のタイトルに基づいて講義を行なってください。\n'
        'タイトル:{title}\n'
        '出力は以下のルールに基づいて行なってください。'
        '<ルール>\n'
        '1,講義前にトピックを列挙して、改行を入れる。'
        '2,１つのトピックを説明したら改行を入れる'
        '3,pythonなどのコードを入れる場合は、改行を入れてから、python:〜として始める'
    )

    prompt_template = ChatPromptTemplate.from_template(prompt_text)
    print(f'prompt_template: {prompt_template}')
    prompt = prompt_template.format_prompt(title=title, user_input=user_input)
    print(f'prompt: {prompt}')

    response = llm.invoke(prompt.to_string())
    print(f'response: {response}')
    print(f'return: {response.content}')

    if not response.content.strip():
        return '問題が発生しました。'
    
    return response.content


# 問題生成(選択式)
def generate_multipul_choice_question(title, previous_question=''):
    llm = ChatOpenAI(model='gpt-4o-mini', temperature=0.7, max_completion_tokens=1000)
    
    if previous_question:
        prompt_text = (
            'あなたは優秀な教師です。以下のタイトルに関する選択問題を1問生成してください。'
            '前回の問題と内容が重複しないようにしてください。\n'
            'タイトル:{title}\n'
            '前回の問題:{previous_question}\n'
            '出力例のように改行を入れて出力してください。(必須)\n'
            '<出力例>'
            'Question: 生成した問題\n'
            'a): 生成した選択肢\n'
        )
    else:
        prompt_text = (
            'あなたは優秀な教師です。以下のタイトルに関する選択問題を1問生成してください。'
            'タイトル:{title}\n'
            '出力例のように改行を入れて出力してください。(必須)\n'
            '<出力例>'
            'Question: 生成した問題\n'
            'a): 生成した選択肢\n'
        )

    prompt_template = ChatPromptTemplate.from_template(prompt_text)
    prompt = prompt_template.format_prompt(title=title, previous_question=previous_question)
    response = llm.invoke(prompt.to_string())
    print(f'response: {response}')
    print(f'return: {response.content}')

    return response.content


# 採点(選択問題)
def grade_multiple_choice_question(question, answer):
    print(f'Question: {question}\nAnswer: {answer}')

    prompt_text = (
        'あなたは優秀な教師です。以下は出題された選択問題とユーザーの回答です。\n'
        'Question:{question}\n'
        'Answer:{answer}\n'
        '採点は、正解:2pt、不正解:0ptとし、float型で返してください。\n'
        'スコアと解説を出力例のように辞書型のみで出力してください(必須)。\n'
        '出力例:{{"score": スコア, "explanation": 解説}}'
    )

    prompt_template = ChatPromptTemplate.from_template(prompt_text)
    llm = ChatOpenAI(model='gpt-4o-mini', temperature=0.2)
    chain = LLMChain(prompt=prompt_template, llm=llm)

    response = chain.invoke({
        'question': question,
        'answer': answer
    })

    # AIの出力を辞書型に変換
    try:
        result = json.loads(response['text'])
    except json.JSONDecodeError:
        raise ValueError(f'AIの出力を辞書型に変換できません。')
    
    # 出力が辞書型か確認
    if not isinstance(result, dict):
        raise ValueError(f'AIの出力が辞書型ではありません。{result}')

    # 辞書に必要なキーが含まれているか確認
    required_keys = ['score', 'explanation']
    for key in required_keys:
        if key not in result:
            raise KeyError(f'必要なキー {key} が出力に含まれていません。')
    
    # scoreがfloat型か確認
    if not isinstance(result.get('score'), float):
        try:
            result['score'] = float(result['score'])
        except (TypeError, ValueError):
            raise ValueError(f'scoreの値をfloat型に変換できません。: {result["score"]}')

    print(f'return: {result}')

    return result


# 問題生成(記述式)
def generate_constructed_question(title):
    llm = ChatOpenAI(model='gpt-4o-mini', temperature=0.7, max_completion_tokens=1000)
    prompt_text = (
        'あなたは優秀な教師です。以下のタイトルに関する記述問題を生成してください。'
        'プログラミングの場合は、コーディング問題を生成してください。'
        'タイトル:{title}\n'
        '出力例\n'
        'Question: 生成した問題\n'
    )
    prompt_template = ChatPromptTemplate.from_template(prompt_text)
    prompt = prompt_template.format_prompt(title=title)
    response = llm.invoke(prompt.to_string())
    print(f'response: {response}')
    print(f'return: {response.content}')

    return response.content


# 採点(記述問題)
def grade_constructed_question(question, answer):
    print(f'Question: {question}\nAnswer: {answer}')

    prompt_text = (
        'あなたは優秀な教師です。以下は出題された選択問題とユーザーの回答です。\n'
        'Question:{question}\n'
        'Answer:{answer}\n'
        'スコアと解説を出力例のように辞書型のみで出力してください(必須)。\n'
        '出力例:{{"score": スコア, "explanation": 解説}}\n' 
        'スコア:最大100ptとし、float型で返してください。\n'
        '解説:コーディング問題の場合は、以下の採点基準を元に採点を行い、改行を入れて読みやすく、詳細に記述してください。\n' 
        '採点基準:正確性(/40pt)、設計(/20pt)、読みやすさ(/20pt)、ベストプラクティス(/20pt)'
    )

    prompt_template = ChatPromptTemplate.from_template(prompt_text)
    llm = ChatOpenAI(model='gpt-4o-mini', temperature=0.2)
    chain = LLMChain(prompt=prompt_template, llm=llm)
    response = chain.invoke({
        'question': question,
        'answer': answer
    })

    # 出力を辞書型に変換
    try:
        result = json.loads(response['text'])
    except json.JSONDecodeError:
        raise ValueError(f'AIの出力を辞書型に変換できません。')
    
    # 出力が辞書型か確認
    if not isinstance(result, dict):
        raise ValueError(f'AIの出力が辞書型ではありません。: {result}')
    
    # 辞書に必要なキーが含まれているか確認
    required_keys = ['score', 'explanation']
    for key in required_keys:
        if not key in result:
            raise KeyError(f'必要なキー {key} が出力に含まれていません。')

    # scoreがfloat型か確認
    if not isinstance(result.get('score'), float):
        try:
            result['score'] = float(result['score'])
        except (TypeError, ValueError):
            raise ValueError(f'scoreの値をfloat型に変換できません。: {result["score"]}')
    print(result)    
    
    return result

if __name__ == '__main__':
    title = 'Python基礎文法(ループ)'
    current_level = 'Python未経験'
    target_level = ''
    user_input = ''

    question = '''Pythonでforループを使用して、リストの各要素を出力するための正しい構文はどれですか
a): for item in list: print(item)  
b): for (item in list) { print(item); }  
c): foreach item in list: print(item)  
d): for item: list print(item)  
'''
    question_2 = '''
Pythonを使用して、1から100までの整数の合計を計算するプログラムを作成してください。ただし、ループを使用して実装すること。合計を出力する際には、「合計は: 合計値」という形式で表示してください。
'''
    answer = 'a'
    answer_2 = '''
    result = 0
    for num in range(1, 101):
        result += num
    
    print(f'合計値: {result}')
'''
    grade_constructed_question(question_2, answer_2)
