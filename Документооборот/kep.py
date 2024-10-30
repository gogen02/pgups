import hashlib
import sys
from Crypto.Util import number


def sha256_hash(data):
    sha256 = hashlib.sha256()
    sha256.update(data.encode('utf-8'))
    hash_result = sha256.hexdigest()
    return hash_result


# Рассчитывает НОД
def gcd(a, b):
    while b:
        a, b = b, a%b
    return a


# Метод extended_euclidean() реализует расширенный алгоритм Евклида (алгоритм для нахождения НОД двух целых чисел)
# Используется в методе calculate_secret_exponent()
def extended_euclidean(value, other):
    a0 = value
    a1 = other
    if a0 == 0 or a1 == 0:
        return None
    x0 = 1
    x1 = 0
    y0 = 0
    y1 = 1

    while a1 != 0:
        q = a0 // a1
        (a0, a1) = (a1, a0 - a1 * q)
        (x0, x1) = (x1, x0 - x1 * q)
        (y0, y1) = (y1, y0 - y1 * q)
    out = []
    out.append(a0)
    out.append(x0)
    out.append(y0)
    return out


# Метод calculate_secret_exponent() возвращает число, обратное value по модулю other
def calculate_secret_exponent(value, other):
    dxy = extended_euclidean(value, other)
    if dxy[0] == 1:
        if dxy[1] > 0:
            return dxy[1]
        return other - abs(dxy[1])
    return None


# Метод rsa_cipher_info() выполняет возведение числа в степень other по модулю modulo
def rsa_cipher(value, other, modulo):
    return pow(value, other, modulo)


class CreateRSASign:

    def __init__(self):
        self.p = number.getPrime(1024) # Генерация простого числа длиной 1024 бит
        self.q = number.getPrime(1024)
        self.n = self.p * self.q # Вычислениие модуля
        self.phi = (self.p - 1) * (self.q - 1) # Функция Эйлера
        self.public = CreateRSASign.create_public_key(self.phi) # Генерация публичного ключа
        self.private = calculate_secret_exponent(self.public, self.phi)

    def create_public_key(phi):
        key = number.getPrime(1024)
        while (key >= phi) or (gcd(phi, key) != 1): # Если ключ больше функции Эйлера
                                                                    # или числа не взаимно простые,
                                                                    # то нужно сгенерировать другой ключ
            key = number.getPrime(1024)
        return key

signs = [CreateRSASign() for i in range(3)]

document = 'Съешь ещё этих мягких французских булок'
msg_hash = sha256_hash(document) # Хэш документа, это значение будет подписано

signature1 = rsa_cipher(int(msg_hash, 16), signs[0].private, signs[0].n) # Подпись первого участника
signature2 = rsa_cipher(signature1, signs[1].private, signs[1].n) # Подпись второго участника
signature3 = rsa_cipher(signature2, signs[2].private, signs[2].n) # Подпись третьего участника

print(f"Публичный ключ 1:\n", signs[0].public)
print(f"Публичный ключ 2:\n", signs[1].public)
print(f"Публичный ключ 3:\n", signs[2].public)


# Проверка, что подпись действительна:
# RSA-преобразование в обратную сторону
s1 = rsa_cipher(signature3, signs[2].public, signs[2].n)
s2 = rsa_cipher(s1, signs[1].public, signs[1].n)
h1 = rsa_cipher(s2, signs[0].public, signs[0].n) # Здесь должен получится изначальный хэш

print("\nДокумент:", document)
print('Коллективная ЭП:\n', signature3)
print(f'Хэш начальный (полученный закрытыми ключами): {int(msg_hash, 16)}')
print(f'Хэш полученный (расшифрованный открытыми ключами): {h1}')
if h1 == int(msg_hash,16):
    print(f'Подпись действительна!')
else:
    print(f'Подпись недействительна!')

