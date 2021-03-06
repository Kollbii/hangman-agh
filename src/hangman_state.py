'''
HangmanState stores initial word from numbers and current state of guessed letters.
Its main purpouse is to keep track of guessed letters and making pattern for grep serach.

I was thinking about using frequency of letters in words of given length but could not come up with something nice. Relicts.
'''

class HangmanState(object):
    def __init__(self, word_to_guess: str):
        self.word_plain = word_to_guess.strip()
        self.word = [int(i) for i in word_to_guess]
        self.guessed = ['' for _ in range(len(word_to_guess))]
        self.count_guesses = 0
        if len(word_to_guess) == 5:# Words of length 5. Total count 28008
            self.freq = ['a', 'o', 'i', 'e', 'k', 'u', 'r', 'm', 'n', 's', 'l', 'y', 't', 'p', 'w', 'z', 'c', 'd', 'b', 'ą', 'ł', 'ę', 'g', 'j', 'ż', 'f', 'h', 'ó', 'ć', 'ś', 'ń', 'ź', 'x', 'v']
        if len(word_to_guess) == 6:# Words of length 6. Total count 63030
            self.freq = ['a', 'o', 'i', 'e', 'k', 'r', 'u', 'm', 'n', 's', 'y', 'z', 'w', 'l', 'c', 't', 'p', 'd', 'ł', 'b', 'j', 'ą', 'g', 'ę', 'ż', 'h', 'ó', 'f', 'ć', 'ś', 'ń', 'ź', 'x', 'v', 'q']
        if len(word_to_guess) == 7:# Words of length 7. Total count 124353
            self.freq = ['a', 'o', 'i', 'e', 'k', 'r', 'n', 'm', 'z', 'w', 'u', 'y', 's', 'c', 'l', 't', 'p', 'd', 'ł', 'j', 'b', 'ą', 'g', 'ę', 'h', 'ż', 'ó', 'f', 'ś', 'ć', 'ń', 'ź', 'x', 'v', 'q']
        if len(word_to_guess) == 8:# Words of length 8. Total count 205528
            self.freq = ['a', 'o', 'i', 'e', 'n', 'r', 'k', 'z', 'w', 'y', 'm', 'c', 's', 'u', 't', 'p', 'l', 'ł', 'd', 'j', 'b', 'ą', 'g', 'h', 'ę', 'ż', 'ó', 'ś', 'f', 'ń', 'ć', 'ź', 'x', 'v', 'q']
        if len(word_to_guess) == 9:# Words of length 9. Total count 295470
            self.freq = ['a', 'o', 'i', 'e', 'n', 'z', 'y', 'r', 'w', 'c', 'm', 'k', 's', 'u', 'p', 't', 'l', 'ł', 'd', 'j', 'b', 'ą', 'g', 'h', 'ż', 'ę', 'ś', 'ó', 'f', 'ń', 'ć', 'ź', 'x', 'v', 'q']
        if len(word_to_guess) == 10:# Words of length 10. Total count 373343
            self.freq = ['a', 'o', 'i', 'e', 'n', 'y', 'z', 'w', 'r', 'c', 'm', 'k', 's', 'p', 'u', 't', 'l', 'ł', 'd', 'j', 'b', 'ą', 'g', 'h', 'ś', 'ż', 'ę', 'f', 'ó', 'ń', 'ć', 'ź', 'x', 'v', 'q']
        if len(word_to_guess) == 11:# Words of length 11. Total count 423178
            self.freq = ['a', 'i', 'o', 'e', 'n', 'y', 'z', 'w', 'r', 'c', 'm', 's', 'k', 'p', 'u', 't', 'l', 'ł', 'd', 'j', 'b', 'g', 'ą', 'h', 'ś', 'ż', 'ę', 'f', 'ó', 'ń', 'ć', 'ź', 'v', 'x']
        if len(word_to_guess) == 12:# Words of length 12. Total count 435586
            self.freq = ['a', 'i', 'o', 'e', 'n', 'y', 'z', 'w', 'r', 'c', 'm', 's', 'k', 'p', 't', 'u', 'l', 'd', 'ł', 'j', 'b', 'g', 'ą', 'h', 'ś', 'ż', 'ę', 'f', 'ń', 'ó', 'ć', 'ź', 'v', 'x']
        if len(word_to_guess) == 13:# Words of length 13. Total count 415967
            self.freq = ['i', 'a', 'o', 'e', 'n', 'y', 'w', 'z', 'r', 'c', 'm', 's', 'p', 'k', 't', 'u', 'l', 'd', 'ł', 'j', 'b', 'g', 'ą', 'ś', 'h', 'ż', 'ę', 'f', 'ń', 'ó', 'ć', 'ź', 'v', 'x']
        if len(word_to_guess) == 14:# Words of length 14. Total count 372165
            self.freq = ['i', 'a', 'e', 'o', 'n', 'y', 'w', 'z', 'r', 'c', 'm', 's', 'p', 'k', 't', 'u', 'l', 'd', 'j', 'b', 'ł', 'g', 'ś', 'ą', 'h', 'ę', 'ż', 'f', 'ń', 'ó', 'ć', 'ź', 'v']
        if len(word_to_guess) == 15:# Words of length 15. Total count 308641
            self.freq = ['i', 'e', 'a', 'n', 'o', 'y', 'w', 'z', 'r', 'c', 'm', 's', 'p', 'k', 't', 'u', 'l', 'd', 'j', 'b', 'ł', 'ś', 'g', 'h', 'ą', 'ę', 'f', 'ż', 'ó', 'ń', 'ź', 'ć', 'v']

    '''
    Returns strings witch is passed to `grep` os call. 
    Ex. return `[^aiort][^aiort]a[^aiort][^aiort]i[^aiort]orta`.
    '''
    def parse_to_grep(self, excluded_letters):
        excluded = list()
        for key in excluded_letters:
            for char in excluded_letters[key]:
                excluded.append(char)

        grepped = ''
        for letter in self.guessed:
            if letter == '':
                # Add blank space
                grepped += ''.join('[^')
                # Add every letter with should not be in this position
                grepped += ''.join(''.join(excluded)+']')
            else:
                grepped += ''.join(letter)
        print(grepped)
        return grepped

    '''
    Used only to validate if ANY letter was guessed. If so - make os.grep call with pattern.
    '''
    def count_guess(self):
        for g in self.guessed:
            if g != '':
                self.count_guesses += 1
        return self.count_guesses

    def __str__(self):
        return ''.join(char if char != '' else '.' for char in self.guessed)
