#!/usr/bin/env python3

from hangman_problem import HangmanProblem
from hangman_state import HangmanState

from time import sleep, time, strftime
from os import system
import socket

global AUTH, CONN, HOST, PORT, ALPHABET, LOGIN, PASSW, GUESSED, SERVER

ALPHABET=0
AUTH=False
CONN=False

'''Represent current time'''
def current_time():
    return str(strftime('[%-d %b %X]'))

'''Response striped and splited response'''
def get_response():
    return list(map(lambda x: x.rstrip().replace('\x00',''), s.recv(64).decode().split('\n')))

'''Writing msg to log_[day]_[month].txt in `logs` dir'''
def write_to_log(info):
    log_msg = f'{current_time()} {info}'
    print(log_msg)
    system("echo '" + log_msg + "' >> ../logs/log_"+str(strftime('%-d_%b'))+".txt")

'''System grep call to patterns.txt file. '''
def search_for_words(problem):
    grepped = str(problem.state.parse_to_grep(problem.guessed_letters))
    try:
        system("grep -E '^" + grepped + "$' ./patterns.txt > guess.txt")
    except Exception:
        write_to_log('[ERROR] patterns.txt file not found.')

    problem.potential_words = [line for line in [line.strip() for line in open('guess.txt','r').readlines()]][::-1]
    problem.potential_words_length = len(problem.potential_words)
    write_to_log(f'{problem.state} for current search: {problem.potential_words_length}')

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
    write_to_log(f'Total game time: {end-start}')   # Optional. Will be deleted on ranked games
    write_to_log(f'Closing connection with server')
    system('rm -f guess.txt')
    system('rm -f patterns.txt')
    s.close()
    CONN = False
    AUTH = False
    sleep(0.2)

'''Authenticate and update global variables. Some servers have different type of parsing(?)'''
def auth():
    global ALPHABET, AUTH, SERVER
    if SERVER != 4:
        s.send(LOGIN.encode())
        s.send(PASSW.encode())
    else:
        s.send(f"{LOGIN}\n{PASSW}\n".encode())
    
    sleep(0.5)
    msg = s.recv(64).decode().replace('\n', '').replace('\r', '').replace('\0', '').replace('\x00','')
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

'''Temp func.'''
def write_to_benchmark(round, hint, plain, guessed, word="None"):
    if guessed:
        system("echo '" + f"{round},{hint},{plain},{guessed}" + "' >> ../utils/benchmark.txt")
    else:
        system("echo '" + f"{round},{hint},{word},{guessed}" + "' >> ../utils/benchmark.txt")

'''Handle given signs in response'''
def handle_response(response, **kwargs):
    start_time = kwargs['time']

    # START OPTIONAL
    plain_word = kwargs['plain']
    word = kwargs['word']
    round = kwargs['round']
    # END OPTIONAL

    if "=" in response:
        write_to_log('Guessed!')
        write_to_benchmark(round, plain_word, word, True) # Optional
        close_write(start_time, time())
        return True
    
    if "?" in response:
        write_to_log('Got ? closing connection.')
        write_to_benchmark(round, plain_word, word, False, response[1]) # Optional
        close_write(start_time, time())
        return True

    if "#" in response:
        write_to_log('Got ignored')
        return False

