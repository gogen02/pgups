#from datablocks import Datablock
import hashlib
# import os
# import Crypto
from Crypto.Util import number


def sha256_hash(data):
    sha256 = hashlib.sha256()
    sha256.update(data.encode('utf-8'))
    hash_result = sha256.hexdigest()
    return hash_result


# Метод gcd() возвращает наибольший общий делитель value и other
def gcd(value, other):
    slf = value
    oth = other

    # if slf == oth:
    #     return self.clone()

    if slf > oth:
        a, b = slf, oth
    else:
        a, b = oth, slf

    while True:
        r = a % b
        q = a // b

        if r == 0:
            break

        a = b
        b = r

    return b


# Метод extEuc реализует расширенный алгоритм Евклида
# Используется в методе modInverse()
def extEuc(value, other):
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


# Метод modInverse() возвращает число , обратное value по модулю other
def modInverse(value, other):
    dxy = extEuc(value, other)
    if dxy[0] == 1:
        if dxy[1] > 0:
            return dxy[1]
        return other - abs(dxy[1])
    return None


# Метод modPow() выполняет возведение числа в степень other по модулю modulo
def modPow(value, other, modulo):
    return pow(value, other, modulo)


class User:
    def __init__(self):
        self.p = number.getPrime(1024) # генерация простого числа длиной 512 бит
        self.q = number.getPrime(1024)
        self.n = self.p * self.q # вычислениие модуля
        self.phi = (self.p - 1) * (self.q - 1) # функция Эйлера
        self.public = User.createPublicKey(self.phi) # генерация публичного ключа
        self.private = modInverse(self.public, self.phi)

    def createPublicKey(phi):
        key = number.getPrime(512)
        while (key >= phi) or (gcd(phi, key) != 1): # проверяем, чтобы число было больше phi и проверка на наибольший общий делитель
            key = number.getPrime(512)
        return key

users = [User() for i in range(3)]

document = 'Gelasimov Груздев Gelasimov Gelasimov Gelasimov бебра Gelasimov Gelasimov Gelasimov'
msg_hash = sha256_hash(document) # Хэш документа

signature1 = modPow(int(msg_hash, 16), users[0].private, users[0].n) # подпись первого участника
signature2 = modPow(signature1, users[1].private, users[1].n) # подпись второго участника
signature3 = modPow(signature2, users[2].private, users[2].n) # подпись третьего участника

print(f"Public key 1:", users[0].public)
print(f"Public key 2:", users[1].public)
print(f"Public key 3:", users[2].public)

# Check signature

s1 = modPow(signature3, users[2].public, users[2].n)
s2 = modPow(s1, users[1].public, users[1].n)
h1 = modPow(s2, users[0].public, users[0].n) # финальный хэш

print('\nКоллективная ЭП:')
print(f'Хэш начальный: {int(msg_hash, 16)}')
print(f'Хэш полученный: {h1}')
if h1 == int(msg_hash,16):
    print(f'Подпись действительна!')
else:
    print(f'Подпись недействительна!')


# Композиционная ЭП RSA

