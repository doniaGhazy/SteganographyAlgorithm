#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  8 02:10:01 2018

@author: ahmadrefaat
"""

from scipy.io import wavfile
import numpy as np


def encode(data,samplerate ,msg, key, outFile_name):
   
    # Find the first Non Zero sample
    first_non_zero = np.where(data != 0)[0][0]

    
    # Encoding each character to 8 Bits
    my_string_in_bits = []
    for i in range(len(msg)):
        my_string_in_bits.append('{0:08b}'.format(ord(msg[i])))
    
    # ADD NULL AT THE END
    my_string_in_bits.append('{0:08b}'.format(0))

    
    # START FROM THE FIRST NON ZER0 + KEY
    # FOR EACH CHARACTER EXAMPLE: 01101100
    # WE START STORING THE MSB IN THE CHARACTER (0) IN THE LSB OF THE BYTE WE WISH TO ENCODE 
    # THE ARRAY DATA IS AN INTEGER ARRAY => EACH ELEMENT IS 4 BYTES THEREFORE WE NEED TO SHIFT THE BIT TO ENCODE

                                  
    i = first_non_zero + key
    for j in range(len(my_string_in_bits)):
        print (my_string_in_bits[j])
        for k in range(4):
            
            if k == 0:
                shifted_bit = 1
            else:
                shifted_bit = (1 << (k*8 - 1))
                
            # SETTING THE BIT AT INDEX K * 8 (0,8,16,24) WITH THE CORRESPONDING BIT IN THIS CHARACTER
            # THIS LOOP IS FOR THE 4 LEFT MOST BITS IN THE CHARACTER WHICH ARE STORED AT INDEX I
            if my_string_in_bits[j][k] == '1':
                data[i] |=  shifted_bit
            else:
                data[i] &= ~shifted_bit
    
            
        for k in range(4):
 
            if k == 0:
                shifted_bit = 1
            else:
                shifted_bit = (1 << (k*8 - 1))
            
            # SETTING THE BIT AT INDEX K * 8 (0,8,16,24) WITH THE CORRESPONDING BIT IN THIS CHARACTER
            # THIS LOOP IS FOR THE 4 RIGHT MOST BITS IN THE CHARACTER WHICH ARE STORED AT INDEX I+1
            if my_string_in_bits[j][k+4] == '1':
                data[i+1] |=  shifted_bit
            else:
                data[i+1] &= ~shifted_bit
    
        i = i + key + 2
    

    real_back_again_32int = np.array(data,dtype=np.int32)    
    final_out = np.vstack((real_back_again_32int,real_back_again_32int)).T
    wavfile.write(outFile_name,samplerate,final_out)



def decode(data, key):
    # Find the first Non Zero sample
    first_non_zero = np.where(data != 0)[0][0]

    i = first_non_zero + key
    while True:
        ch = ''
        for k in range(4):
            if k == 0:
                bit_to_decode = 1
            else:
                bit_to_decode = (1 << (k*8 - 1))
                
            result = data[i] & bit_to_decode
            if int(result) == 0:
                ch += '0'
            else:
                ch += '1'
                
        
        for k in range(4):
            if k == 0:
                bit_to_decode = 1
            else:
                bit_to_decode = (1 << (k*8 - 1))
                
            result = data[i+1] & bit_to_decode
            if int(result) == 0:
                ch += '0'
            else:
                ch += '1'
                
        
        char_to_get = int(ch,2)
        if char_to_get == 0:
            print ('found 0')
            break
        else:
            print (chr(char_to_get))
        
        i = i + key + 2
        
        

    
message = "Hello Friends"
sRate, myData = wavfile.read('./sound.wav')
myNewData = np.array(myData[:,0]).astype(np.uint32)
theKey = 16
outFile = "output.wav"

# Encoding Part
encode(data = myNewData , 
       samplerate = sRate, 
       msg = message , 
       key = theKey, 
       outFile_name = outFile)


sRate, myData = wavfile.read('./' + outFile)
myNewData = np.array(myData[:,0]).astype(np.uint32)
# Decoding Part
decode(data = myNewData , key = theKey)
     