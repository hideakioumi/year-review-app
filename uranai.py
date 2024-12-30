import streamlit as st
import google.generativeai as genai

# =========================================
# Streamlitアプリ用 サンプルコード (Secrets管理)
# =========================================

# 0. APIキーの取得 (Secretsから)
#   1) Streamlit CloudのダッシュボードでSecretsを設定したうえで
#   2) st.secrets["API_KEY"] を呼び出す
GOOGLE_API_KEY = st.secrets["API_KEY"]  

genai.configure(api_key=GOOGLE_API_KEY)

# 1. Geminiモデルの設定
model = genai.GenerativeModel("gemini-2.0-flash-exp")

# 2. 質問リスト
questions = [
    "今年1年を振り返って、「自分らしく過ごせた」と思える瞬間はいつでしたか？そのとき、心や身体の調子はどう感じていましたか？",
    "逆に、どんなときに疲れやすくなったり、気分が落ちたりしたと感じましたか？そのとき、姿勢や呼吸、体の使い方に何か気になることはありましたか？",
    "今年意識して続けていた習慣やルーティンはありますか？それによって、身体的あるいは精神的にどんな変化がありましたか？",
    "1年を通じて、一番「リラックス」できた時間や場所はどこでしたか？",
    "来年はどんな自分でいたいですか？ そのために身体面・心の面で意識したいことがあれば教えてください。"
]

# 3. システムプロンプト
system_prompt = (
    "あなたは「偏りを発見するカウンセラー」であり、野口整体の専門家です。"
    "1. 役割・目的 あなたの役割は、ユーザーが年末に振り返った内容（身体の使い方、心の動き、日常習慣など）から、野口整体でいう「体癖（たいへき）」..."
    "...(以下、長い文章は省略)..."
)

# Streamlit 画面レイアウト
st.title("来年の運勢占い 〜野口整体風〜")
st.write("以下の質問に回答して、『占い結果を見る』ボタンを押してみてください。")

# ユーザーの回答を入力フォームで受け取る
user_answers = {}
for i, question in enumerate(questions):
    user_answers[f"answer{i+1}"] = st.text_area(f"Q{i+1}. {question}", key=f"answer_{i+1}")

# 「占い結果を見る」ボタン
if st.button("占い結果を見る"):
    # ユーザープロンプトの作成
    user_prompt = "以下の質問に対するユーザーの回答をもとに、来年の運勢を占ってください。\n\n"
    for i, question in enumerate(questions):
        user_prompt += f"質問{i+1}: {question}\n"
        user_prompt += f"回答{i+1}: {user_answers[f'answer{i+1}']}\n"
    user_prompt += "\n占いの結果:"

    # システムプロンプトとユーザープロンプトを結合
    full_prompt = system_prompt + "\n\n" + user_prompt

    st.write("占い中です。少々お待ちください...")

    # Gemini APIにリクエストを送信
    response = model.generate_content(full_prompt)

    # 結果を表示
    st.subheader("占いの結果")
    st.write(response.text)
