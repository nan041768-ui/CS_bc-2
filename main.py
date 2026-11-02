import json
import os
import random

class Quiz:
   # 클래스 생성될 때 문제, 선택지, 정답을 초기화
   def __init__(self, question, choices, answer):
         self.question = question
         self.choices = choices
         self.answer = answer

   # 파일 저장을 위해 딕셔너리 형태로 변환하는 method
   def to_dict(self):
         return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer
         }