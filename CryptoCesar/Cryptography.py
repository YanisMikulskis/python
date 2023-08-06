#Шифр Цезаря. Каждый буква в сообзении двигается влево или в право на определнное количество символов

letters = 'АБВГДЕЁЖЗИКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'

mess = 'привет, world!'.upper()
mess2 = 'привет, world!'.upper()

def encrypt(message, k):
    new_mess = ''
    for word in message:
        if word in letters:
            if k > 0:
                if k > len(letters[letters.index(word):]):
                    new_k = k - len(letters[letters.index(word):])
                    new_mess += letters[new_k]
                else:
                    new_mess += letters[letters.index(word) + k]
            else:
                if abs(k) > len(letters[:letters.index(word)]):
                    new_k = abs(k) - len(letters[:letters.index(word)])
                    new_mess += letters[-new_k]
                else:
                    new_mess += letters[letters.index(word) + k]
        else:
            new_mess += word
    return new_mess

print(encrypt(mess, 5))
print(encrypt(mess2, -5))