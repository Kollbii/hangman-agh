a1 ={   'a': 1,'ą': 1,'b': 3,'c': 1,'ć': 1,'d': 3,'e': 1,'ę': 1,'f': 4,
        'g': 2,'h': 3,'i': 1,'j': 2,'k': 3,'l': 3,'ł': 3,'m': 1,'n': 1,
        'ń': 1,'o': 1,'ó': 1,'p': 2,'q': 2,'r': 1,'s': 1,'ś': 1,'t': 3,
        'u': 1,'v': 1,'w': 1,'x': 1,'y': 2,'z': 1,'ź': 1,'ż': 1}

a2 ={   'a': 1,'ą': 2,'b': 3,'c': 1,'ć': 3,'d': 3,'e': 1,'ę': 2,'f': 4,
        'g': 2,'h': 3,'i': 3,'j': 2,'k': 3,'l': 3,'ł': 3,'m': 1,'n': 1,
        'ń': 3,'o': 1,'ó': 3,'p': 2,'q': 2,'r': 1,'s': 1,'ś': 3,'t': 3,
        'u': 1,'v': 1,'w': 1,'x': 1,'y': 2,'z': 1,'ź': 3,'ż': 3}

a1_out = []
a2_out = []

with open('../slowa.txt','r') as f:
    save_a1 = open('a1.txt','w')
    save_a2 = open('a2.txt','w')
    for line in [line.strip() for line in f.readlines()]:
        if len(line) > 4:
            tmp_a1 = ''
            tmp_a2 = ''
            for char in line:
                tmp_a1 += str(a1[char])
                tmp_a2 += str(a2[char])
            save_a1.write(f'{tmp_a1},{line}\n')
            save_a2.write(f'{tmp_a2},{line}\n')
            
            