import streamlit as st
from openai import OpenAI
import os
from datetime import datetime

st.set_page_config(page_title="어르니 GPT", page_icon="💬", layout="centered")

# ===== 시스템 프롬프트 =====
SYSTEM_PROMPT = (
    "You are a friendly, concise AI assistant. "
    "If the user's message is in Korean, reply in Korean. "
    "Keep answers clear and helpful for general users."
)

# ===== API 키 로딩 =====
def load_api_key():
    try:
        if "OPENAI_API_KEY" in st.secrets:
            return st.secrets["OPENAI_API_KEY"]
    except Exception:
        pass
    key = os.getenv("OPENAI_API_KEY")
    if key:
        return key
    with st.expander("관리자 설정 (임시 테스트)"):
        st.info("배포 후에는 Settings → Secrets에 키를 넣어주세요. 여기 입력은 이 브라우저 세션에만 보관됩니다.")
        tmp = st.text_input("OpenAI API 키(임시)", type="password")
        if tmp:
            return tmp
    return None

api_key = load_api_key()
if not api_key:
    st.stop()

client = OpenAI(api_key=api_key)

# ===== 세션 초기화 =====
def init_messages():
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

if "messages" not in st.session_state:
    init_messages()

# ===== 상단 헤더 =====
st.markdown("<h1 style='text-align:center;margin-bottom:10px;'>어르니 GPT</h1>", unsafe_allow_html=True)
st.caption("간단하고 편한 AI 도우미 (개인정보 입력은 피해주세요)")

# ===== 모드 선택 =====
st.markdown("### 사용 모드 선택")
mode = st.radio(
    "모드",
    options=["빠르고 가벼움 (추천)", "정확하고 깊게"],
    index=0,
    help="상황에 맞게 선택하세요. 필요하면 언제든 바꿀 수 있어요."
)

if mode.startswith("빠르고"):
    model_name = "gpt-5-nano"
    max_tokens = 1000
else:
    model_name = "gpt-5"
    max_tokens = 2000

# ===== GPT 호출 함수 =====
def ask_gpt(q: str):
    history = [m for m in st.session_state.messages][-8:] + [{"role": "user", "content": q}]
    resp = client.chat.completions.create(
        model=model_name,
        messages=history,
        max_completion_tokens=max_tokens  # gpt-5 계열은 이걸 사용
    )
    text = resp.choices[0].message.content.strip() if resp.choices else "응답 없음"
    used_model = getattr(resp, "model", model_name)
    return text, used_model

# ===== 사이드바 =====
with st.sidebar:
    st.header("도움말")
    st.markdown(
        "- 아래 입력창에 그냥 궁금한 것을 적고 엔터를 누르시면 됩니다.\n"
        "- 개인정보(이름/전화/주소 등)는 되도록 넣지 말아주세요.\n"
        "- 중요한 결정은 공식 자료로 다시 확인해주세요.\n"
    )
    st.divider()
st.subheader("💡 예시 질문")

if st.button("오늘 뭐 해먹지?"):
    q = "냉장고에 재료가 별로 없을 때 간단히 만들 수 있는 저녁 메뉴 추천해줘."
    st.session_state.messages.append({"role": "user", "content": q})
    try:
        ans, used_model = ask_gpt(q)
    except Exception as e:
        ans, used_model = f"오류가 발생했습니다: {e}", model_name
    st.session_state.messages.append({"role": "assistant", "content": ans})
    st.rerun()   # ✅ 화면 갱신해서 채팅창에 바로 보이게

if st.button("오늘 날씨 어때?"):
    q = "오늘 대한민국 주요 도시의 날씨를 알려줘."
    st.session_state.messages.append({"role": "user", "content": q})
    try:
        ans, used_model = ask_gpt(q)
    except Exception as e:
        ans, used_model = f"오류가 발생했습니다: {e}", model_name
    st.session_state.messages.append({"role": "assistant", "content": ans})
    st.rerun()   # ✅ rerun으로 즉시 채팅창 반영


# ===== 이전 대화 렌더 =====
for m in st.session_state.messages:
    if m["role"] != "system":
        with st.chat_message("assistant" if m["role"] == "assistant" else "user"):
            st.markdown(m["content"])

# ===== 입력창 =====
user_input = st.chat_input(
    placeholder="무엇이든 물어보세요! 예) 감기 기운 있을 때 집에서 할 수 있는 관리 방법은?"
)

# ===== 입력 처리 =====
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"): st.markdown(user_input)
    with st.chat_message("assistant"):
        with st.spinner("생각 중…"):
            try:
                ans, used_model = ask_gpt(user_input)
            except Exception as e:
                ans, used_model = f"오류가 발생했습니다: {e}", model_name
            st.markdown(ans)
            st.caption(f"모델: `{used_model}`")
    st.session_state.messages.append({"role": "assistant", "content": ans})

# ===== 푸터 =====
st.caption(f"ⓘ 마지막 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
