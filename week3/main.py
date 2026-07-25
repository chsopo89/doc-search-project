import pandas as pd
import os
import numpy as np
import sys
import re
from sklearn.feature_extraction.text import TfidfVectorizer

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

def preprocess(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return (text)
def function6(df):
  print("="*11,"기능 1","="*11)
  df.dropna(subset=["content"], inplace=True)
  df["content_clean"] = df["content"].apply(preprocess)
  print(df[["content", "content_clean"]].head(3))

def cosine_similarity_numpy (a, b):
  dot_product = np.dot(a, b)
  norm_a = np.linalg.norm(a)
  norm_b = np.linalg.norm(b)
  if norm_a == 0 or norm_b == 0:
    return 0.0
  else:
    return dot_product/(norm_a * norm_b) 
def function7(df):
  print("="*11,"기능 2","="*11)
  a = np.array([1,2,3])
  b = np.array([1,2,3])
  print(cosine_similarity_numpy(a,b))

def keyword_search(query, df, top_k=5):
    query = preprocess(query)
    query_words = set(query.split())
    df["score"] = df["content_clean"].apply(lambda x : len(query_words & set(x.split())))
    score_descending = df.sort_values("score", ascending=False)
    score_descending = score_descending[["doc_id", "title", "category", "score"]].head(top_k)
    return(score_descending) 
def function8(df):
  print("="*11,"기능 3","="*11)  
  print(keyword_search("gradient descent", df))

def function9(df):
  print("="*11,"기능 4","="*11)
  vector = TfidfVectorizer(max_features=5000, min_df=2, stop_words="english")
  matrix = vector.fit_transform(df["content_clean"])
  print(f"문서 수: {matrix.shape[0]}, 사용 단어 수: {matrix.shape[1]}")
  return matrix, vector

def tfidf_search(df, query, vector, matrix, k):
  clean_query = preprocess(query)
  vector_query = vector.transform([clean_query]).toarray()
  similarity = []
  for doc in matrix.toarray():
    similarity.append(cosine_similarity_numpy(vector_query[0], doc))
  similarity = np.array(similarity)
  top_K = similarity.argsort()[::-1][:k]
  df["similarity"] =  similarity
  return df.iloc[top_K][["doc_id", "title", "category", "similarity"]]

def main():
    df = function1()
    function2(df)
    function3(df)
    function4()
    function5(df)
    function6(df)
    function7(df)
    print(df.columns)
    function8(df)
    matrix, vector = function9(df)
    query = "python list comprehension"
    k = 3 
    print("="*11,"기능 5","="*11)
    print(tfidf_search(df, query, vector, matrix, k))
    print("="*11,"기능 6","="*11)
    print(keyword_search(query, df, k))  #Baseline 경우 단어 매칭 갯수로만 검색을 하기에 D059가 1위를 함               
    print(tfidf_search(df, query, vector, matrix, k))  #TF-IDF는 단어의 중요도를 반영을 하여 더 관련있는 문서를 검색하기에 D001 이 1위를 함
    function11(df) 
    search_results = tfidf_search(df, query, vector, matrix, k)
    relevant_docs = ["D001", "D059"] 
    precision_at_k(search_results, relevant_docs, k)
    print("="*11,"기능 2","="*11)
    print(round(precision_at_k(["D001","D012","D059"], ["D001","D059"], k=3),4))
    print("="*11,"기능 3","="*11)
    print(reciprocal_rank(search_results["doc_id"].tolist(), relevant_docs))
    run_eva (df, vector, matrix, k)
    print
    analyze_fail(df, vector, matrix, k)


def function11(df):
  print("="*11,"기능 1","="*11)
  print(df[["doc_id", "title"]])
  eval_set = [
    {"query": "list comprehension in python", "relevant_doc_ids": ["D001"]},
    {"query": "python decorator usage", "relevant_doc_ids": ["D010"]},
    {"query": "how to branch in git", "relevant_doc_ids": ["D013"]},
    {"query": "git tag release version", "relevant_doc_ids": ["D022"]},
    {"query": "machine learning loss function", "relevant_doc_ids": ["D024"]},
    {"query": "neural network introduction", "relevant_doc_ids": ["D031"]},
    {"query": "numpy array index", "relevant_doc_ids": ["D033"]},
    {"query": "numpy stack split array", "relevant_doc_ids": ["D041"]},
    {"query": "pandas loc iloc indexing", "relevant_doc_ids": ["D046"]},
    {"query": "pandas read write csv file", "relevant_doc_ids": ["D050"]},
  ]
  print(f"평가셋 크기: {len(eval_set)}개 질문")

def precision_at_k(search_results, relevant_docs, k):
  search_results[:k]
  return len(set(search_results[:k]) & set (relevant_docs))/k
  print(precision_at_k(search_results, relevant_docs, k))

def reciprocal_rank(search_results, relevant_docs): 
  for rank, document in enumerate(search_results, start=1):
    if document in relevant_docs:
     return 1/rank
  return 0.0  

def run_eva(df, vector, matrix, k):
  run_evaluation = [
  ("Python List Comprehension", ["D001", "D059"]),
  ("Git Branching Basics", ["D013","D059"]),
  ("Loss Functions in Machine Learning",["D024", "D059"]),
  ("Introduction to Neural Networks",["D031", "D059"]),
  ("NumPy Random Number Generation",["D038", "D059"]),
  ("pandas Reading and Writing Files",["D050", "D059"])
  ]
  precision_scores = []
  mrr_scores = []
  base_precision_scores = []
  base_mrr_scores = []
  base_results = []
  for query, relevant_docs in run_evaluation:
    search_results = tfidf_search(df, query, vector, matrix, k)
    base_results = keyword_search(query, df, k)
    precision_scores.append(precision_at_k(search_results["doc_id"].tolist(), relevant_docs, k))
    mrr_scores.append(reciprocal_rank(search_results["doc_id"].tolist(), relevant_docs))
    base_precision_scores.append(precision_at_k(base_results["doc_id"].tolist(), relevant_docs, k))
    base_mrr_scores.append(reciprocal_rank(base_results["doc_id"].tolist(), relevant_docs))
  print("="*11,"기능 4","="*11)
  print(round(np.mean(precision_scores),4))
  print(round(np.mean(mrr_scores),4))
  print(round(np.mean(base_precision_scores),4))
  print(round(np.mean(base_mrr_scores),4))
  print(pd.DataFrame({"Precision@k": [np.mean(base_precision_scores), np.mean(precision_scores)], "MRR": [np.mean(base_mrr_scores), np.mean(mrr_scores)]}, index=["Baseline", "TF-IDF"]))
  return()

def analyze_fail(df, vector, matrix, k):
  print("="*11,"기능 5","="*11)
  analyze_failures = [
  ("pandas Reading and Writing Files",["D001", "D059"]),
  ("NumPy Random Number Generation",["D013", "D059"]),
  ("Introduction to Neural Networks",["D024", "D059"]),
  ("Loss Functions in Machine Learning",["D031", "D059"]),
  ("Git Branching Basics", ["D038","D059"]),
  ("Python List Comprehension", ["D050", "D059"])
  ]
  for query, relevant_docs in analyze_failures:
    search_results = tfidf_search(df, query, vector, matrix, k)
    if reciprocal_rank(search_results["doc_id"].tolist(), relevant_docs) == 0.0:
      print(f"실패한 질문 : {query}")
      print(f"정답 : {relevant_docs}")
      print(f"검색 결과 : {search_results}")
  return()

if __name__ == "__main__":
    main()