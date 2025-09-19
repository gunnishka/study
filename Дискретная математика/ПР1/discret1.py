import math
import string
from itertools import permutations

with open ('example.txt', 'r', encoding = 'utf-8') as file:
    text = file.read()
    print(f"1. {text}")
    text = text.lower()
    symbol_list=[' ']
    punctuation = string.punctuation
    for i in punctuation:
        symbol_list.append(i)
    newtext = ''
    for symbol in text:
        if symbol not in symbol_list:
            newtext += symbol
#исключение запретных символов

with open ('newtext.txt', 'w', encoding = 'utf-8') as output_file:
    output_file.write(newtext)

with open ('newtext.txt', 'r', encoding = 'utf-8') as input_file:
    text2=input_file.read()
    print(f"2. {text2}")
    counter1L = [text2.count(char) for char in set(text2)]
    amount1L = 0
    for i in counter1L:
        amount1L += i
    print("3. Однобуквенные")
    for i in range(len(set(text2))):
        print(f"{list(set(text2))[i]} : {counter1L[i]}")
#подсчет частоты однобуквенных

    combinations = [''.join(comb) for comb in permutations(set(text2), 2)]

    twoL = []*len(combinations)
    for k in range(len(combinations)):
        twoL.append(0)
        for i in range(len(text2)-1):
            if text2[i]+text2[i+1] == combinations[k]:
                twoL[k] += 1
    print("3. Двубуквенные")
    for i in range (len(combinations)):
        if (twoL[i] != 0):
            print(f"{combinations[i]} : {[twoL[i]]}")
#подсчет частоты двухбуквенных

    def entropy(frequency):
        total = sum(frequency)
        entropy = 0
        entropy = - sum(count/total * math.log2(count/total) for count in frequency if count > 0)
        return entropy
#функция подсчета энтропии

    single_entropy = entropy(counter1L)
    double_entropy = entropy(twoL)

    print(f"4. Однобуквенные: {single_entropy}, Двубуквенные: {double_entropy}")
    uniq_symbs_counter = len(set(text2))
    length = round(math.log2(uniq_symbs_counter))
    x=0
    for i in counter1L:
        p = i / amount1L
        if p>0:
            x -= p * math.log2(p)
    redundancy = (length - x) / length * 100

    print(f"5. Длина = {length}, Избыточность = {redundancy}")
#подсчет длины кода и избыточности

    num_of_todelete_symbols = round(uniq_symbs_counter * 0.2)

    def analyze_entropy_after_removal(text, chars_to_remove):
        modified_text = ''.join([char for char in text if char not in chars_to_remove])
        char_count = [modified_text.count(char) for char in set(modified_text)]
        return entropy(char_count), len(modified_text), len(set(modified_text))

    char_frequency = {}
    for char in text2:
        if char in char_frequency:
            char_frequency[char] += 1
        else:
            char_frequency[char] = 1

    sorted_by_frequency = sorted(char_frequency.items(), key=lambda x: x[1], reverse=True)
    frequent_chars = [char for char, freq in sorted_by_frequency[:num_of_todelete_symbols]]

    entropy_after_frequent_removal, new_length1, new_unique1 = analyze_entropy_after_removal(text2, frequent_chars)

    print(f"6. Исходная энтропия: {single_entropy:.4f}")
    print(f"Энтропия после удаления: {entropy_after_frequent_removal:.4f}")
    print(f"Изменение энтропии: {entropy_after_frequent_removal - single_entropy:+.4f}")

    sorted_by_rarity = sorted(char_frequency.items(), key=lambda x: x[1])
    rare_chars = [char for char, freq in sorted_by_rarity[:num_of_todelete_symbols]]

    entropy_after_rare_removal, new_length2, new_unique2 = analyze_entropy_after_removal(text2, rare_chars)

    print(f"7. Исходная энтропия: {single_entropy:.4f}")
    print(f"Энтропия после удаления: {entropy_after_rare_removal:.4f}")
    print(f"Изменение энтропии: {entropy_after_rare_removal - single_entropy:+.4f}")

