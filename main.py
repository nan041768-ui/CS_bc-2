import json
import os
import random

# --------------------기본 뼈대 & Quiz Class--------------------------
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

#------------------(QuizGame 클래스 및 메뉴)--------------------
class QuizGame:
   def __init__(self):
      self.quizzes = []
      self.best_score = 0
      self.filename = "state.json"
      self.load_data() # 시작할 때 파일 불러오기

   def load_data(self):
      try:
         if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as f:
               data = json.load(f)
               self.best_score = data.get("best_score", 0)
               for q_data in data.get("quizzes", []):
                  quiz = Quiz(q_data["question"], q_data["choices"], q_data["answer"])
                  self.quizzes.append(quiz)
            print(f"📂 저장된 데이터를 불러왔습니다. (퀴즈 {len(self.quizzes)}개, 최고점수 {self.best_score}점)")
         else:
            self.set_default_quizzes()
      except Exception as e:
         print("⚠️ 데이터 파일을 읽는 중 오류가 발생했습니다. 기본 데이터로 시작합니다.")
         self.set_default_quizzes()

   def save_data(self):
      try:
         data = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score
         }
         with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
      except Exception as e:
         print(f"⚠️ 데이터 저장 중 오류 발생: {e}")

   def set_default_quizzes(self):
      # 기본 퀴즈 5개 설정 (원하는 주제로 수정하세요)
      self.quizzes = [
         Quiz("파이썬의 창시자는?", ["Guido", "Linus", "Bjarne", "James"], 1),
         Quiz("1 + 1 은?", ["1", "2", "3", "4"], 2),
         Quiz("대한민국의 수도는?", ["부산", "서울", "인천", "제주"], 2),
         Quiz("애플의 창립자는?", ["일론 머스크", "마크 주커버그", "스티브 잡스", "빌 게이츠"], 3),
         Quiz("물이 끓는 온도는(섭씨)?", ["50도", "90도", "100도", "120도"], 3)
      ]

   def add_quiz(self):
      print("\n📌 새로운 퀴즈를 추가합니다.")
      question = input("문제를 입력하세요: ").strip()
      choices = []
      for i in range(1, 5):
         choice = input(f"선택지 {i}: ").strip()
         choices.append(choice)

      while True:
         try:
            answer = input("정답 번호 (1-4): ").strip()
            answer = int(answer)
            if 1 <= answer <= 4:
               break
            print("⚠️ 1-4 사이의 숫자를 입력하세요.")
         except ValueError:
            print("⚠️ 잘못된 입력입니다. 숫자를 입력하세요.")


      new_quiz = Quiz(question, choices, answer)
      self.quizzes.append(new_quiz)
      self.save_data()
      print("✅ 퀴즈가 추가되었습니다!")

   def show_list(self):
      print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
      print("-" * 40)
      for i, quiz in enumerate(self.quizzes):
            print(f"[{i+1}] {quiz.question}")
      print("-" * 40)

   def show_score(self):
      print(f"\n🏆 최고 점수: {self.best_score}점")

   def run(self):
      while True:
         print("\n" + "="*40)
         print("        🎯 나만의 퀴즈 게임 🎯")
         print("="*40)
         print("1. 퀴즈 풀기\n2. 퀴즈 추가\n3. 퀴즈 목록\n4. 점수 확인\n5. 종료")
         print("="*40)

         try:
            choice = input("선택: ").strip()
            if not choice:
               print("⚠️ 빈 입력입니다. 다시 입력해주세요.")
               continue

            choice = int(choice)
            if choice < 1 or choice > 5:
               print("⚠️ 허용 범위 밖입니다. 1-5 사이 숫자를 입력하세요.")
               continue

            if choice == 1:
               print("퀴즈 풀기 기능은 곧 추가됩니다.")
            elif choice == self.add_quiz():
               print("퀴즈 추가 기능은 곧 추가됩니다.")
            elif choice == self.show_list():
               print("퀴즈 목록 기능은 곧 추가됩니다.")
            elif choice == self.show_score():
               print("점수 확인 기능은 곧 추가됩니다.")
            elif choice == 5:
               print("게임을 종료합니다.")
               self.save_data()
               break

         except ValueError:
            print("!! 잘못된 입력입니다. 숫자를 입력하세요.")

# Ctrl+C 종료 시에도 안전하게 저장되도록 예외 처리
if __name__ == "__main__":
   game = QuizGame()
   try:
         game.run()
   except (KeyboardInterrupt, EOFError):
         print("\n!! 비정상 종료를 감지했습니다. 데이터를 안전하게 저장하고 종료합니다.")
         game.save_data()