# Burp Suite: Decoder

# Introduction

The burp suite decoder is a really usefull tool that's built into burp. It enables us to encode/decode/hash any value that we want and we can do it multiple times.

![Burp%20Suite%20Decoder%20f734161787184ddba02a1ae02444a4a3/Untitled.png](Burp%20Suite%20Decoder%20f734161787184ddba02a1ae02444a4a3/Untitled.png)

1. This is where we enter our value that we want to encode/decode/hash
2. This is where we select the algorithm we want to apply

Not how the value change text color when we encode it and background colour when we decode it. It will also take the color of the encoding/decoding type.

# Encoding

As shown in the screenshot we simply paste the value we want to encode in the field and select the encoding type we want to use. If we want to encode again, that's also possible.

![Burp%20Suite%20Decoder%20f734161787184ddba02a1ae02444a4a3/Untitled%201.png](Burp%20Suite%20Decoder%20f734161787184ddba02a1ae02444a4a3/Untitled%201.png)

As show we first encode in base64 and then URL encode the value to pass a base 64 value into a URI element.

# Decoding

As shown in the screenshot we simply paste the value we want to decode in the field and select the decoding type we want to use. If we want to decode again, that's also possible.

![Burp%20Suite%20Decoder%20f734161787184ddba02a1ae02444a4a3/Untitled%202.png](Burp%20Suite%20Decoder%20f734161787184ddba02a1ae02444a4a3/Untitled%202.png)

As show we first decode in base64 and then URL decode the value to read a base 64 value from a URI element.

# Hashing

![Burp%20Suite%20Decoder%20f734161787184ddba02a1ae02444a4a3/Untitled%203.png](Burp%20Suite%20Decoder%20f734161787184ddba02a1ae02444a4a3/Untitled%203.png)

As shown we can also hash our value, please not this does not have any colors to distinguish between the different hashing algorhitms so you won't see what you hash the value with after selecting the algorithm. As you may know hashing is an irreversable process as well.

# Smart decode

We can also try to smart decode our values where burp suite will try to guess the encoding algorithm and apply the decoding it needs to do.