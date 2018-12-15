'''
Based on: https://rosettacode.org/wiki/MD5/Implementation#Python
'''
import math


class MD5:
    # Per round shift amounts:
    __rotate_amounts = [7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,  # 0 to 15
                        5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20,  # 16 to 31
                        4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,  # 32 to 47
                        6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21]  # 48 to 63

    # Use binary integer part of the sines of integers (Radians) as constants
    # this is performed by performing logical AND operation with largest 32 bit integer -  0xFFFFFFFF
    __constants = [int(abs(math.sin(i + 1)) * 2 ** 32) & 0xFFFFFFFF for i in range(64)]

    # Define initial values:
    __init_values = [0x67452301,  # A
                     0xefcdab89,  # B
                     0x98badcfe,  # C
                     0x10325476]  # D

    __functions = 16 * [lambda b, c, d: (b & c) | (~b & d)] + \
                  16 * [lambda b, c, d: (d & b) | (~d & c)] + \
                  16 * [lambda b, c, d: b ^ c ^ d] + \
                  16 * [lambda b, c, d: c ^ (b | ~d)]

    __index_functions = 16 * [lambda i: i] + \
                        16 * [lambda i: (5 * i + 1) % 16] + \
                        16 * [lambda i: (3 * i + 5) % 16] + \
                        16 * [lambda i: (7 * i) % 16]

    @staticmethod
    def __left_rotate(x, amount):
        x &= 0xFFFFFFFF
        return ((x << amount) | (x >> (32 - amount))) & 0xFFFFFFFF

    def __md5(self, text):
        message = bytearray(text.encode('ascii'))  # copy our input into a mutable buffer
        orig_len_in_bits = (8 * len(message)) & 0xffffffffffffffff
        message.append(0x80)
        while len(message) % 64 != 56:
            message.append(0)
        message += orig_len_in_bits.to_bytes(8, byteorder='little')

        hash_pieces = self.__init_values[:]
        for chunk_offset in range(0, len(message), 64):
            a, b, c, d = hash_pieces
            chunk = message[chunk_offset:chunk_offset + 64]
            for i in range(64):
                f = self.__functions[i](b, c, d)
                g = self.__index_functions[i](i)
                to_rotate = a + f + self.__constants[i] + int.from_bytes(chunk[4 * g:4 * g + 4], byteorder='little')
                new_b = (b + self.__left_rotate(to_rotate, self.__rotate_amounts[i])) & 0xFFFFFFFF
                a, b, c, d = d, new_b, b, c
            for i, val in enumerate([a, b, c, d]):
                hash_pieces[i] += val
                hash_pieces[i] &= 0xFFFFFFFF

        return sum(x << (32 * i) for i, x in enumerate(hash_pieces))

    @staticmethod
    def __md5_to_hex(digest):
        raw = digest.to_bytes(16, byteorder='little')
        return '{:032x}'.format(int.from_bytes(raw, byteorder='big'))

    def get_hash(self, text):
        return self.__md5_to_hex(self.__md5(text))


if __name__ == '__main__':
    demo = ['',
            'a',
            'abc',
            'message digest',
            'abcdefghijklmnopqrstuvwxyz',
            'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789',
            '12345678901234567890123456789012345678901234567890123456789012345678901234567890',
            'The quick brown fox jumps over the lazy dog',
            'The quick brown fox jumps over the lazy dog.']

    for msg in demo:
        print('{0} - {1}'.format(MD5().get_hash(msg), msg))
        # print(type(message))
