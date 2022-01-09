for i in range(9):
    with open(f'benchmark{i}.txt') as f:
        lines = [line.strip().split(',') for line in f.readlines()]
        sum_guesses = 0
        guess_ratio = 0
        for line in lines:
            sum_guesses += int(line[0])
            if line[3] == 'True': 
                guess_ratio += 1

        print('Average guesses: ', round(sum_guesses/len(lines), 2), sum_guesses,"/",len(lines))
        print('Ratio of guessed words: ', round(guess_ratio/len(lines)*100, 2), guess_ratio,"/",len(lines))