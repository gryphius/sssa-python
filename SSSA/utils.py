import base64
import codecs
import math
import struct
from random import SystemRandom

class utils:
    prime = 0

    def __init__(self, prime=115792089237316195423570985008687907853269984665640564039457584007913129639747):
        self.prime = prime

    def random(self):
        return SystemRandom().randrange(self.prime)

    def split_ints(self, secret):
        result = []

        working = None
        byte_object = None
        try:
            byte_object = bytes(secret, "utf8")
        except:
            byte_object = bytes(secret)
        text = codecs.encode(byte_object, 'hex_codec').decode('utf8') + "00"*(32 - (len(byte_object) % 32))

        for i in range(0, int(len(text)/64)):
            result.append(int(text[i*64:(i+1)*64], 16))

        return result

    def merge_ints(self, secrets):
        result = ""

        for secret in secrets:
            hex_data = hex(secret)[2:].replace("L", "")
            result += "0"*(64 - (len(hex_data))) + hex_data

        byte_object = None
        try:
            byte_object = bytes(result, "utf8")

            return codecs.decode(byte_object, 'hex_codec').decode('utf8').rstrip("\00\x00")
        except:
            byte_object = bytes(result)

            return codecs.decode(byte_object, 'hex_codec').rstrip("\00\x00")
        pass

    def evaluate_polynomial(self, coefficients, value):
        result = 0
        for coefficient in reversed(coefficients):
            result = result * value + coefficient
            result = result % self.prime

        return result

    def to_base64(self, number):
        tmp = hex(number)[2:].replace("L", "")
        tmp = "0"*(64 - len(tmp)) + tmp

        try:
            tmp = bytes(tmp, "utf8")
        except:
            tmp = bytes(tmp)

        result = str(base64.urlsafe_b64encode(b'\00'*(64 - len(tmp)) + codecs.decode(tmp, 'hex_codec')).decode('utf8'))

        if len(result) != 44:
            print("error: result, tmp, number")
            print(result)
            print(len(result))
            print(tmp)
            print(len(tmp))
            print(number)
            print(hex(number))
            print(hex(codecs.decode(tmp, 'hex_codec')))
        return result

    def from_base64(self, number):
        byte_number = number
        try:
            byte_number = bytes(byte_number, "utf8")
        except:
            byte_number = bytes(byte_number)

        tmp = base64.urlsafe_b64decode(byte_number)

        try:
            tmp = bytes(tmp, "utf8")
        except:
            tmp = bytes(tmp)

        return int(codecs.encode(tmp, 'hex_codec'), 16)

    def gcd(self, a, b):
        if b == 0:
            return [a, 1, 0]
        else:
            n = int(math.floor(a*1.0/b))
            c = a % b
            r = self.gcd(b, c)
            return [r[0], r[2], r[1] - r[2]*n]

    def mod_inverse(self, number):
            remainder = (self.gcd(self.prime, number % self.prime))[2]
            if number < 0:
                remainder *= -1
            return (self.prime + remainder) % self.prime


    def shares_to_x_y(self,shares):
        x = []
        y = []
        # must be: len(shares[0])//88 == len(shares[0])/88
        for i in range(len(shares[0])//88):
            part_x = []
            part_y = []
            for share in shares:
                part_x.append(self.from_base64(share[88*i+0:88*i+44]))
                part_y.append(self.from_base64(share[88*i+44:88*i+88]))
            x.append(tuple(part_x))
            y.append(tuple(part_y))
        return x,y

    # extended_gcd, divmod, lagrange_interpolate are copied from https://en.wikipedia.org/wiki/Shamir%27s_Secret_Sharing

    def extended_gcd(self, a, b):
        """
        Division in integers modulus p means finding the inverse of the
        denominator modulo p and then multiplying the numerator by this
        inverse (Note: inverse of A is B such that A*B % p == 1) this can
        be computed via extended Euclidean algorithm
        http://en.wikipedia.org/wiki/Modular_multiplicative_inverse#Computation
        """
        x = 0
        last_x = 1
        y = 1
        last_y = 0
        while b != 0:
            quot = a // b
            a, b = b, a % b
            x, last_x = last_x - quot * x, x
            y, last_y = last_y - quot * y, y
        return last_x, last_y

    def divmod(self, num, den, p):
        """Compute num / den modulo prime p

        To explain what this means, the return value will be such that
        the following is true: den * divmod(num, den, p) % p == num
        """
        inv, _ = self.extended_gcd(den, p)
        return num * inv

    def lagrange_interpolate(self, x, x_s, y_s, p):
        """
        Find the y-value for the given x, given n (x, y) points;
        k points will define a polynomial of up to kth order.
        """
        k = len(x_s)
        assert k == len(set(x_s)), "points must be distinct"
        def PI(vals):  # upper-case PI -- product of inputs
            accum = 1
            for v in vals:
                accum *= v
            return accum
        nums = []  # avoid inexact division
        dens = []
        for i in range(k):
            others = list(x_s)
            cur = others.pop(i)
            nums.append(PI(x - o for o in others))
            dens.append(PI(cur - o for o in others))
        den = PI(dens)
        num = sum([self.divmod(nums[i] * den * y_s[i] % p, dens[i], p)
                for i in range(k)])
        return (self.divmod(num, den, p) + p) % p