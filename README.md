# cipher-algorithms
Requires plugins. 
```
nunmpy>=1.14.2
matplotlib>=2.2.2
```
Use `pip install -r requirements.txt` to install them.
## Hill cipher
> In classical cryptography, the Hill cipher is a polygraphic substitution cipher based on linear algebra. Invented by Lester S. Hill in 1929, it was the first polygraphic cipher in which it was practical (though barely) to operate on more than three symbols at once. The following discussion assumes an elementary knowledge of matrices.
### Instructions
Create an instance of class Hill and choose the key matrix dimensions or the used alphabet (default is ascii)
```python
from cipher.hill import Hill

hill = Hill(key_dimension=2, alphabet=None)
```
Then encrypt a text with `encrypt()` function
```python
text = "Once upon a midnight dreary, while I pondered, weak and weary"
encrypted_text = hill.encrypt(text)
```
`encrypted_text` will contain an encrypted string with the current key like `broanlbrkcrnlkbxcfdizfmafmxkbpbrpedirueqkowhiczfvh`

Decrypt with `decrypt()`
```python
encrypted_text = "broanlbrkcrnlkbxcfdizfmafmxkbpbrpedirueqkowhiczfvh"
plain_text = hill.decrypt(encrypted_text)
```
`plain_text` will contain the decrypted text like `onceuponamidnightdrearywhileiponderedweakandweary`

## Vigenère cipher
>The Vigenère cipher (French pronunciation: ​[viʒnɛːʁ]) is a method of encrypting alphabetic text by using a series of interwoven Caesar ciphers based on the letters of a keyword. It is a form of polyalphabetic substitution
### Instructions
Create an instance of class Vigenere and choose the alphabet and key lenght or directly instert your key.
```python
from cipher.Vigenere import Vigenere

vigenere = Vigenere(key=None, alphabet=None, key_lenght=32)
```
Then encrypt a text with `encrypt()` function
```python
text = "Once upon a midnight dreary, while I pondered, weak and weary"
encrypted_text = vigenere.encrypt(text)
```
`encrypted_text` will contain an encrypted string with the current key like `zfgxjglwuonfgpyejbqkflmocdihumdkowvxsnbjecsfplsoo`

Decrypt with `decrypt()`
```python
encrypted_text = "zfgxjglwuonfgpyejbqkflmocdihumdkowvxsnbjecsfplsoo"
plain_text = vigenere.decrypt(encrypted_text)
```
`plain_text` will contain the decrypted text like `onceuponamidnightdrearywhileiponderedweakandweary`
