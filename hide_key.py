from base64 import b64encode
import sys, os
from PIL import Image

dict = [chr(x) for x in range(65,91)] + [chr(x) for x in range(97,123)] + [chr(x) for x in range(48,58)] + ['+','/']

def encode_word(word, secret):
    first_equal = word.index('=')
    to_modify = word[first_equal-1]
    delta = int(secret, 2)
    encoded_char = dict[dict.index(to_modify) + delta]
    encoded_string = word[:first_equal-1] + encoded_char + (len(word)-first_equal) * '='
    return encoded_string
    
def count_equals(word_list):
    equals = 0
    for word in word_list:
        equals += word.count('=')
    count = 2*equals
    return count

def encode(text, secret, verbose=False):
    words = text.split(' ')
    words_b64 = [b64encode((word+" ").encode('ascii')).decode('ascii') for word in words]
    secret_max_length = count_equals(words_b64)
    if verbose: print('[*] Number of words: %d' % len(words))
    if verbose: print('[*] Maximum length of the secret: %d' % ((secret_max_length-16)//7))
    if verbose: print('[*] Length of the secret: %d' % len(secret))
    if 7*len(secret)+16 > secret_max_length:
        raise ValueError('[ERROR] The text size is too small for the secret. Please add more text.')
    if verbose: print('[*] Text size OK')
    bin_secret = bin(len(secret))[2:].zfill(16)
    for char in secret:
        bin_secret += bin(ord(char))[2:].zfill(7)
    bin_secret = bin_secret + (secret_max_length - len(bin_secret)) * '0'
    encoded_list = []
    for word in words_b64:
        equals = word.count('=')
        if equals > 0:
            encoded_list.append(encode_word(word, bin_secret[:2*equals]))
            bin_secret = bin_secret[2*equals:]
        else:
            encoded_list.append(word)
    return encoded_list


def hide_in_b64():
    try:
        file = input("Enter file containing plain text where you whant to hide secret : ")
        with open(file, "r") as f:
            text = f.read()
        secret = input("Enter secret you whant to hide : ")
        encoded_text = encode(text=text,secret=secret)
        with open("encoded_text.txt", "w") as f:
            f.write('\n'.join(encoded_text))
        print("[*] Secret hidden successfully in encoded_text.txt !")
    except Exception as e:
        print("[*] Sorry ! you failed !")
        end = input("[*] Press any key to exit")
        sys.exit(0)


def genData(data):
        newd = []

        for i in data:
            newd.append(format(ord(i), '08b'))
        return newd

def modPix(pix, data):

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

def encode_enc(newimg, data):
    w = newimg.size[0]
    (x, y) = (0, 0)

    for pixel in modPix(newimg.getdata(), data):

        newimg.putpixel((x, y), pixel)
        if (x == w - 1):
            x = 0
            y += 1
        else:
            x += 1

def encode_file():
    try:
        img = input("Enter image name where you whant to hide the b64 encoded key : ")
        image = Image.open(img, 'r')
        
        with open('encoded_text.txt', "r") as file:
            data = file.read() 
        if (len(data) == 0):
            raise ValueError('Data is empty')

        newimg = image.copy()
        encode_enc(newimg, data)
        new_img_name = img
        newimg.save(new_img_name)
        print(f"Message hidden in {new_img_name} file")
        os.remove('encoded_text.txt')
    except Exception as e:
        print("[*] Sorry ! you failed !")
        print(e)
        end = input("[*] Press any key to exit")
        sys.exit(0)



if __name__ == "__main__":
    hide_in_b64()
    encode_file()