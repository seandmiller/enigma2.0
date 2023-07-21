from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = [
    'http://localhost:3000',
    'https://localhost:3000',
]
app.add_middleware(
    CORSMiddleware,
    allow_origins        = origins,
    allow_credentials    = True,
    allow_methods        = ['*'],
    allow_headers        = ['*']
)

class EnigmaMachine:
  def __init__(self, rotor_choices: list, rotor_settings: list, plug_board : list = [] ):
      self.rotor_choices = rotor_choices
      self.rotor_settings = rotor_settings
      self.plug_board = plug_board
      self.rt_1 = ['USROTZIBHQDNA_WLGCYXEPJVFKM1234567890',
                   'THSMEBANOVXGPKYQW09DC1I2J3F4Z5L6R7U8_'] 
      self.rt_2 = ['CB1A2DE3U4Q56R78_SLH0Z9JYMKFGINOPTVWX',
                   'D1A2EBZIMNYOKTWPVXC_LJF0H9RS876UQ5G43']
      self.rt_3 = ['DECBAFIJMNHKLU_1234567890RPGOQYWXZSTV',
                   'ABDECONJPQL0987654321MKIHGTUZF_VWXRSY']
      self.rt_4 = ['_KELQ12IYPV34WFR56ATX78BN90HZGOCMSDJU',
                   'EFGJ54VIP321LDHQ678_O9X0CSKRNUTZBMAYW']
      self.rt_5 = ['UC12NQRF36745OZW89SH0ADVEXLBPIJ_TKMGY',
                   'RTNHPZBFWOLDCGQVJK0Y7M129A86E5X34IUS_'] 
      self.plug = { l:l  for l in 'ABCDEFGHIJKLMNOQRSPTUVWXYZ1234567890_' }
      self.rotors = [self.rt_1, self.rt_2, self.rt_3, self.rt_4, self.rt_5]
      self.rotor_config = {}
      for idx, rotor in enumerate(rotor_choices):
        self.rotor_config[idx + 1] = self.rotors[rotor]
        
      for idx, setting in enumerate(rotor_settings):
        self.rotate(self.rotor_config[idx +1], setting)
      idx = 0
      for _ in range(len(plug_board) // 2 ):
        letter_swap1 = plug_board[idx]
        letter_swap2 = plug_board[idx + 1]
        self.plug[letter_swap1] = letter_swap2
        self.plug[letter_swap2] = letter_swap1
        idx += 2



    

      



  def rotate(self,rotor : list , rotation : int):
    
       for _ in range(rotation):
         letr = rotor[1][0]
         rotor[1] = rotor[1].replace(letr, "")
         rotor[1]  += letr
     
  def enigma(self, word :str):
      r1, r2 = self.rotor_settings[0:2]
      rotor_1, rotor_2, rotor_3 = [self.rotor_config[1], self.rotor_config[2], self.rotor_config[3] ]
      
      reflector = ['ABCDEFGHIJKLMNOPQRSTUVWXYZ_1234567890',
                   '0987654321_ZYXWVUTSRQPONMLKJIHGFEDCBA']   
      new_word = ""
      
      for letter in word:
        letter = self.plug[letter]

        first_idx      = rotor_1[1].find(letter)
        second_letter  = rotor_2[0][first_idx]
        second_idx     = rotor_2[1].find(second_letter)
        third_letter   = rotor_3[0][second_idx]
        third_idx      = rotor_3[1].find(third_letter)
        reflector_letter  = reflector[1][third_idx]
        reflector_idx     = reflector[0].find(reflector_letter)
        third_letter      = rotor_3[1][reflector_idx]
        third_idx         = rotor_3[0].find(third_letter)
        second_letter     = rotor_2[1][third_idx]
        second_idx        = rotor_2[0].find(second_letter)
        output            = rotor_1[1][second_idx]
        output            = self.plug[output]
        new_word += output
        self.rotate(rotor_1, 1)
        length_of_r = len(rotor_2[1])
        r1+=1
        if r1 > length_of_r:
          r1 = 0
          self.rotate(rotor_2, 1)

          r2+=1
        if r2 > length_of_r:
          r2 = 0
        
          self.rotate(rotor_3, 1)
      
      return new_word


@app.post('/')
def encrypt(rotors ,x,y,z,  word: str, plug_board: str ):
  rotors = [int(r) for r in rotors]
  settings = [int(s) for s in [x,y,z]]
  eni = EnigmaMachine(rotors, settings, plug_board)
  return {'token' : eni.enigma(word.upper()), 'settings': [rotors,settings] }

if __name__ == '__main__':
  uvicorn.run('eni:app', host='127.0.0.1', port=5000, reload=True)