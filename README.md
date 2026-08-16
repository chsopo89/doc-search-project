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
 DATA_PATH = "data/tech_docs.csv" 로 변경하고, python을 프로젝트 루트(doc-search-project/)에서 실행하면 해결됩니다. 함수 이름도 def load_data(file_path): 형태로 바꿔보세요. 
 => 수정내용 
- 이름: function1 → load_data
- DATA_PATH 절대경로 → 상대경로 data/tech_docs.csv
- 함수 안에서 DATA_PATH 대신 인자 file_path 사용
- main()에서 df = load_data(...) 로 반환값 받기




## 기능 2 — explore_structure
✅ shape, columns, dtypes, head(5), info()를 모두 출력하고 각 블록마다 구분선(=====)을 붙여 가독성을 잘 챙기셨습니다. 요구사항의 모든 출력 항목을 충족합니다.

⚠️ 함수 이름을 explore_structure(df)로 맞춰주시면 명세와 완전히 일치합니다. 기능 자체는 잘 동작합니다.

💡 def explore_structure(df): 로 이름만 변경해 주세요.

## 기능 3 — show_category_distribution
✅ value_counts()로 카테고리별 문서 수와 비율(%)을 출력하고, unique()로 고유 카테고리를 추출한 뒤 반복문과 딕셔너리 없이 리스트 컴프리헨션으로 평균 단어 수를 계산하는 구조가 잘 짜여 있어요. 비율 계산 로직도 정확합니다.

⚠️ 두 가지 성장 포인트가 있어요. 첫째, 요구사항에서 '반복문과 딕셔너리를 사용해 카테고리별 평균 단어 수를 계산'하도록 명시하고 있는데, 딕셔너리에 결과를 저장하는 부분이 빠져 있습니다. 둘째, 함수가 dict를 반환해야 하는데 현재는 반환값이 없습니다. 또한 변수명 cat을 value_counts()용과 반복문용으로 동시에 사용해 첫 번째 cat이 덮어씌워지는 버그가 있어요.

cat = df["category"].value_counts()
for cat, count in df["category"].value_counts().items():  # 위의 cat이 덮어씌워짐
    ...
💡 아래처럼 딕셔너리를 활용하고 반환값을 추가해 보세요:

def show_category_distribution(df):
    result = {}
    for cat in df['category'].unique():
        texts = df[df['category'] == cat]['content']
        avg = sum(len(t.split()) for t in texts) / len(texts)
        count = len(texts)
        result[cat] = {'count': count, 'avg_words': round(avg, 2)}
    for cat, info in result.items():
        ratio = round(info['count'] / len(df) * 100, 2)
        print(f"{cat}: {info['count']}건 {ratio}% | 평균단어수: {info['avg_words']}")
    return result

## 기능 4 — check_missing
✅ 컬럼별로 isnull().sum()을 확인하고 비율에 따라 낮음/주의/높음 심각도를 분기하는 핵심 로직을 잘 구현하셨습니다. 결측치가 없는 컬럼에 안내 메시지를 출력하는 점도 좋아요.

⚠️ 세 가지를 보완하면 더 좋습니다. 첫째, 함수가 df를 인자로 받지 않고 내부에서 pd.read_csv()를 다시 호출하고 있어요. 이미 불러온 df를 재활용하면 불필요한 파일 읽기를 줄일 수 있습니다. 둘째, 요구사항은 '결측치가 1개 이상인 컬럼만 출력'하고 '결측치 없는 컬럼 목록을 별도로 출력'하도록 명시하는데, 현재는 결측치 없는 컬럼도 개별 출력됩니다. 셋째, 결측치가 있는 컬럼의 경우 결측치 수와 비율(%)도 함께 출력하면 명세를 완전히 충족합니다. 마지막으로 함수가 dict를 반환해야 합니다.

def function4():
  df=pd.read_csv(DATA_PATH)  # 인자 없이 파일을 다시 읽음
💡 def check_missing(df): 로 인자를 받도록 변경하고, missing_cols와 clean_cols 리스트를 분리해서 결측치 있는 컬럼만 상세 출력한 뒤 결측치 없는 컬럼 목록을 한 번에 출력하는 구조로 바꿔보세요. 결과는 딕셔너리로 반환하는 것도 잊지 마세요.

## 기능 5 — numpy_doc_stats
✅ dropna()로 결측치를 제거한 뒤 반복문으로 단어 수 배열을 만들고, ddof=1을 지정해 pandas와 동일한 표본표준편차를 계산한 점이 훌륭합니다. 조건 필터링(word_arr < 50)도 NumPy 방식으로 정확히 구현하셨어요. pd.Series(words).describe()로 비교 출력을 포함한 것도 좋습니다.

⚠️ 두 가지를 보완하면 더 좋습니다. 첫째, 50단어 미만 문서가 있을 때 단어 수 배열(words_length)만 출력하고 있는데, 요구사항은 해당 문서를 '찾아서 출력'하도록 하므로 doc_id나 title 같은 문서 식별 정보를 함께 보여주면 더 완성도 있습니다. 둘째, describe() 비교 출력에서 pandas와 NumPy 수치가 '일치한다/다르다'는 명시적인 비교 메시지가 있으면 요구사항을 완전히 충족합니다.

words_length = word_arr[word_arr < 50]
if len(words_length) == 0:
    print("50단어 미만의 문서 : 없음.")
else:
    print(words_length)  # 단어 수만 출력, 문서 정보 없음
💡 아래처럼 df를 활용해 문서 정보를 함께 출력하고 비교 메시지를 추가해 보세요:

short_doc_mask = word_arr < 50
short_docs = df.dropna(subset=['content']).reset_index(drop=True)[short_doc_mask]
print(short_docs[['doc_id','title']])

pandas_std = pd.Series(words).std()
print(f'pandas std: {round(pandas_std,2)}, NumPy std(ddof=1): {round(words_SD,2)}')
print('일치' if round(pandas_std,2)==round(words_SD,2) else '불일치 — ddof 확인 필요')

## main()
✅ DATA_PATH 상수를 파일 상단에 선언하고, if __name__ == '__main__': 블록으로 진입점을 명확히 한 점이 좋습니다. 함수 호출 순서도 요구사항 흐름과 일치합니다.

⚠️ function4()가 df 인자 없이 호출되고 있어서 내부에서 파일을 다시 읽는 구조가 됩니다. check_missing(df)로 인자를 전달하도록 수정하면 전체 흐름이 깔끔해집니다. 또한 함수 이름들이 요구사항 명세(load_data, explore_structure 등)와 달라서, 이름을 맞춰주면 main() 코드가 문서 역할도 겸할 수 있습니다.

def main():
    df = function1()
    function2(df)
    function3(df)
    function4()   # df를 받지 않아 내부에서 파일 재로드
    function5(df)
💡 함수 이름을 명세에 맞게 변경한 뒤 main()을 아래처럼 정리해 보세요:

def main():
    df = load_data(DATA_PATH)
    explore_structure(df)
    show_category_distribution(df)
    check_missing(df)
    numpy_doc_stats(df)
    
============================================================================================


