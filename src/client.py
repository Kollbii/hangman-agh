#!/usr/bin/env python3

from hangman_problem import HangmanProblem
from hangman_state import HangmanState

import socket
from time import sleep, time
from random import randint
from datetime import datetime
import os


global AUTH, CONN, HOST, PORT, ALPHABET, LOGIN, PASSW

# Local Jurcz
HOST='0.0.0.0'
PORT=7777

# Local Nędz
# HOST='0.0.0.0'
# PORT=65432

# Local Kono
# HOST='127.0.0.1'
# PORT=12345

# Dyrcz 
# HOST='136.243.156.120'
# PORT=50804

# Jurczyk
# HOST='209.182.238.21'
# PORT=4444

# Konopek
# HOST='136.243.156.120'
# PORT=12186

# Nędza
# HOST='136.243.156.120'
# PORT=50804

# Gjorgi :)
# HOST='31.172.70.25'
# PORT=130


AUTH=False
CONN=False
ALPHABET=0

LOGIN='test01\n'
PASSW='qq\n'

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

def current_time():
    now = datetime.now().timetuple()
    return str(f"[{now.tm_hour}:{now.tm_min}:{now.tm_sec}]")

def search_for_words(state):
    os.system("grep -E '^" + str(state.parse_to_grep()) + "' ../slowa.txt > guess.txt")
    
    possible_words = [line for line in [line.strip() for line in open('guess.txt','r').readlines()] if len(line) == len(state.word)]
    print(state.parse_to_grep(), 'for current search: ',len(possible_words))
    
    return possible_words

def guess_word():
    raise NotImplementedError

def guess_letter():
    raise NotImplementedError

def get_conn():
    global CONN
    if s.connect((HOST, PORT)):
        CONN = True
        return True
    return False

def close_write(start, end):
    global AUTH, CONN
    print(current_time(),f'Total game time: {end-start}\nClosing connection...')
    os.system("rm -f guess.txt")
    s.close()
    CONN = False
    AUTH = False
    # Change this sleep later in time...
    sleep(4)
    os.system("clear")


def auth():
    global ALPHABET, AUTH
    s.send(LOGIN.encode())
    s.send(PASSW.encode())
    
    sleep(0.1)
    msg = s.recv(64).decode().replace('\n', '').replace('\r', '').replace('\0', '')
    if msg[0] == '+':
        print(current_time(),'Set AUTH=True', end='')
        AUTH=True
        if msg[1] == '1':
            ALPHABET = 1
            print(' ==> Picking alphabet no. 1')
        if msg[1] == '2':
            ALPHABET = 2
            print(' ==> Picking alphabet no. 2')
        return True

    print(current_time(),'Authentication failure.')
    return False

def write_to_log(info):
    print(info)
    log_msg = f'[{current_time()}]'

while True:
    try:
        if not CONN:
            get_conn()           

        if not AUTH:
            auth()

        s_messg=s.recv(64)
        if not s_messg:
            break

        parsed = s_messg.decode().replace('\n', '').replace('\r', '').replace('\0', '')
        print(current_time(),"Server:",parsed)

        if parsed.isdecimal():
            start_time = time()
            p = HangmanProblem(HangmanState(parsed), ALPHABET)
            letters = p.actions()

            for i in range(10):
                letter = letters[i]
                possible_words = []

                if p.state.count_guess() > 1:
                    possible_words = search_for_words(p.state)

                if len(possible_words) > 0 and len(possible_words) < 10:
                    i += 1
                    s.send(str("=\n" + possible_words[0] + "\n").encode())
                    print(current_time(),f'[{i}] Guessing: {possible_words[0]}')
                    possible_words.remove(possible_words[0])

                    sleep(0.1)
                    guessed = list(map(lambda x: x.rstrip(), s.recv(64).decode().split('\n')))
                    print(current_time(),"Server:",guessed)
                    
                    if guessed[0] == "=":
                        print('Guessed!')
                        close_write(start_time, time())
                        break

                    if i >= 9:
                        print('Out of guesses')
                        close_write(start_time, time())
                        break
                
                if i == 9:
                    s.send(str("=\n" + possible_words[0] + "\n").encode())
                    print(current_time(),f'[{i}] Guessing: {possible_words[0]}')

                    sleep(0.1)
                    guessed = list(map(lambda x: x.rstrip(), s.recv(64).decode().split('\n')))
                    print(current_time(),f'Server: {guessed}')
                    
                    if guessed[0] == "=":
                        print('Guessed!')

                    print(current_time(),'Out of guesses')
                    close_write(start_time, time())
                    break
                    
                
                s.send(str('+\n' + letter + '\n').encode())
                print(current_time(),f'[{i}] Guessing: {letter}')

                sleep(0.1)

                guessed = list(map(lambda x: x.rstrip(), s.recv(64).decode().split('\n')))
                print(current_time(),'Server:', guessed)

                if guessed[0] == "=":
                    for gi in [inx for inx, c in enumerate(guessed[1]) if c == '1']:
                        p.state.guessed[gi] = letter

    except socket.error:
        CONN = False
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        while not CONN:
            try:
                s.connect((HOST, PORT))
                CONN = True
            except socket.error:
                sleep(2)

    except KeyboardInterrupt:
        s.close()
        exit(0)
    