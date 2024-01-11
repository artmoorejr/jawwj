# lib_s_validate
# used to validate words
# commented out code to create new database as well.
# was formerly lib_validate but converted to use shelve


import shelve

word_list = []
word_dic = {}


def alphagram(word: str) -> str:  # convert word to alphagram for db storage/retrieval

    ag_list = sorted(list(word.upper()))
    a_gram = ''.join(ag_list)
    return a_gram


def validate(words: list[str]) -> bool:

    valid = True

    for query in words:

        anagram_list = []

        with shelve.open("assets/nwl2020s.db","r") as master_list:
            if alphagram(query) in list(master_list.keys()):
                anagram_list = master_list[alphagram(query)]

        valid = True if query.upper() in anagram_list and valid else False

        if not valid:
            break

    return valid

# ---- code block to generate new word database
# ---- update BOTH filenames or you will be unhappy

# with open("nwl2020.txt", 'r') as f:
#     word_list = f.readlines()

# word_list = [x.strip().upper() for x in word_list]
#
# for word in word_list:
#     key = alphagram(word)
#     if key in word_dic.keys():
#         word_dic[key].append(word)
#     else:
#         word_dic[key] = [word]

# print("creating shelf")
#
# with shelve.open("nwl2020s.db") as wl:
#     for key, value in word_dic.items():
#         wl[key] = value


# print(word_list)

# manual test below
# default = ""
#
# while default != "0":
#     anagrams = ""
#     default = input("Word to look up? ")
#
#     checklist = default.split()
#     print(checklist)
#
#     print("VALID" if validate(checklist) else "UNACCEPTABLE")
