import pandas as pd
import os
import numpy as np
import sys

DATA_PATH = "data/tech_docs.csv"

def load_data(file_path): 
  print("="*11,"기능 1","="*11)
  if os.path.exists(file_path):
    df = pd.read_csv(file_path, encoding="utf-8-sig")
    print(f"데이터 로드 완료: {df.shape[0]}행 × {df.shape[1]}열")
  else:
    print("파일이 없습니다. 프로그램을 즉시 종료합니다.")
    sys.exit()
  print("="*30)
  return df

def explore_structure(df): 
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

def show_category_distribution(df):
  print("="*11,"기능 3","="*11)
  print("카테고리 문서 수와 비율")
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

def check_missing(df):
  print("="*11,"기능 4","="*11) 
  df=pd.read_csv(DATA_PATH)
  clean_cols = []
  for column in df.columns:
    count = df[column].isnull().sum()
    if count == 0 :  
      clean_cols.append(column)
    else:
      rate = df[column].isnull().sum() / len(df)*100
      if rate < 5:
        print(f"{column} : 결측지 심각도 기준 낮음")
      elif  rate <20:
        print(f"{column} : 결측치 심각도 기준 주의")
      else:
        print(f"{column} : 결측치 심각도 기준 높음")
  print("결측치 없는 컬럼:", ", ".join(clean_cols))

def numpy_doc_stats(df):  
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
    df = load_data(DATA_PATH) 
    explore_structure(df) 
    show_category_distribution(df)
    check_missing(df)
    numpy_doc_stats(df)

if __name__ == "__main__":
    main()