from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64
from PIL import Image
import re, sys
from base64 import b64encode, b64decode
import re


def genData(data):
    try:
        newd = []

        for i in data:
            newd.append(format(ord(i), '08b'))
        return newd
    except Exception as e:
        print("Sorry ! you failed !")
        end = input("Press any key to exit")
        sys.exit(0)

def modPix(pix, data):
    try:
        datalist = genData(data)
        lendata = len(datalist)
        imdata = iter(pix)

        for i in range(lendata):

            pix = [value for value in imdata.__next__()[:3] +
                                    imdata.__next__()[:3] +
                                    imdata.__next__()[:3]]


            for j in range(0, 8):
                if (datalist[i][j] == '0' and pix[j]% 2 != 0):
                    pix[j] -= 1

                elif (datalist[i][j] == '1' and pix[j] % 2 == 0):
                    if(pix[j] != 0):
                        pix[j] -= 1
                    else:
                        pix[j] += 1

            if (i == lendata - 1):
                if (pix[-1] % 2 == 0):
                    if(pix[-1] != 0):
                        pix[-1] -= 1
                    else:
                        pix[-1] += 1

            else:
                if (pix[-1] % 2 != 0):
                    pix[-1] -= 1

            pix = tuple(pix)
            yield pix[0:3]
            yield pix[3:6]
            yield pix[6:9]
    except Exception as e:
        print("Sorry ! you failed !")
        end = input("Press any key to exit")
        sys.exit(0)


def encode_enc(newimg, data):
    try:
        w = newimg.size[0]
        (x, y) = (0, 0)

        for pixel in modPix(newimg.getdata(), data):

            newimg.putpixel((x, y), pixel)
            if (x == w - 1):
                x = 0
                y += 1
            else:
                x += 1
    except Exception as e:
        print("Sorry ! you failed !")
        end = input("Press any key to exit")
        sys.exit(0)

def encode_file(data_to_hide=None, source_image=None ):
    try:
        if not source_image:
            img = input("Enter target image name : ")
        else:
            img = source_image
        image = Image.open(img, 'r')
        
        
        if not data_to_hide:
            data = input("Enter data to be encoded : ")
            if (len(data) == 0):
                raise ValueError('Data is empty')
        else:
            data = data_to_hide

        newimg = image.copy()
        encode_enc(newimg, data)
        new_img_name = img
        newimg.save(new_img_name)
        print(f"Message hidden in {new_img_name} file")
    except Exception as e:
        print("Sorry ! you failed !")
        end = input("Press any key to exit")
        sys.exit(0)

def decode_file(source_filename=None):
    try:
        if not source_filename:
            img = input("Enter key : ")
            image = Image.open(img, 'r')
        else:
            image = Image.open(source_filename, 'r')

        data = ''
        imgdata = iter(image.getdata())

        while (True):
            pixels = [value for value in imgdata.__next__()[:3] +
                                    imgdata.__next__()[:3] +
                                    imgdata.__next__()[:3]]

            binstr = ''

            for i in pixels[:8]:
                if (i % 2 == 0):
                    binstr += '0'
                else:
                    binstr += '1'

            data += chr(int(binstr, 2))
            if (pixels[-1] % 2 != 0):
                return data
    except Exception as e:
        print("Sorry ! you failed !")
        end = input("Press any key to exit")
        sys.exit(0)

dict = [chr(x) for x in range(65,91)] + [chr(x) for x in range(97,123)] + [chr(x) for x in range(48,58)] + ['+','/']

def decode_word(word):
    try:
        first_equal = word.index('=')
        encoded_char = word[first_equal-1]
        base = b64encode(b64decode(word))
        base_char = chr(base[first_equal-1])
        secret_index = dict.index(encoded_char) - dict.index(base_char)
        secret = "{0:b}".format(secret_index).zfill(2*word.count('='))
        return secret
    except Exception as e:
        print("Sorry ! you failed !")
        end = input("Press any key to exit")
        sys.exit(0)

