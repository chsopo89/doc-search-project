# doc-search-project
마일스톤으로 이번 KANT 시작 전 4주 프로젝트로 
week1 주차부터 4주차까지 쌓이는 프로젝트입니다. 이때 어찌 시험을 잘 봤는지 모르겠지만 프로젝트에 배정이 되어 하게 되었습니다 ㅠㅠ  
천천히 주마다 피드백 받는 내용을 1주바다 다시 수정하여 슬랙 DM으로 보내드리겠습니다. 날카로운 첨삭 부탁드립니다 ^^
(우선 피드백 받은 내용으로 수정을 하지면 튜터님 입장에서 이부분을 더 수정을을 하면 더 깔끔한 코드일거 같다 이런식으로 해주시면 너무 감사 할 거 같습니다 ㅠㅠ 개발에 초짜인 새싹이 뿌리가 깊에 박힐 수 있게 도와 주세요 ㅎㅎㅎ 강한 피드백도 OK 입니다. 뭐 장미칼과 같은 날카로운 피드백 또한 정말 언제드지 OK 입니다 ^^;; 뭐 30분 맨탈 나가면 되죠 뭐 ㅎㅎㅎㅎㅎㅎㅎㅎㅎ^^;;;;)

==================================================================================================================================================

1주차에 받은 피드백 내용입니다. 
🎯 보완이 필요한 영역

함수 이름을 요구사항 명세(load_data, explore_structure 등)에 맞추는 습관
함수 반환값 명세 준수 (show_category_distribution, check_missing의 dict 반환)
파일 경로 하드코딩 대신 상대 경로 + DATA_PATH 상수 활용
결측치 출력 형식 — 결측치 수·비율과 심각도를 함께 표시하고, 결측치 없는 컬럼 목록 별도 출력
50단어 미만 문서의 실제 내용(제목 등) 출력 및 pandas describe() 비교 출력 명시
📝 기능별 피드백

부분충족
load_data (function1)
✅ os.path.exists()로 파일 존재 여부를 확인하고, 없을 때 안내 메시지 출력 후 sys.exit()로 종료하는 흐름을 정확히 구현하셨습니다. '데이터 로드 완료: 60행 × 5열' 형태의 출력도 잘 맞췄어요.

⚠️ 두 가지를 보완하면 더 좋습니다. 첫째, 함수 이름이 function1인데 요구사항은 load_data()를 명시하고 있어요. 함수명을 명세에 맞추면 가독성과 협업 측면에서 훨씬 유리합니다. 둘째, DATA_PATH가 절대 경로(C:/Users/chsop/...)로 하드코딩되어 있어서 다른 컴퓨터에서는 실행이 안 됩니다. 상대 경로를 사용하면 어떤 환경에서도 동작합니다.

DATA_PATH = "C:/Users/chsop/doc-search-project/data/tech_docs.csv"
💡 DATA_PATH = "data/tech_docs.csv" 로 변경하고, python을 프로젝트 루트(doc-search-project/)에서 실행하면 해결됩니다. 함수 이름도 def load_data(file_path): 형태로 바꿔보세요.

충족
explore_structure (function2)
✅ shape, columns, dtypes, head(5), info()를 모두 출력하고 각 블록마다 구분선(=====)을 붙여 가독성을 잘 챙기셨습니다. 요구사항의 모든 출력 항목을 충족합니다.

⚠️ 함수 이름을 explore_structure(df)로 맞춰주시면 명세와 완전히 일치합니다. 기능 자체는 잘 동작합니다.

💡 def explore_structure(df): 로 이름만 변경해 주세요.

부분충족
show_category_distribution (function3)
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

부분충족
check_missing (function4)
✅ 컬럼별로 isnull().sum()을 확인하고 비율에 따라 낮음/주의/높음 심각도를 분기하는 핵심 로직을 잘 구현하셨습니다. 결측치가 없는 컬럼에 안내 메시지를 출력하는 점도 좋아요.

⚠️ 세 가지를 보완하면 더 좋습니다. 첫째, 함수가 df를 인자로 받지 않고 내부에서 pd.read_csv()를 다시 호출하고 있어요. 이미 불러온 df를 재활용하면 불필요한 파일 읽기를 줄일 수 있습니다. 둘째, 요구사항은 '결측치가 1개 이상인 컬럼만 출력'하고 '결측치 없는 컬럼 목록을 별도로 출력'하도록 명시하는데, 현재는 결측치 없는 컬럼도 개별 출력됩니다. 셋째, 결측치가 있는 컬럼의 경우 결측치 수와 비율(%)도 함께 출력하면 명세를 완전히 충족합니다. 마지막으로 함수가 dict를 반환해야 합니다.

def function4():
  df=pd.read_csv(DATA_PATH)  # 인자 없이 파일을 다시 읽음
💡 def check_missing(df): 로 인자를 받도록 변경하고, missing_cols와 clean_cols 리스트를 분리해서 결측치 있는 컬럼만 상세 출력한 뒤 결측치 없는 컬럼 목록을 한 번에 출력하는 구조로 바꿔보세요. 결과는 딕셔너리로 반환하는 것도 잊지 마세요.

부분충족
numpy_doc_stats (function5)
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

부분충족
main()
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

💪 최종 마무리

전체 기능 흐름을 스스로 완성하셨다는 것 자체가 정말 의미 있는 출발입니다. 오늘 발견한 성장 포인트들(함수 이름, 반환값, 상대 경로)은 한 번만 익히면 이후 2~4주차에서 자연스럽게 체화되는 것들이니 너무 부담 갖지 마세요!

===============================================================================================================================================

