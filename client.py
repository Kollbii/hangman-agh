#!/usr/bin/env python3

from hangman_problem import HangmanProblem
from hangman_state import HangmanState

import socket
from random import choice
from time import sleep
import os

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

HOST='0.0.0.0'
# HOST='136.243.156.120'
PORT=7777
# PORT=50804
AUTH=False
PICKED=False
ALPHABET=0

LOGIN='test01\n'
PASSW='qq\n'

s.connect((HOST,PORT))

def random_word():
    return choice(list(map(str, open('slowa.txt').read().split())))

def search_for_words(state):
    os.system("grep -E '^" + str(p.state.parse_to_grep()) + "' slowa.txt > guess.txt")
    
    lines = [line.strip() for line in open('guess.txt','r').readlines()]
    possible_words = [line for line in lines if len(line) == len(p.state.word)]
    print(state.parse_to_grep(), 'for current search: ',len(possible_words))
    
    return possible_words

while True:
    try:
        if not AUTH:
            s.send(LOGIN.encode())
            s.send(PASSW.encode())
            sleep(0.1)
            msg = s.recv(64).decode().replace('\n', '').replace('\r', '')
            if msg[0] == '+':
                print('Set AUTH=True', end='')
                AUTH=True
                if msg[1] == '1':
                    ALPHABET = 1
                    print(' ==> Picking alphabet no. 1\n')
                if msg[1] == '2':
                    ALPHABET = 2
                    print(' ==> Picking alphabet no. 2\n')

        s_messg=s.recv(64)
        if not s_messg:
            break
        parsed = s_messg.decode().replace('\n', '').replace('\r', '')
        print("S:",parsed)

        if parsed == '@':
            word = random_word() + '\n'
            print('Picking word:', word)
            s.send(word.encode())

        if parsed.isdecimal():
            p = HangmanProblem(HangmanState(parsed), ALPHABET)
            letters = p.actions(p.state)

            for i in range(10):
                letter = letters[i]
                possible_words = []

                if i > 3:
                    possible_words = search_for_words(p.state)

                if len(possible_words) < 9 and i > 3:
                    s.send(str("=\n" + possible_words[0] + "\n").encode())
                    print('Guessing:', possible_words[0], '| round:',i)
                    possible_words.remove(possible_words[0])

                    sleep(0.1)
                    guessed = list(map(lambda x: x.rstrip(), s.recv(64).decode().split('\n')))
                    print("S:",guessed)
                    
                    if guessed[0] == "=":
                        print(f'Guessed {possible_words[0]} in {i} rounds for {guessed[1]} points. Closing connection.')
                        s.close()
                        exit(0)

                    i += 1
                    if i >= 9:
                        print('Out of guesses')
                        s.close()
                        exit(0)
                
                if i == 9:
                    s.send(str("=\n" + possible_words[0] + "\n").encode())
                    print('Guessing:', possible_words[0], '| round:',i)

                    sleep(0.1)
                    guessed = list(map(lambda x: x.rstrip(), s.recv(64).decode().split('\n')))
                    print("S:",guessed)
                    
                    if guessed[0] == "=":
                        print(f'Guessed {possible_words[0]} in {i} rounds for {guessed[1]} points. Closing connection.')
                        s.close()
                        exit(0)
                    
                    print(f'Correct word was {guessed[1]}. Got toal of {guessed[2]} points')

                    print('Out of guesses')
                    s.close()
                    exit(0)

                s.send(str('+\n' + letter + '\n').encode())
                print('Guessing:', letter, '| round:',i)

                sleep(0.1)

                guessed = list(map(lambda x: x.rstrip(), s.recv(64).decode().split('\n')))
                print('S:', guessed)

                if guessed[0] == "=":
                    for gi in [inx for inx, c in enumerate(guessed[1]) if c == '1']:
                        p.state.guessed[gi] = letter

    except KeyboardInterrupt:
        s.close()
        exit(0)
    