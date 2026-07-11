import pandas as pd
import os
import numpy as np

DATA_PATH = "C:/Users/chsop/doc-search-project/data/tech_docs.csv"

def function1():
  print("="*11,"기능 1","="*11)
  if os.path.exists(DATA_PATH):
    df = pd.read_csv(DATA_PATH, encoding="utf-8-sig")
    print(f"데이터 로드 완료: {df.shape[0]}행 × {df.shape[1]}열")
  else:
    print("파일이 없습니다. 프로그램을 즉시 종료합니다.")
    sys.exit()
  print("="*30)
  return df

def function2(df):
  print("="*11,"기능 2","="*11)
  print(f"데이터의 크기 : 행 : {df.shape[0]} 열: {df.shape[1]}")
  print("="*30)
  print(f"컬럼명 목록  \n{df.columns} ")
  print("="*30)
  print(f"컬럼별 자료형  \n{df.dtypes}")
  print("="*30)
  print(f"상위 5행  \n{df.head(5)}")
  print("="*30)
  print("데이터 요약 정보  ") 
  df.info()

def function3(df):
  print("="*11,"기능 3","="*11)
  cat = df["category"].value_counts()
  print("카테고리 문서 수와 비율")
  for cat, count in df["category"].value_counts().items():
    print(f"{cat}: {count} 건 {round(count/(len(df))*100,2)} %")
  print("카테고리별 평균단어 수")
  cat_uni = df["category"].unique()
  for cat in cat_uni:
    texts = df[df["category"] == cat]["content"]
    counts = [len(text.split()) for text in texts]
    avg = sum(counts) / len(counts)
    print(f"{cat} : {round(avg,2)} 단어")

def function4():
  print("="*11,"기능 4","="*11) 
  df=pd.read_csv(DATA_PATH)
  for column in df.columns:
    count = df[column].isnull().sum()
    if count == 0 :
      print(f"{column} : 결측치가 없습니다.")
    else:
      rate = df[column].isnull().sum() / len(df)*100
      if rate < 5:
        print(f"{column} : 결측지 심각도 기준 낮음")
      elif  rate <20:
        print(f"{column} : 결측치 심각도 기준 주의")
      else:
        print(f"{column} : 결측치 심각도 기준 높음")

def function5(df):  
  print("="*11,"기능 5","="*11) 
  content = df["content"].dropna()
  words = [] 
  for text in content: 
      words.append(len(text.split()))
  word_arr = np.array(words)
  words_ave = np.mean(word_arr)
  words_SD = np.std(word_arr, ddof=1)
  words_mid = np.median(word_arr)
  words_min = np.min(word_arr)
  words_max = np.max(word_arr)
  print(f"평균 : {round(words_ave,2)}")
  print(f"표본표준편차 : {round(words_SD,2)}")
  print(f"중앙값 : {words_mid}")
  print(f"최솟값 : {words_min}")
  print(f"최댓값 : {words_max}")
  words_length = word_arr[word_arr < 50]
  if len(words_length) == 0:
    print("50단어 미만의 문서 : 없음.")
  else:
    print(words_length)
  print(round(pd.Series(words).describe(),2))

def main():
    df = function1()
    function2(df)
    function3(df)
    function4()
    function5(df)

if __name__ == "__main__":
    main()