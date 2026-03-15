import uvicorn
import os

# '플래시 디베이트 아레나' 메인 실행 파일
if __name__ == "__main__":
    # app.py의 app 인스턴스를 8000포트에서 실행합니다.
    # reload=True 설정으로 코드 수정 시 자동 재시작이 가능합니다.
    print("🏟️ The Flash-Debate Arena 서버를 시작합니다...")
    print("접속 주소: http://127.0.0.1:8000")
    
    uvicorn.run(
        "app:app", 
        host="127.0.0.1", 
        port=8000, 
        reload=True
    )
