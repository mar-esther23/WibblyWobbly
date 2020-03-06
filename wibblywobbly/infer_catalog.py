data = ['mice', 'CAT ', 'doggo', 'PERSON', 'guinea pig', 'pig', 'Gorilla', 'Chimpanzee', 
        'orangután', 'chinpanze', 'gorila', 'dogs', 'rats', 'mouse', 'kitty', 'Cat', 'macaco']
print(data)

def get_best_match_dictionary(data, thr_accept=80):
    dic = {}
    while len(data)>1:
        target = data.pop()
        value, score = process.extract(target,data)[0]
        if score>=thr_accept:
            data.remove(value)
            dic[target] = value
        print(target, value, score)
    return dic
    
get_best_match(data)