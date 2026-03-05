import argparse
import json
import random
import time


class Question:
    def __init__(self, text, answers, correct_answer):
        self.text = text
        self.answers = answers
        self.correct_answer = correct_answer


class TriviaGame:
    def __init__(self, questions, num_of_players):
        self.questions = questions
        self.num_of_players = num_of_players
        self.scores = [0] * num_of_players
        self.player_index = 0
        self.current_question = None

    def next_player(self):
        self.player_index = (self.player_index + 1) % self.num_of_players

    def get_new_question(self):
        if not self.questions:
            return None
        return self.questions.pop()

    def play(self):
        random.shuffle(self.questions)
        self.current_question = self.get_new_question()

        if self.current_question is None:
            print("No questions available.")
            return

        while self.current_question is not None:
            q = self.current_question
            print(q.text)
            for i, ans in enumerate(q.answers, start=1):
                print(f"{i}. {ans}")

            start = time.time()
            choice = input(
                f"Player {self.player_index + 1}, choose your answer number (you have 10 sec to answer): "
            ).strip()
            elapsed = time.time() - start

            if elapsed > 10:
                print("times up!")
                self.next_player()
                continue

            if not choice.isdigit():
                print("Invalid input, please enter a number.")
                continue

            idx = int(choice) - 1
            if idx < 0 or idx >= len(q.answers):
                print("Invalid choice.")
                continue

            chosen_answer = q.answers[idx]
            if chosen_answer == q.correct_answer:
                print("Correct!")
                self.scores[self.player_index] += 1
                self.next_player()
                self.current_question = self.get_new_question()
            else:
                print("Wrong!")
                self.next_player()
                self.current_question = self.get_new_question()
                
        print("\nGame over!")
        for i, score in enumerate(self.scores, start=1):
            print(f"Player {i}: {score}")

        max_score = max(self.scores)
        winners = [i + 1 for i, s in enumerate(self.scores) if s == max_score]
        if len(winners) == 1:
            print(f"The winner is Player {winners[0]}.")
        else:
            joined = ", ".join(str(w) for w in winners)
            print(f"There is a tie between players: {joined}.")


def load_questions(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    questions = []
    for item in data:
        questions.append(
            Question(
                text=item["text"],
                answers=item["answers"],
                correct_answer=item["correct_answer"],
            )
        )
    return questions


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Trivia Game")
    parser.add_argument("file", help="Path to questions JSON file")
    parser.add_argument("players", type=int, help="Number of players (>= 2)")
    args = parser.parse_args()

    if args.players < 2:
        print("Number of players must be at least 2.")
        raise SystemExit(1)

    questions = load_questions(args.file)
    game = TriviaGame(questions, args.players)
    game.play()
