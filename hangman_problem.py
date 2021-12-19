class HangmanProblem(object):
    def __init__(self, initial, alph):
        self.state = initial
        self.alphabet_type = alph
        if alph == 1:
            self.alphabet = {
                            1: ['a','i','o','e','n','z','w','r','c','m','s','u','ą','ś','ę','x','v','ż','ó','ń','ć','ź'],
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

    def actions(self, state):
        occurences = {
            1: state.word.count(1),
            2: state.word.count(2),
            3: state.word.count(3),
            4: state.word.count(4)
        }
        guesses = list()

        #TODO Think about it more...
        for i in range(len(self.state.word)):
            if self.state.word[i] == '4':
                guesses.append(self.alphabet[4][0])
                self.alphabet[4].remove(self.alphabet[4][0])

        # Random polish character.
        polish = ['ą','ś','ę','ż','ó','ń','ć','ź']
        for char in self.state.freq:
            if char in polish:
                if char == 'ł':
                    guesses.append(char)
                    self.alphabet[3].remove('ł')
                    break
                else:
                    if self.alphabet_type == 1:
                        guesses.append(char)
                        self.alphabet[1].remove(char)
                    else:
                        guesses.append(char)
                        self.alphabet[2].remove(char)
                    break

        # Fill guesses up to 10 and higher.
        while len(guesses) < 10:
            for num in [1,3,2]:
                for _ in range(occurences[num]):
                    try:
                        guesses.append(self.alphabet[num][0])
                        self.alphabet[num].remove(self.alphabet[num][0])
                    except IndexError:
                        guesses.append(self.alphabet[(num + 1) % 3 + 1][0])
                        self.alphabet[(num + 1) % 3 + 1].remove(self.alphabet[(num + 1) % 3 + 1][0])
        print('Letter queue', guesses)

        return guesses