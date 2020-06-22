from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer

chatbot = ChatBot("Ron Obvious")
conversation = [
    "Hello",
    "Hi there!",
    "How are you doing?",
    "I'm doing great.",
    "That is good to hear",
    "Thank you.",
    "You're welcome.",
    "I am neither male not female",
    "What is going on?",
    "Yes",
    "No"
]

trainer = ListTrainer(chatbot)

trainer.train(conversation)


trainer = ChatterBotCorpusTrainer(chatbot)

trainer.train(
    "chatterbot.corpus.english"
)

"""
while True:
    i = input()
    if i == 'exit' : break
    print(chatbot.get_response(i))
"""


def answer(msg:str):
    return chatbot.get_response(msg)
