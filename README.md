# doc-search-project
마일스톤으로 이번 KANT 시작 전 4주 프로젝트로 data/tech_docs.csv 하에 기술 문서 60건을 넘파이/판다스로 탐색하고 기초 통계를 하는 프로젝트로 1주차부터 4주차까지 쌓입니다. 
마일스톤에서 주마다 4개에서 5개의 문제를 주고 파이썬으로 풀고 깃허브 주소를 올리는 형식으로 구성이 되었는데 현재 문제를 확인이 안되어 1주차 피드백 내용을 바탕으로 요구 사항을 재구성 된 점 양해 부탁드립니다.
## 데이터 
 data/tech_docs.csv - 기술 문건이 60건,  doc_id, title, category, content, source 구성이 되어 있으며 카테고리는 Python, Git, AI기초, NumPy, pandas 5종입니다.
## 실행
프로젝트 루트에서 `python weekX/main.py`
`DATA_PATH`를 절대경로에서 상대경로 `data/tech_docs.csv`로 바꾸면서, 실행 위치가 프로젝트 루트가 아니면 CSV를 찾지 못하는 문제가 생겼습니다. 그래서 프로젝트 루트에서 실행하도록 했습니다. (VS Code 설정 쪽은 더 편한 방법을 찾아보겠습니다.)

============================================================================================

## 1주차에 받은 피드백 내용입니다. 

# 기능별 피드백

## 기능 1 — load_data
**받은 피드백**
- 함수명이 `function1`인데 명세는 `load_data()`
- `DATA_PATH`가 절대경로로 하드코딩되어 다른 환경에서 실행 불가
  
**수정내용**
- 이름: `function1` → `load_data`
- `DATA_PATH` 절대경로 → 상대경로 `data/tech_docs.csv`
- 함수 안에서 `DATA_PATH` 대신 인자 `file_path` 사용
- `main()`에서 `df = load_data(...)` 로 반환값 받기

## 기능 2 — explore_structure
**받은 피드백**
- `shape`, `columns`, `dtypes`, `head(5)`, `info()` 출력 항목은 모두 충족
- 함수명이 `function2`인데 명세는 `explore_structure(df)`
  
**수정내용**
- 이름: `function2` → `explore_structure`

## 기능 3 — show_category_distribution
**받은 피드백**
- `value_counts()`로 카테고리별 문서 수와 비율 출력, `unique()`로 고유 카테고리 추출하는 구조는 잘 구성됨
- 반복문과 딕셔너리로 카테고리별 평균 단어 수를 계산하라는 요구가 있었으나 dict에 저장하는 부분이 없음
- 함수가 dict를 반환해야 하는데 반환값 없음
- 변수 `cat`을 `value_counts()`용과 반복문용으로 동시에 사용해 첫 번째 값이 덮어씌워지는 버그

**수정내용**
- 이름: `function3` → `show_category_distribution`
- 사용하지 않는 `cat = df["category"].value_counts()` 줄 삭제
- 계산용 for문과 출력용 for문으로 분리, 결과를 `result` dict에 저장
- `return result` 추가

<img width="1035" height="459" alt="image" src="https://github.com/user-attachments/assets/1a4260be-b076-41f0-be30-592ee9675bc2" />


## 기능 4 — check_missing
**받은 피드백**
- `isnull().sum()`으로 컬럼별 결측치를 확인하고 비율에 따라 낮음/주의/높음으로 분기하는 핵심 로직은 잘 구현됨
- `df`를 인자로 받지 않고 내부에서 `pd.read_csv()`를 다시 호출함
- 결측치 없는 컬럼도 개별 출력됨 (명세는 목록으로 별도 출력)
- 결측치가 있는 컬럼은 개수와 비율(%)도 함께 출력해야 함

**수정내용**
- 이름: `function4` → `check_missing`
- `df`를 인자로 받도록 변경, 내부 `pd.read_csv()` 제거
- `clean_cols` 리스트에 모아 마지막에 한 줄로 출력
- `missing_cols` 리스트에 컬럼명·개수·비율·심각도를 dict로 담아 상세 출력

## 기능 5 — numpy_doc_stats
**받은 피드백**
- `dropna()` 후 단어 수 배열을 만들고 `ddof=1`로 표본표준편차를 계산한 점, `word_arr < 50` 조건 필터링은 정확히 구현됨
- 50단어 미만 문서를 찾을 때 단어 수 배열만 출력하고 문서 식별 정보(`doc_id`, `title`)가 없음
- pandas와 NumPy 수치가 일치하는지 명시적인 비교 메시지 필요

**수정내용**
- 이름: `function5` → `numpy_doc_stats`
- 조건식을 `short_doc_mask` 변수로 분리해 `word_arr`와 `df` 양쪽에 재사용
- 해당 문서의 `doc_id`, `title`을 출력하도록 변경
- pandas `std()`와 NumPy `std(ddof=1)` 비교 및 일치 여부 메시지 추가

## main()
**받은 피드백**
- `DATA_PATH` 상수를 상단에 선언하고 `if __name__ == '__main__':`으로 진입점을 명확히 한 점은 좋음
- `function4()`가 `df` 인자 없이 호출되어 내부에서 파일을 다시 읽는 구조
- 함수명이 명세와 달라 `main()`이 문서 역할을 못 함

**수정내용**
- 모든 함수명을 명세에 맞게 변경
- `df = load_data(DATA_PATH)`로 반환값 받도록 수정
- `check_missing(df)`로 인자 전달

<img width="546" height="272" alt="image" src="https://github.com/user-attachments/assets/09056616-db93-4f21-8b96-803b0d74c036" />

    
============================================================================================
위 받은 피드백을 제 나름대로 AI와 책을 토대로 수정을 하였지만 이 코드가 좋은 코드인지 판단이 아직 서지 않아 튜터님께 다시 피드백을 요청 드립니다. 

