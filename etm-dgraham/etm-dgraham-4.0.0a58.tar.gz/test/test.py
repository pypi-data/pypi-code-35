#! /usr/bin/env python3

# count = 0
# dup = []
# uni = []
# for a in [2, 1, 7, 3, 5]:
#     for b in [1, 2, 3, 4, 6, 8, 9, 11]:
#         count += 1
#         if a == b:
#             dup.append(a)
#             # Break the inner loop...
#             break
#     else:
#         # Continue if the inner loop wasn't broken.
#         uni.append(a)
#         continue
#     # Inner loop was broken, break the outer.
#     continue
# print(count, dup, uni)

# count = 0
# dup = []
# for b in [1, 2, 3, 4, 6, 8, 9, 11]:
#     for a in [1, 3, 5, 7]:
#         count += 1
#         if a == b:
#             dup.append(a)
#             # Break the inner loop...
#             break
#     else:
#         # Continue if the inner loop wasn't broken.
#         continue
#     # Inner loop was broken, break the outer.
#     continue
# print(count, dup)

# A = [2, 1, 7, 3, 5]
# B = [1, 2, 3, 4, 6, 8, 9, 11]

# uni = [ x for x in A if x not in B ]

# print(uni)
def obfuscate(byt):
    # Use same function in both directions.  Input and output are bytes
    # objects.
    mask = b'keyword'
    lmask = len(mask)
    return bytes(c ^ mask[i % lmask] for i, c in enumerate(byt))

def test(s):
    print(s)
    data = obfuscate(s.encode())
    print(len(s), len(data), data)
    newdata = obfuscate(data).decode()
    print(newdata == s)


simple_string = 'Just plain ASCII'
unicode_string = ('sensei = \N{HIRAGANA LETTER SE}\N{HIRAGANA LETTER N}'
                  '\N{HIRAGANA LETTER SE}\N{HIRAGANA LETTER I}')

test(simple_string)
test(unicode_string)