def decode(encoded_list, verbose=False):
    try:
        bin_secret = ''
        decoded_string = ''
        for word in encoded_list:
            if word.count('=') > 0:
                bin_secret += decode_word(word)
            decoded_string += b64decode(word).decode('ascii')
        secret_length = int(bin_secret[:16], 2)
        bin_secret = bin_secret[16:]
        binary_letters = re.findall('.{7}', bin_secret)[:secret_length]
        secret = ''.join(chr(int(letter, 2)) for letter in binary_letters)
        return secret, decoded_string
    except Exception as e:
        print("Sorry ! you failed !")
        end = input("Press any key to exit")
        sys.exit(0)

def base64_padding_extractor(b64_data):
    try:
        secret, decoded_string = decode(b64_data.split('\n'))
        return secret.encode('utf-8')
    except Exception as e:
        print("Sorry ! you failed !")
        end = input("Press any key to exit")
        sys.exit(0)

def aes_decrypt(key, encrypted_text):
    try:
        encrypted_data = base64.b64decode(encrypted_text)
        iv = encrypted_data[:16]
        ciphertext_bytes = encrypted_data[16:]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext_padded = cipher.decrypt(ciphertext_bytes)
        plaintext = unpad(plaintext_padded, AES.block_size)
        plaintext_str = plaintext.decode('utf-8')

        return plaintext_str
    except Exception as e:
        print("Sorry ! you failed !")
        end = input("Press any key to exit")
        sys.exit(0)

def aes_encrypt(key, plaintext):
    try:
        iv = get_random_bytes(16)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext_padded = pad(plaintext.encode('utf-8'), AES.block_size)
        ciphertext_bytes = cipher.encrypt(plaintext_padded)
        encrypted_data = iv + ciphertext_bytes
        encrypted_text = base64.b64encode(encrypted_data).decode('utf-8')
        return encrypted_text
    except Exception as e:
       print("Sorry ! you failed !")
       end = input("Press any key to exit")
       sys.exit(0)

def main_hide():
    try:
        choice = input("Do you want to hide a message or a file? (message/file) : ")
        if choice.lower() == 'file':
            file_to_hide = input("Enter file to hide : ")
            with open(file_to_hide, "rb") as fh:
                message = base64.b64encode(fh.read()).decode('utf-8')
        elif choice.lower() == 'message':
            message = input("Enter the message you want to hide : ")
        else:
            print("Invalid choice")
            sys.exit(1)
        extracted_key = decode_file()
        decrypted_key = base64_padding_extractor(extracted_key)
        final_output = aes_encrypt(decrypted_key, str(message))
        encode_file(data_to_hide=final_output)
        end = input("Press any key to exit")
        sys.exit(0)
    except Exception as e:
        print(e)
        print("Sorry ! you failed !")
        end = input("Press any key to exit")
        sys.exit(0)

def main_extract():
    try:
        extracted_key = decode_file()
        decrypted_key = base64_padding_extractor(extracted_key)
        file_to_decode = input("Enter file to decode : ")
        decoded_file = decode_file(file_to_decode)
        final_res = aes_decrypt(decrypted_key, decoded_file)
        if len(final_res) > 10000:
            target_image = input("Enter file name to recreate : ")
            with open(target_image, "wb") as fh:
                fh.write(base64.b64decode(final_res))
            print(f"Hidden picture is : \n{target_image}")
        else:
            print(f"Hidden message is : \n{final_res}")
        end = input("Press any key to exit")
        sys.exit(0)
    except Exception as e:
        print("Sorry ! you failed !")
        end = input("Press any key to exit")
        sys.exit(0)

if __name__ == '__main__':
    choice  = input("Do you want to hide or extract? (hide/extract) : ")
    if str(choice).lower() == 'hide':
        main_hide()
    elif str(choice).lower() == 'extract':
        main_extract()
    else:
        print("Invalid choice")
        sys.exit(1)