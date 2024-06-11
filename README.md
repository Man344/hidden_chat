# hidden_chat Project
Hidden_chat is a personal project created for a security course during my final year of engineering.

## Context
Imagine you are an agent in an intelligence agency, and you need to create a program that allows remote secret agents to send messages or pictures to the central agency.

### Constraints
You need to use classic email channels to avoid detection, possibly in a cyber cafe using a public network. Additionally, if the agent is caught, the sent messages must not be decodable! Therefore, the program must be hidden.

## Manual

### 1. hide_key.py
This program is strictly confidential and must be used in a secure context on a secure computer. It allows you to hide a secret AES 256 key in a picture using steganography.

However, to make it more secure, the key is first hidden in a base64 encoded random text before being hidden in the picture.

It is hidden using the padding bits of the base64 encoding.

You are free to insert honey pots in the random text, such as:

```secret key is : myWrongRandomKeyOf32chars```

### 2. chat_engine.py

#### How to Hide?
This program needs to be installed on the secret agent's computer. Transform it into an executable file using a library like `pyinstaller`, and hide it in a directory. 

You can also make it a hidden file and build a file, such as a .png or any picture file, which should be a renamed .lnk file containing a link targeting the .exe file.

For example:

```C:\Windows\System32\cmd.exe /c myRenamedExeFile.png```

So now you have, for example, a .png (hidden .exe) set as a hidden file and a .png (hidden .lnk) file, which launches the .exe.

#### How to Use?
Click on the .lnk hidden file, which will launch the program. This program can hide or extract messages or pictures inside/from a picture using an AES256 key provided by another picture (generated with the hide_key.py program).

Thus, the agent only needs to have the same key (hidden in a picture) as the agency. All the messages should be sent, encrypted, using classic email. The only way to decode the messages is to capture the secret agent's computer, reverse engineer the .exe (hidden in a .png) to find the key, and then try to decode all pictures on the computer to find the key.

#### Limitations
The random text containing the AES key must be long because each word contains only one or two padding bits where we can hide data.

The chat engine only works for .png pictures.