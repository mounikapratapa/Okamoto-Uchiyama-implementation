from miller_rabin_test import is_prime
import random

def generate_prime_candidate(size):
    p = random.getrandbits(size)
    p |= (1 << size - 1) | 1
    return p
def generate_prime_numbers(size):
    p = 4
    while not is_prime(p):
        p = generate_prime_candidate(size)
    return p
def gcd(a, b):
    while b:
        return gcd(b, a%b)
    return a
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)
def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

def L(x, p):
    return ((x-1) // p)
def keys(size):
    p = generate_prime_numbers(size)
    q = generate_prime_numbers(size)
    assert p != q
    n =  p*p*q
    while True:
        x =  random.randint(23,n)
        g = pow(x, p-1, p**2)
        if g != 1:
            break
    return((n, g), (p, q))
    
def enc(pk,pt):
    n,g = pk
    r = random.randint(23,n)
    ct = pow(g, (pt+(n*r)), n)
    return ct
def dec(sk,g,ct):
    p,q = sk
    x1 = pow(ct, p-1, p**2)
    x2 = pow(g, p-1, p**2)
    L1 = L(x1,p)
    print(L1)
    L2 = modinv(L(x2,p),p)
    message = (L1* L2) % p
    return message
def main():
    pk, sk = keys(32)
    n,g= pk
    print(pk,sk)
    disp = input("Do you want to test for homomorphism?(y/n):")
    if(disp == 'y'):
        print("Good choice,let us have some fun!")
        p1 = input("Enter the first integer:")
        p2 = input("Enter the second integer:")
        c1 = enc(pk,int(p1))
        c2 = enc(pk,int(p2))
        c3 = c1 * c2
        print("Your first cipher text is:",c1)
        print("Your second cipher text is:",c2)
        print("cipher product is:", c3)
        print("Decrypting")
        message = dec(sk,g, c3)
        print(message)
        d = input("Is this less than plain m1 + m2?(y/n):")
        if(d == 'y'):
            print("Eureka!")
        else:
            print("Okamoto_Uchiyama Failed!")
    else:    
        pt = input("Enter the integer you want to encrypt:")
        print("Encrypting...")
        ct = enc(pk,int(pt))
        print("Your cipher text is:",ct)
        print("Decrypting...")
        message = dec(sk,g,ct)
        print("Here is the secret in plain text:", message)
    
main()


        
    
