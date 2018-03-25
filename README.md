# cipher-algorithms
Requires `nunmpy>=1.14.2` to work.
## Hill cipher
Create an instance of class Hill
```
from cipher.hill import Hill

hill = Hill()
```
Then encrypt a text with encrypt() function
```
text = "Once upon a midnight dreary, while I pondered, weak and weary, Over many a quaint and curious volume of forgotten lore"
encrypted_text = hill.encrypt(text)
```
`encrypted_text` will contain an encrypted string with the current key like `boiexibosgtqzrxqebxttcswtlrnlwbojfxtxbeekkyvcytcgsbxjxnayyuamewdnatrnwqciqdppvsopknznhxezvkzhqjk`
Decrypt with decrypt()
```
encrypted_text = "boiexibosgtqzrxqebxttcswtlrnlwbojfxtxbeekkyvcytcgsbxjxnayyuamewdnatrnwqciqdppvsopknznhxezvkzhqjk"
plain_text = hill.decrypt(encrypted_text)
```
`plain_text` will contain the decrypted text like `onceuponamidnightdrearywhileiponderedweakandwearyovermanyaquaintandcuriousvolumeofforgottenlore`
