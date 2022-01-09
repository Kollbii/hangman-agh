'''
HangmanProblem stores initial state of given word.
Goal state is not included. You have to guess...
'''

class HangmanProblem(object):
    def __init__(self, initial, alph):
        self.state = initial
        self.alphabet_type = alph
        self.potential_words = list()
        self.potential_words_length = 0
        self.letter_queue = list()
        self.guessed_letters = {1:[],
                                2:[],
                                3:[],
                                4:[]}

        self.occurences = dict()
        for i in list(set(self.state.word)):
            self.occurences[i] = self.state.word.count(i)

        if alph == 1:
            self.alphabet = {
                            1: ['a','i','o','z','e','c','n','w','r','m','s','u','ą','ś','ę','x','v','ż','ó','ń','ć','ź'],
                            2: ['y','p','j','g','q'],
                            3: ['k','t','l','d','ł','b','h'],
                            4: ['f']
                            }
        if alph == 2:
            self.alphabet = {
                            1: ['a','o','e','n','z','w','r','c','m','s','u','x','v'],
                            2: ['y','p','j','g','ą','ę','q'],
                            3: ['i','k','t','l','d','ł','b','h','ś','ż','ó','ń','ć','ź'],
                            4: ['f']
                            }

    '''Find all possible words with given pattern from server'''
    def words_initial(self):
        from os import system
        try:
            system("grep -E '^" + str(self.state.word_plain) + ",' " + str(f'../utils/a{self.alphabet_type}.txt') + " | awk -F, '{print $2}' > patterns.txt")
        except Exception:
            raise NameError(f'Could not find ../utils/a{self.alphabet_type}.txt file')

        self.potential_words = [line for line in [line.strip().split(',')[0] for line in open('patterns.txt', 'r').readlines()] if len(line) == len(self.state.word_plain)]
        self.potential_words_length= len(self.potential_words)

    '''Insert description here later'''
    def get_letters_occurences_initial(self):
        from collections import Counter
        from operator import itemgetter

        total = dict(sorted(dict(Counter(''.join(word for word in self.potential_words))).items(), key=itemgetter(1), reverse=True))
        
        for new_char in reversed(total):
            if new_char not in self.guessed_letters[1] and new_char not in self.guessed_letters[2] and new_char not in self.guessed_letters[3] and new_char not in self.guessed_letters[4]:            
                self.letter_queue.append(new_char)
        
        return self.letter_queue

    def get_letters_occurences(self):
        from collections import Counter
        from operator import itemgetter

        total = dict(sorted(dict(Counter(''.join(word for word in self.potential_words))).items(), key=itemgetter(1), reverse=True))
        letters = list()

        try:
            pass
        except Exception:
            pass

        for key in self.guessed_letters:
            for char_guess in reversed(total):
                if char_guess not in self.guessed_letters[key]:
                    letters.append(char_guess)
        return letters

    '''Update dictionary with guessed letters'''
    def add_to_guessed(self, letter):
        for key in self.alphabet:
            for char in self.alphabet[key]:
                if char == letter:
                    self.guessed_letters[key].append(char)
                    break

    '''If letter is guessed, substract counter from current count'''
    def update_occurences(self, letter, times):
        for key in self.guessed_letters:
            for char in self.guessed_letters[key]:
                if char == letter:
                    self.occurences[key] -= times
                    return

    '''
    Return one letter from least occured letter number.
    To work properly after each guess dictionaries must be updated via `update_occurenxes()` func.
    '''
    def get_letter(self):
        letters = list()
        strategic_letter = min(zip(self.occurences.values(), self.occurences.keys()))
        try:
            if self.occurences[1] >= 8:
                strategic_letter = max(zip(self.occurences.values(), self.occurences.keys()))
        except KeyError:
            strategic_letter = max(zip(self.occurences.values(), self.occurences.keys()))

        #TODO: Problem with short words len < 8. Make prio 2->1->3
        if self.occurences[strategic_letter[1]] <= 0:
            del self.occurences[strategic_letter[1]]
            strategic_letter = min(zip(self.occurences.values(), self.occurences.keys()))

        for i in range(strategic_letter[0]):
            try:
                if self.alphabet[strategic_letter[1]][i] not in self.guessed_letters[strategic_letter[1]]:
                    letters.append(self.alphabet[strategic_letter[1]][i])
                    self.guessed_letters[strategic_letter[1]].append(self.alphabet[strategic_letter[1]][i])
                    self.alphabet[strategic_letter[1]].remove(self.alphabet[strategic_letter[1]][i])
                    return letters
            except IndexError:
                continue

    '''Old version of generating letter queue. Kept as backup.'''
    def actions(self):
        guesses = list()

        '''Pick letter F'''
        if 4 in self.state.word:
            guesses.append(self.alphabet[4][0])
            self.alphabet[4].remove(self.alphabet[4][0])
        del self.occurences[4]

        '''Add pottential guess for last letter'''
        for i in range(1):
            try:
                guesses.append(self.alphabet[self.state.word[-1]][i])
                self.alphabet[self.state.word[-1]].remove(self.alphabet[self.state.word[-1]][i])
            except IndexError:
                continue

        '''Add pottential guess for first letter'''
        for i in range(1):
            try:
                guesses.append(self.alphabet[self.state.word[0]][i])
                self.alphabet[self.state.word[0]].remove(self.alphabet[self.state.word[0]][i])
            except IndexError:
                continue

        '''Fill guesses up to 10'''
        while len(guesses) < 10:
            for num in [3,1,2]:
                for _ in range(self.occurences[num]):
                    if len(guesses) >= 10:
                        break
                    try:
                        guesses.append(self.alphabet[num][0])
                        self.alphabet[num].remove(self.alphabet[num][0])
                    except IndexError:
                        guesses.append(self.alphabet[(num + 1) % 3 + 1][0])
                        self.alphabet[(num + 1) % 3 + 1].remove(self.alphabet[(num + 1) % 3 + 1][0])

        return guesses