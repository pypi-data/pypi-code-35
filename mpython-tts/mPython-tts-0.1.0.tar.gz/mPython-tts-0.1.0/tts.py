"""
MIT License

Copyright (c) 2019 tangliufeng@labplus

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import codec
import uhashlib,ntptime,base64,ubinascii,time

class TTS(object):
    """
    xfyun Text To Speech (TTS),More about TTS API info browe  https://www.xfyun.cn/
    """
    def __init__(self,appid,api_key,voice_name="aisxping",engine_type="intp65"):

        while True:
            try:
                ntptime.settime()
            except OSError :
                pass
            else:
                break
        self.APPID = appid
        self.API_KEY = api_key
        self.voice_name = voice_name
        self.engine_type = engine_type

    def _get_header(self): 
        
            AUE="lame"
            curTime = str(int(time.time()+946656001))
            param = "{\"aue\":\""+AUE+"\",\"auf\":\"audio/L16;rate=16000\",\"voice_name\":\""+self.voice_name+"\",\"volume\":\"100\",\"engine_type\":\""+self.engine_type+"\"}"
            # print("param:{}".format(param))
            
            paramBase64 = str(base64.b64encode(param.encode('utf-8')), 'utf-8')
            # print("x_param:{}".format(paramBase64))
            
            m2 = uhashlib.md5()
            m2.update((self.API_KEY + curTime + paramBase64).encode('utf-8'))
            
            checkSum = ubinascii.hexlify(m2.digest()).decode()
            # print('checkSum:{}'.format(checkSum))
            
            header ={
                    'X-CurTime':curTime,
                    'X-Param':paramBase64,
                    'X-Appid':self.APPID,
                    'X-CheckSum':checkSum,
                    'X-Real-Ip':'127.0.0.1',
                    'Content-Type':'application/x-www-form-urlencoded; charset=utf-8',
            }
            return header


     
    def translate(self,text):
        """TTS translate text"""
        header=self._get_header()
        codec.web_tts(header, text)
