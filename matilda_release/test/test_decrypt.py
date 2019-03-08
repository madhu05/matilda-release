from matilda_release.util.encoder import AESCipher

enc = AESCipher()

def test_decrypt():
    txt1 = '4qAgX+VruuzBoS9bX88xvVJNjjdV+o6Yn8pyvf8N8FarKKCJ/hGjZ3TyWwS1bV0khApRxALpr72P32EvYBQZ8Q7wTnqN5z849ZK9kid6GFBceYgyuQ4ON2yLhxsRb2YPGrPgWRm98U7t0OMWB/4AomP85NvHEXblgyO9ltw4BgIT7AuFn75aMcxoSVvSV+8a'
    txt2 = 'tFVGCCj3BVa6vkFgMgh5aikWSQ7dByRd+Tte32xoS9g/lOIL2xx4GZvBgTDRCcG1VkQLXAmBsGyyJcp5URNAI3UCAXxkE4gi3ui7NIWMP4ppBATkIaR/33ryS0O45AHdrnZ83fjd3fQuwXT5cxC+3Xcfs/v+yjdaXaA6Ntx/gsZymTd+qwj3hbx++IVoWhNApEkIJyR9SvE/ENEkUmgXegGFoK5Av16hW7LtYPezl2HDl1r05RXUA6WwGC+yPsAiLKRx/+AEvbQNyrh+IrHv1QW4azFG5OSIYEr27BAmMf01piUTR1f76A73P81zclFG'
    print (enc.decrypt(txt1))
    print (enc.decrypt(txt2))

test_decrypt()
