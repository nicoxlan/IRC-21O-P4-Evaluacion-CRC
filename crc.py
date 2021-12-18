import bitarray
import numpy as np

cont = 0

def cyclic_redundancy_check(filename: str, divisor: str, len_crc: int) -> int:
    """
    This function computes the CRC of a plain-text file
    arguments:
    filename: the file containing the plain-text
    divisor: the generator polynomium
    len_crc: The number of redundant bits (r)
    """
    from bitarray import bitarray
    redundancy = len_crc * bitarray('0')
    bin_file = bitarray()
    p = bitarray(divisor)
    len_p = len(p)
    with open(filename, 'rb') as file:
        bin_file.fromfile(file)
    cw = bin_file + redundancy
    rem = cw[0 : len_p]
    end = len(cw)
    for i in range(len_p, end + 1):
        if rem[0]:
            rem ^= p
        if i < end:
            rem = rem << 1
            rem[-1] = cw[i]
    return bin_file + rem[len_p-len_crc : len_p]

"""
Prueba del funcionamiento de la función cyclic_redundacy_check
http://www.sunshine2k.de/coding/javascript/crc/crc_js.html
"""


def cyclic_redundacy_check_decoder(txt: bitarray, divisor: str, len_crc: int) -> int:

    from bitarray import bitarray
    redundancy = len_crc * bitarray('0')
    bin_file = txt
    p = bitarray(divisor)
    len_p = len(p)
    cw = bin_file + redundancy
    rem = cw[0 : len_p]
    end = len(cw)
    for i in range(len_p, end + 1):
        if rem[0]:
            rem ^= p
        if i < end:
            rem = rem << 1
            rem[-1] = cw[i]
    return rem[len_p-len_crc : len_p]


def error_generator(lenTxt: int, txt: bitarray, seed: int, n: int) -> int:
    from bitarray import bitarray
    from numpy import random
    txtRaw = txt[0:len(txt)-4]
    crc = txt[len(txt)-4:len(txt)]
    # Generamos la rafaga
    np.random.seed(seed)
    e = np.random.randint(low = 1, high = n, size = 1)[0]
    start = np.random.randint(low = 0, high = len(txtRaw)-n, size = 1)[0]
    randPos = np.random.randint(low = 0, high = n-1, size = e)
    j = 0
    for i in range(start, start+n):
        if j in randPos:
            if txtRaw[i] == 0:
                txtRaw[i] = 1
            else:
                txtRaw[i] = 0
        j = j + 1
    return txtRaw + crc


def validator(crc: bitarray, option: int, n: int) -> float:
    global cont
    if not option:
        if 1 in crc:
            cont = cont + 1
    else:
        return cont/n


def main():
    # Se crea el mensaje con CRC
    txtCrc = cyclic_redundancy_check('test.txt', '11110', 4)

    # Se generan n rafagas de errores y verifica el mensaje resultante n veces y se pasa la validador
    n = 5
    repetitions = 1000
    for i in range(repetitions):
        txtCrcError = error_generator(len(txtCrc)-4, txtCrc, 3837023-i, n)
        txtCrcVerify = cyclic_redundacy_check_decoder(txtCrcError, '11110', 4 )
        validator(txtCrcVerify, 0, repetitions)

    result = validator(txtCrcVerify, 1, repetitions)
    print("Probabilidad: ", result)

    '''
    print(txtCrcVerify)
    print("\nTexto original con crc:", txtCrc)
    print("Texto con error con crc:", txtCrcError)
    #print(txtcrc[len(txtcrc)-4:len(txtcrc)])
    print(bitarray.bitarray(txtCrcError[0:len(txtCrcError)-4]).tobytes().decode(errors='ignore'))
    '''

main()
