# GPT 간단 챗봇 (Streamlit)

## 로컬 실행
```bash
pip install -r requirements.txt
streamlit run app.py
```

## API 키
- 배포 시: Streamlit Cloud > App > Settings > Secrets 에 `OPENAI_API_KEY="sk-..."` 저장
- 로컬 테스트 시: 실행 화면의 "관리자 설정"에서 임시로 입력 가능(세션에만 저장)

## 배포(Streamlit Community Cloud)
1) 이 폴더를 GitHub에 푸시
2) Streamlit Cloud에서 New app > repo 선택 > Deploy
3) App > Settings > Secrets 에 키 저장

## 주의
- 개인/민감정보는 입력 금지
- OpenAI API 키는 절대 코드/깃에 노출 금지