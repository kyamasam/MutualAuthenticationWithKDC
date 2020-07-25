from string import ascii_letters
import base64


def encrypt(character_string, key):
    int_key = int(key)

    new_character_string = ''
    for character in character_string:
        if character in ascii_letters:
            new_character_string = new_character_string + ascii_letters[
                (ascii_letters.index(character) + int_key) % len(ascii_letters)]
        else:
            # cater for non ascii letters (spaces)
            new_character_string += character

    # convert to utf8
    base64_string = str(base64.b64encode(new_character_string.encode("utf-8")), "utf-8")

    print("Encrypted message :", base64_string)
    return base64_string


def decrypt(encrypted_message, key):
    int_key = int(key)
    # print("Converting integer to base 64 string.... \n\n")

    # convert from base64encrypted_message
    semi_original_string = str(base64.b64decode(encrypted_message), "utf-8")

    print(semi_original_string)

    # print("Converting to original characters (Previous Number of Alphabet)..... \n\n")

    # convert to unmodified string
    original_character_string = ''
    for character in semi_original_string:
        if character in ascii_letters:
            original_character_string = original_character_string + ascii_letters[
                (ascii_letters.index(character) - int_key) % len(ascii_letters)]
        else:
            # cater for non ascii letters (spaces)
            original_character_string += character

    print("Decrypted message :", original_character_string)
    return original_character_string