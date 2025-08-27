import streamlit as st
from openai import OpenAI
import os
from datetime import datetime

st.set_page_config(page_title="GPT 간단 챗봇", page_icon="💬", layout="centered")

# ----- 사이드바: 간단 사용법 -----
with st.sidebar:
    st.header("사용법")
    st.markdown("""    1) 아래 입력창에 질문을 적고 엔터를 누르세요.
2) 개인정보(실명/전화/학번 등)는 입력하지 마세요.
3) 중요한 결정은 공식 자료로 다시 확인하세요.
""")
    st.caption("이 대화는 이 접속 세션에서만 유지됩니다.")

# ----- API 키 로딩 (Secrets > ENV > 임시 입력) -----
api_key = st.secrets.get("OPENAI_API_KEY") if "OPENAI_API_KEY" in st.secrets else os.getenv("OPENAI_API_KEY")
if not api_key:
    with st.expander("관리자 설정(임시 테스트용)"):
        st.info("배포 후에는 Streamlit Secrets에 키를 넣어주세요. 여기 입력은 현재 브라우저 세션에만 보관됩니다.")
        _tmp = st.text_input("OpenAI API 키(임시)", type="password")
        if _tmp: api_key = _tmp
if not api_key:
    st.stop()

client = OpenAI(api_key=api_key)

# ----- 초기 메시지 -----
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful, concise AI assistant. If the user's message is in Korean, reply in Korean."}
    ]

st.title("💬 GPT 간단 챗봇")

# 기존 대화 렌더
for m in st.session_state.messages:
    if m["role"] != "system":
        with st.chat_message("assistant" if m["role"]=="assistant" else "user"):
            st.markdown(m["content"])

user_input = st.chat_input("무엇이든 물어보세요!")

def ask_gpt(q: str):
    history = [m for m in st.session_state.messages][-8:] + [{"role":"user","content":q}]
    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=history,
        temperature=0.7,
        max_tokens=500
    )
    return res.choices[0].message.content.strip()

if user_input:
    st.session_state.messages.append({"role":"user","content":user_input})
    with st.chat_message("user"): st.markdown(user_input)
    with st.chat_message("assistant"):
        with st.spinner("응답 생성 중..."):
            try:
                ans = ask_gpt(user_input)
            except Exception as e:
                ans = f"오류가 발생했습니다: {e}"
            st.markdown(ans)
    st.session_state.messages.append({"role":"assistant","content":ans})

st.caption(f"ⓘ 마지막 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M')}")