'''Main func to keep game running.'''
def game(word_numbers):
    start_time = time() # Probably should delete this. But it will stay for flex now.
    p = HangmanProblem(HangmanState(word_numbers), ALPHABET)
    p.words_initial()
    letters = p.get_letters_occurences_initial()
    print("Letter queue:", letters)

    i = 0
    while i < 10:
        print("Lenngth of potential words",len(p.potential_words))
        print("Guessed letters", p.guessed_letters)

        try:
            letter = letters.pop()
        except IndexError:
            break

        if i > 0:
            search_for_words(p)

        # DELETE THIS LATER
        if len(p.potential_words) < 10:
            print(' '.join(p.potential_words))

        if len(p.potential_words) > 0 and len(p.potential_words) < 4:
            for _ in range(10 - i):
                try:
                    word_to_guess = p.potential_words.pop()
                    guessed = guess_word(word_to_guess, i)
                except IndexError:
                    break

                if handle_response(guessed,time=start_time,plain=p.state.word_plain,word=word_to_guess,round=i+1):
                    break
                else:
                    i += 1
                    if i > 9:
                        write_to_log('Out of guesses')
                        close_write(start_time, time())
                        break
                    continue

        if i == 9:
            try:
                word_to_guess = p.potential_words.pop()
                guessed = guess_word(word_to_guess, i)
            except IndexError:
                break

            if handle_response(guessed,time=start_time,plain=p.state.word_plain,word=word_to_guess,round=i+1):
                write_to_log('Out of guesses')
                break

            break
    
        if i > 2: # i == 2 --> 4.72 / 98.48
            letters.pop()
            letter = letters.pop()
            guessed = guess_letter(letter, i)
        else:
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
        p.add_to_guessed(letter)
        
        letters = p.get_letters_occurences_initial()

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
if __name__ == "__main__":
    print(  '\033[96m:::    :::     :::     ::::    :::  ::::::::  :::    ::: \n'
            ':+:    :+:   :+: :+:   :+:+:   :+: :+:    :+: :+:    :+: \n'
            '+:+    +:+  +:+   +:+  :+:+:+  +:+ +:+        +:+    +:+ \n'
            '+#++:++#++ +#++:++#++: +#+ +:+ +#+ :#:        +#++:++#++ \n'
            '+#+    +#+ +#+     +#+ +#+  +#+#+# +#+   +#+# +#+    +#+ \n'
            '#+#    #+# #+#     #+# #+#   #+#+# #+#    #+# #+#    #+# \n'
            '###    ### ###     ### ###    ####  ########  ###    ### \n\033[00m')
    print(  '0 → Debugi\n'
            '1 → Dyrczu\n'
            '2 → Jurczy\n'
            '3 → Konope\n'
            '4 → Nędzaa\n'
            '5 → Gjorgi\n')
    SERVER=int(input('Pick Server:'))
    if SERVER == 0:
        # Local Debug
        HOST='0.0.0.0'
        PORT=7777
        LOGIN='test01\n'
        PASSW='qq\n'
    if SERVER == 1:
        # Dyrczu http://srv.lbk.ct8.pl/
        HOST='136.243.156.120'
        PORT=50804
        LOGIN='405865\n'
        PASSW='[REDACTED]\n'
    if SERVER == 2:
        # Jurczyk https://ranking.but-it-actually.work/
        HOST='209.182.238.21'
        PORT=4444
        LOGIN='405865\n'
        PASSW='[REDACTED]\n'
    if SERVER == 3:
        # Konopek http://balalaika.ct8.pl/
        HOST='136.243.156.120'
        PORT=12186
        LOGIN='405865\n'
        PASSW='[REDACTED]n'
    if SERVER == 4:
        # Nędza http://146.59.45.35
        HOST='146.59.45.35'
        PORT=65432
        LOGIN='405865'
        PASSW='[REDACTED]'
    if SERVER == 5:
        # Gjorgi http://31.172.70.25/
        HOST='31.172.70.25'
        PORT=130
        LOGIN='405865\n'
        PASSW='[REDACTED]\n'

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

            '''Hotfix for Pati server. Ignoring null msgs.'''
            while s_messg == b'\x00':
                s_messg=s.recv(64)

            parsed = s_messg.decode().replace('\n', '').replace('\r', '').replace('\0', '').replace('\x00', '')      
            write_to_log(f'Server: {parsed}')
        
            if parsed.isdecimal():
                game(parsed)
            
        except socket.error:
            #TODO: Make reconecting on socket error.
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
        