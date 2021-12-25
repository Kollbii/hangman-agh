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

    def actions(self):
        occurences = {
            1: self.state.word.count(1),
            2: self.state.word.count(2),
            3: self.state.word.count(3),
            4: self.state.word.count(4)
        }
        guesses = list()

        # Pick letter 'F'...
        for i in range(len(self.state.word)):
            if self.state.word[i] == '4':
                guesses.append(self.alphabet[4][0])
                self.alphabet[4].remove(self.alphabet[4][0])
                break

        # Random polish character
        # polish = ['ą','ś','ę','ż','ó','ń','ć','ź']
        # TODO: Picking of random polish character should depend on alphabets type.

        # for char in self.state.freq:
        #     if char in polish:
        #         if char == 'ł':
        #             guesses.append(char)
        #             self.alphabet[3].remove('ł')
        #             break
        #         else:
        #             if self.alphabet_type == 1:
        #                 guesses.append(char)
        #                 self.alphabet[1].remove(char)
        #             else:
        #                 guesses.append(char)
        #                 self.alphabet[2].remove(char)
        #             break

        # Add two potential guesses for last letter
        for i in range(2):
            try:
                guesses.append(self.alphabet[self.state.word[-1]][i])
                self.alphabet[self.state.word[-1]].remove(self.alphabet[self.state.word[-1]][i])
            except IndexError:
                continue

        # Add two pottential guesses for first letter
        for i in range(2):
            try:
                guesses.append(self.alphabet[self.state.word[0]][i])
                self.alphabet[self.state.word[0]].remove(self.alphabet[self.state.word[0]][i])
            except IndexError:
                continue

        # Fill guesses up to 10
        while len(guesses) < 10:
            for num in [3,1,2]:
                for _ in range(occurences[num]):
                    if len(guesses) >= 10:
                        break
                    try:
                        guesses.append(self.alphabet[num][0])
                        self.alphabet[num].remove(self.alphabet[num][0])
                    except IndexError:
                        guesses.append(self.alphabet[(num + 1) % 3 + 1][0])
                        self.alphabet[(num + 1) % 3 + 1].remove(self.alphabet[(num + 1) % 3 + 1][0])
        print('Letter queue', guesses)

        return guesses