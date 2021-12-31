#!/usr/bin/env python3

from hangman_problem import HangmanProblem
from hangman_state import HangmanState

from time import sleep, time, strftime
from os import system
import socket

global AUTH, CONN, HOST, PORT, ALPHABET, LOGIN, PASSW, GUESSED, SERVER

SERVER = 0
AUTH=False
CONN=False
ALPHABET=0

#TODO: Fix this later
if SERVER == 0:
    # Local Jurcz
    HOST='0.0.0.0'
    PORT=7777
    LOGIN='test01\n'
    PASSW='qq\n'
if SERVER == 1:
    # Dyrczu
    HOST='136.243.156.120'
    PORT=50804
    LOGIN='test01\n'
    PASSW='qq\n'
if SERVER == 2:
    # Jurczyk
    HOST='209.182.238.21'
    PORT=4444
    LOGIN='405865\n'
    PASSW='I9$*z(D7BqU0Hvqd\n'
if SERVER == 3:
    # Konopek
    HOST='136.243.156.120'
    PORT=12186
    LOGIN='8\n'
    PASSW='8\n'
if SERVER == 4:
    # Nędza
    HOST='146.59.45.35'
    PORT=65432
    LOGIN='p8\n'
    PASSW='p\n'
if SERVER == 5:
    # Gjorgi :)
    HOST='31.172.70.25'
    PORT=130
    LOGIN='405865\n'
    PASSW='insert\n'


'''Represent current time'''
def current_time():
    return str(strftime('[%-d %b %X]'))

'''Response striped and splited response'''
def get_response():
    return list(map(lambda x: x.rstrip(), s.recv(64).decode().split('\n')))

'''Writing msg to log_[day]_[month].txt in `logs` dir'''
def write_to_log(info):
    #TODO: Make log file for each day/couple of hours or even sessions of games.
    log_msg = f'{current_time()} {info}'
    print(log_msg)
    system("echo '" + log_msg + "' >> ../logs/log_"+str(strftime('%-d_%b'))+".txt")

'''System grep call to patterns.txt file. '''
def search_for_words(problem):
    try:
        system("grep -E '^" + str(problem.state.parse_to_grep()) + "' ./patterns.txt > guess.txt")
    except Exception:
        write_to_log('[ERROR] patterns.txt file not found.')

    problem.potential_words = [line for line in [line.strip() for line in open('guess.txt','r').readlines()]]
    write_to_log(f'{problem.state.parse_to_grep()} for current search: {len(problem.potential_words)}')


'''Guess word, write info to log and receive information from server. Sleep() function is optional but works better on some servers...'''
def guess_word(possible_word, round):
    s.send(str("=\n" + str(possible_word) + "\n").encode())
    write_to_log(f'[{round}] Guessing: {possible_word}')

    sleep(0.05)
    guessed = get_response()
    write_to_log(f'Server: {guessed}')
    return guessed

'''Guess letter, write info to log and receive information from server. Sleep() function is optional but works better on some servers...'''
def guess_letter(possible_letter, round):
    s.send(str('+\n' + str(possible_letter) + '\n').encode())
    write_to_log(f'[{round}] Guessing: {possible_letter}')

    sleep(0.05)
    guessed = get_response()
    write_to_log(f'Server: {guessed}')
    return guessed

'''Connect and update global variables'''
def get_conn():
    global CONN
    if s.connect((HOST, PORT)):
        CONN = True
        return True
    return False

'''Close connection and update global variables. Remove files like `guess.txt` and `patterns.txt` from curent dir.'''
def close_write(start, end):
    global AUTH, CONN
    write_to_log(f'Total game time: {end-start}')
    write_to_log(f'Closing connection with server')
    system('rm -f guess.txt')
    system('rm -f patterns.txt')
    s.close()
    CONN = False
    AUTH = False
    sleep(2)

'''Authenticate and update global variables. Some servers have different type of parsing(?)'''
def auth():
    global ALPHABET, AUTH, SERVER
    if SERVER != 4:
        s.send(LOGIN.encode())
        s.send(PASSW.encode())
    else:
        s.send(f"{LOGIN}\n{PASSW}\n".encode())
    
    sleep(0.1)
    msg = s.recv(64).decode().replace('\n', '').replace('\r', '').replace('\0', '')
    if msg[0] == '+':
        AUTH=True
        if msg[1] == '1':
            ALPHABET = 1
            write_to_log('Set AUTH=True ==> Picking alphabet no. 1')
        if msg[1] == '2':
            ALPHABET = 2
            write_to_log('Set AUTH=True ==> Picking alphabet no. 2')

        return True

    write_to_log('Authentication failure')

    return False

'''Main func to keep game running.'''
def game(word_numbers):
    start_time = time() # Probably should delete this. But it will stay for flex now.
    p = HangmanProblem(HangmanState(word_numbers), ALPHABET)
    p.words_initial()
    letters = p.get_letter()
    i = 0
    while i < 10:
        print("Lenngth of potential words",len(p.potential_words))

        #TODO: Look at this. Sometimes error occures. Potential problem is in hangman_problem.py
        try:
            letter = letters.pop()
        except IndexError:
            break

        if p.state.count_guess() > 1:
            search_for_words(p)
        
        if len(p.potential_words) > 0 and len(p.potential_words) < 7:
            for _ in range(10 - i):
                guessed = guess_word(p.potential_words.pop(), i)

                #TODO: those 3 if's can be in one func. Same under
                if "=" in guessed:
                    write_to_log('Guessed!')
                    close_write(start_time, time())
                    break
                
                if "?" in guessed:
                    write_to_log('Got ? closing connection.')
                    close_write(start_time, time())
                    break

                if "#" in guessed:
                    write_to_log('Got ignored')
                    continue

                i += 1
                if i > 9:
                    write_to_log('Out of guesses')
                    close_write(start_time, time())
                    break

        if i == 9:
            guessed = guess_word(p.potential_words.pop(), i)
            
            if "=" in guessed:
                write_to_log('Guessed!')

            if "?" in guessed:
                    write_to_log('Got ? closing connection.')
                    close_write(start_time, time())
                    break
            
            if "#" in guessed:
                    write_to_log('Got ignored')
                    continue

            write_to_log('Out of guesses')
            close_write(start_time, time())
            break

        guessed = guess_letter(letter, i)

        if "=" in guessed:
            '''Hotfix for Zuza server'''
            if guessed[1] == '':
                guessed[1] = get_response()[0]

            times_guessed = 0
            for gi in [inx for inx, c in enumerate(guessed[1]) if c == '1']:
                p.state.guessed[gi] = letter
                times_guessed += 1

            p.update_occurences(letter, times_guessed)

        letters = p.get_letter()

        if "?" in guessed:
            write_to_log('Got ? closing connection.')
            close_write(start_time, time())
            break

        if "#" in guessed:
            write_to_log('Got ignored')
            continue

        i+=1

'''
Main body to keep connection alive. Auto reconecting after closing connection.
If socket error occurs function will probably do nothing and everything will break.
#TODO
'''
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
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
        write_to_log(f'Server: {parsed}')
        
        if parsed.isdecimal():
            game(parsed)
        
    except socket.error:
        #TODO: Make reconecting on error.
        CONN = False
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        while not CONN:
            try:
                s.connect((HOST, PORT))
                CONN = True
            except socket.error:
                sleep(2)

    except KeyboardInterrupt:
        write_to_log('Closing connection by KeyboardInterrupt')
        s.close()
        exit(0)
    