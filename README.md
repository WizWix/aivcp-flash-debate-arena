# 🏟️ The Flash-Debate Arena (플래시 디베이트 아레나)

Gemini 1.5 Flash / 2.5 Flash Lite의 초고속 추론 능력과 **Google Search Grounding** 기술을 결합한 실시간 AI 토론 플랫폼입니다. 단순히 묻고 답하는 챗봇을 넘어, 개성 뚜렷한 3명의 AI 페르소나가 사용자의 의견과 치열하게 맞붙으며, 중재자가 실시간으로 팩트체크를 수행합니다.

## ✨ 주요 기능

- **3인의 AI 페르소나 (Multi-Persona)**
  - **논리 술사 (The Philosopher)**: 이성적이고 철학적인 관점, 인문학적 식견을 담은 차분한 논리.
  - **혼돈의 사도 (The Chaos Agent)**: 상식 파괴, 도발적이고 유머러스한 관점, 파격적인 비유.
  - **데이터 가디언 (The Scientist)**: 철저한 통계와 과학적 근거 중심, 객관적이고 냉철한 분석.
- **실시간 중재자 (The Arbiter - Fact Checker)**
  - **Google Search Grounding**을 활용하여 AI와 사용자의 주장을 실시간 검색 결과와 대조합니다.
  - 주장의 사실 여부를 확인하고 근거 자료를 제시하여 토론의 신뢰도를 높입니다.
- **배치 처리 & 최적화 (Batching Optimization)**
  - 한 번의 API 호출로 3명의 답변을 동시에 생성하여 API 할당량을 절약하고 응답 속도를 극대화했습니다.
- **프리미엄 UI/UX**
  - **Glassmorphism** 디자인과 다이내믹한 애니메이션 적용.
  - 각 페르소나별 전용 아바타와 상태 바(Energy Bar)를 통해 생동감 있는 토론 현장 연출.

## 🚀 시작하기

### 1. 환경 설정
프로젝트 루트 폴더에 `.env` 파일을 생성하고 Gemini API 키를 입력하세요.
```env
GEMINI_API_KEY=your_api_key_here
```

### 2. 패키지 설치
```powershell
pip install fastapi uvicorn google-genai python-dotenv tenacity
```

### 3. 서버 실행
```powershell
python main.py
```
서버가 시작되면 브라우저에서 [http://localhost:8000](http://localhost:8000)으로 접속하세요.

## 📁 프로젝트 구조

- `app.py`: FastAPI 백엔드 및 Gemini SDK 연동 로직
- `main.py`: 서버 실행 진입점 (Uvicorn)
- `static/`: 프런트엔드 리소스 (HTML, CSS, JS, Avatars)
- `.env`: API 키 및 환경 변수 관리

## 🛠️ 기술 스택

- **Model**: Google Gemini 1.5 Flash / 2.5 Flash Lite
- **Backend**: Python, FastAPI, Tenacity (Retry logic)
- **Frontend**: Vanilla JS, CSS (Custom Animations)
- **Feature**: Google Search Grounding for real-time verification

---
*Powered by Google Gemini 2.5 Flash Lite & Advanced AI Engineering.*