# msg_hash1 = Datablock().fromInt(int(sha256_hash('Gruzdev'), 16))
# msg_hash2 = Datablock().fromInt(int(sha256_hash('Gelasimov'), 16))
# msg_hash3 = Datablock().fromInt(int(sha256_hash('Dukhovich'), 16))
#
# s1 = msg_hash1.modPow(users[0].private, users[0].n)
# s2 = (s1 * msg_hash2).modPow(users[1].private, users[1].n)
# s3 = (s2 * msg_hash3).modPow(users[2].private, users[2].n)
#
# # Check
#
# s1check = (s3.modPow(users[2].public, users[2].n) * msg_hash3.modInverse(users[2].n)) % users[2].n
# s2check = (s1check.modPow(users[1].public, users[1].n) * (msg_hash2.modInverse(users[1].n))) % users[1].n
# hcheck = s2check.modPow(users[0].public, users[0].n)
#
# print('\nКомпозиционная ЭП:')
# print(f'Хэш проверки: {hcheck.asInt(16)}')
# print(f'Хэш начальный: {msg_hash1.asInt(16)}')
# print(f'Подпись действительна!')
#
# # Коллективная ЭП в конечном поле
#
# class Abonent2:
#     def __init__(self, **kwargs):
#         choice = len(kwargs)
#
#         if choice == 1:
#             G = kwargs['G']
#             self.k = Datablock().generatePrime(10)
#             self.x = Datablock().generatePrime(10)
#             self.P = elips_mulscal(G, self.x)
#             self.R = elips_mulscal(G, self.k)
#
#         elif choice == 3:
#             p = kwargs['p']
#             q = kwargs['q']
#             a = kwargs['a']
#             self.k = Datablock().generatePrime(10)
#             self.x = Datablock().generatePrime(10)
#             self.y = Datablock().fromInt(a).modPow(self.x, p)
#             self.r = Datablock().fromInt(a).modPow(self.k, p)
#
#         elif choice == 4:
#             p = kwargs['p']
#             q = kwargs['q']
#             a = kwargs['a']
#             h = kwargs['h']
#             self.k = Datablock().generatePrime(10)
#             self.x = Datablock().generatePrime(10)
#             self.y = Datablock().fromInt(a).modPow(self.x, p)
#             self.r = Datablock().fromInt(a).modPow(self.k, p)
#             self.s = (self.k - self.x * h.asInt()) % q
#
#         else:
#             p = kwargs['p']
#             q = kwargs['q']
#             a = kwargs['a']
#             h = kwargs['h']
#             G = kwargs['G']
#             self.k = Datablock().generatePrime(10)
#             self.x = Datablock().generatePrime(10)
#             self.s = (self.k - self.x * h.asInt()) % q
#             self.P = elips_mulscal(G, self.x)
#             self.R = elips_mulscal(G, self.k)
#
#
# p = int("375ce26d", 16)
# q = int("53db", 16)
# a = int("32b83445", 16)
#
# text = 'Testing'
#
# # Коллективная ЭП на основе вычислений в конечном поле
#
# hsh = Datablock().fromText(sha256_hash(text))
# abonents = [Abonent2(p=p, q=q, a=a, h=hsh) for i in range(3)]
#
# # Генерация коллективной ЭП на основе вычислений в конечном поле
# s = (abonents[0].s + abonents[1].s + abonents[2].s) % q
# y = (abonents[0].y * abonents[1].y * abonents[2].y) % p
# res = (abonents[0].r * abonents[1].r * abonents[2].r) % p
# print('\nКоллективная ЭП на основе вычислений в конечном поле:')
# print(f'Хэш начальный: {res.asInt(16)}')
# res2 = ((y.modPow(hsh, p) * Datablock().fromInt(a).modPow(s, p)) % p)
# print(f'Хэш проверки: {res2.asInt(16)}')
#
# # Проверка коллективной ЭП на основе вычислений в конечном поле
# if res == res2:
#     print('Подпись действительна!')
# else:
#     print('Подпись не действительна!')
#
#
#
# # Композиционная ЭП на основе вычислений в конечном поле
#
# p = int("375ce26d", 16)
# q = int("53db", 16)
# a = int("32b83445", 16)
#
# datas = ['Gelasimov',
#          'Gruzdev',
#          'Dukhovich']
# hashs = [Datablock().fromText(sha256_hash(datas[i])) for i in range(3)]
# abonents = [Abonent2(p=p, q=q, a=a) for i in range(3)]
# print('\nКомпозиционная ЭП на основе вычислений в конечном поле:')
# # Генерация композиционной ЭП на основе вычислений в конечном поле
# y = (abonents[0].y.modPow(hashs[0], p) * abonents[1].y.modPow(hashs[1], p) * abonents[2].y.modPow(hashs[2], p)) % p
# r = (abonents[0].r * abonents[1].r * abonents[2].r) % p
# e = r.asInt() % q
# print(f'Хэш начальный: {e}')
# s = [(abonents[i].k - abonents[i].x * hashs[i].asInt() * e) % q for i in range(3)]
# S = (s[0] + s[1] + s[2]) % q
#
# # Проверка композиционной ЭП на основе вычислений в конечном поле
# r2 = (y.modPow(e, p) * Datablock().fromInt(a).modPow(S, p)) % p
# e2 = r2.asInt() % q
# print(f'Хэш проверки: {e2}')
# if e == e2:
#     print('Подпись действительна!')
# else:
#     print('Подпись не действительна!')
#
#
#
#
# def elips_sum(P, Q):
#     res = []
#     p = int("8000000000000000000000000000000000000000000000000000000000000431", 16)
#     a = int("7", 16)
#
#     if P != Q:
#         alfa = (Q[1] - P[1]) * ((Datablock().fromInt((Q[0] - P[0]) % p)).modInverse(p)).asInt()
#     else:
#         alfa = (3 * P[0] ** 2 + a) * ((Datablock().fromInt(P[1] * 2)).modInverse(p)).asInt()
#
#     res.append((alfa ** 2 - P[0] - Q[0]) % p)
#     res.append((alfa * (P[0] - res[0]) - P[1]) % p)
#     return res
#
#
# def elips_double(P):
#     res = []
#     p = int("8000000000000000000000000000000000000000000000000000000000000431", 16)
#     a = int("7", 16)
#
#     alfa = (3 * P[0] ** 2 + a) * ((Datablock().fromInt(P[1] * 2)).modInverse(p)).asInt()
#
#     res.append((alfa ** 2 - 2 * P[0]) % p)
#     res.append((alfa * (P[0] - res[0]) - P[1]) % p)
#
#     return res
#
# def elips_mulscal(G, n):
#     P = [0, 0]
#     P[0] = G[0]
#     P[1] = G[1]
#     if n == 1:
#         return P
#     elif n % 2 == 1:
#         return elips_sum(P, elips_mulscal(P, n - 1))
#     else:
#         return elips_mulscal(elips_double(P), n // 2)
#
# # Заданные значение
# p = int("8000000000000000000000000000000000000000000000000000000000000431", 16)
# q = int("8000000000000000000000000000000150fe8a1892976154c59cfc193accf5b3", 16)
# a = int("7", 16)
# G = []
# G.append(int("2", 16))
# G.append(int("8e2a8a0e65147d4bd6316030e16d19c85c97f0a9ca267122b96abbcea7e8fc8", 16))
#
#
# # Коллективная ЭП на основе вычислений в группе точек эллиптической кривой
# text = 'super secret mystery'
# hsh = Datablock().fromText(sha256_hash(text))
# abonents = [Abonent2(p = p, q = q, a = a, h = hsh, G = G) for i in range(3)]
#
#
# # Генерация коллективной ЭП на основе вычислений в группе точек эллиптической кривой
# s = (abonents[0].s + abonents[1].s + abonents[2].s) % q
# P = elips_sum(abonents[0].P, abonents[1].P)
# P = elips_sum(P, abonents[2].P)
# R = elips_sum(abonents[0].R, abonents[1].R)
# res = elips_sum(R, abonents[2].R)
# print(f'\nКЭП на основе вычислений в группе точек ЭК: ')
# print(f'R = {res}')
#
# # Проверка коллективной ЭП на основе вычислений в конечном поле
# hP = elips_mulscal(P, hsh.asInt())
# sG = elips_mulscal(G, s)
# res2 = elips_sum(hP, sG)
# print(f'Проверка R = {res2}')
# if res == res2:
#     print('Подпись действительна!')
# else:
#     print('Подпись не действительна!')
#
#
#
# q = int("8000000000000000000000000000000150fe8a1892976154c59cfc193accf5b3", 16)
# G = [int("2", 16),
#      int("8e2a8a0e65147d4bd6316030e16d19c85c97f0a9ca267122b96abbcea7e8fc8", 16)]
#
# abonents = [Abonent2(G=G) for i in range(3)]
# datas = ['тест1',
#          'тест2',
#          'тест3']
# vecs = [Datablock().random(256) for i in range(3)]
# hashs = [Datablock().fromText(sha256_hash(datas[i])) for i in range(3)]
#
# R = elips_sum(abonents[0].R, abonents[1].R)
# R = elips_sum(R, abonents[2].R)
# e = R[0] % q
# s = [(abonents[i].k - abonents[i].x * hashs[i].asInt() * e) % q for i in range(3)]
# S = (s[0] + s[1] + s[2]) % q
# print(f'\nКомпозиционная ЭП на основе вычислений в группе точек ЭК: ')
# print(f'Подпись = {S}')
#
#
# # Проверка композиционной ЭП на основе вычислений в группе точек эллиптической кривой
# P = elips_sum(elips_mulscal(abonents[0].P, hashs[0].asInt()), elips_mulscal(abonents[1].P, hashs[1].asInt()))
# P = elips_sum(P, elips_mulscal(abonents[2].P, hashs[2].asInt()))
# eP = elips_mulscal(P, e)
# sG = elips_mulscal(G, S)
# R2 = elips_sum(eP, sG)
# e2 = R2[0] % q
# if e == e2:
#     print('Подпись действительна!')
# else:
#     print('Подпись не действительна!')
