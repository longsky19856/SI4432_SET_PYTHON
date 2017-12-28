# -*- coding: utf-8 -*-
import threading,time
import serial
import string
import re
import crc16_setup
import crc16
class com:
    def __init__(self,Port,rate):
        self.my_serial = serial.Serial()
        self.my_serial.port = Port
        self.my_serial.baudrate = rate
        self.my_serial.timeout = 1
        self.alive = False
        self.waitEnd = None
        self.thread_read = None
    def waiting(self):
        # 等待event停止标志
        if not self.waitEnd is None:
            self.waitEnd.wait()
    def start(self):
        self.my_serial.open()
        if self.my_serial.isOpen():
            #self.waitEnd = threading.Event()
            self.alive = True
            #self.thread_read = threading.Thread(target=self.Reader)
            #self.thread_read.setDaemon(True)
            #self.thread_read.start()
            return True
        else:
            return False
    def Reader(self):

            try:
                n = self.my_serial.inWaiting()
                data = ''
                if n:
                    #data = self.my_serial.read(n).decode('utf-8')
                    data = self.my_serial.read(n)
                    #print ('recv' + ' ' + time.strftime("%Y-%m-%d %X") + ' ' + data.strip())
                    #print ( data.strip())
                    return data

            except Exception as ex:
                print (ex)



    def Sender(self,data):
        #print ('sent' + ' ' + time.strftime("%Y-%m-%d %X"))
        self.my_serial.write(data)

    def stop(self):
        self.alive = False
        # self.thread_read.join()
        # self.thread_send.join()
        if self.my_serial.isOpen():
            self.my_serial.close()
def crc(data):
    tmp='0001'
    return tmp
class message:
    def __init__(self):
        self.start_byte= '5FAF'
        self.begin=''
        self.num = '01'
        self.position=''
        self.add_hui=''
        self.add_cai=''
        self.cmd=''
        self.data=''
        self.crc=''
        self.mess_setid=''
        self.mess_resetpara=''
        self.mess_calibration_current=''
        self.mess_read_current=''
        self.mess_setroad=''
    def set_id(self):
        self.begin='00'
        self.position='01'
        self.cmd='20'
        self.mess_setid=self.start_byte+self.begin+self.num+self.position+self.add_hui+self.add_cai+self.cmd+self.data
        crc16_calc = crc16_setup.crc16()
        self.crc=crc16_calc.createcrc_hex(self.mess_setid)
        self.mess_setid=self.mess_setid+self.crc
    def reset_para(self):
        self.begin = '00'
        self.position = '01'
        self.cmd = '24'
        self.mess_resetpara = self.start_byte + self.begin + self.num + self.position + self.add_hui + self.add_cai + self.cmd
        crc16_calc = crc16_setup.crc16()
        self.crc = crc16_calc.createcrc_hex(self.mess_resetpara)
        self.mess_resetpara = self.mess_resetpara + self.crc
    def calibration_current(self):
        self.begin = '00'
        self.position = '01'
        self.cmd = '23'
        tmp=hex(int(float(self.data)*10))
        self.data=(6-len(tmp))*'0'+tmp[2:]
        self.mess_calibration_current = self.start_byte + self.begin + self.num + self.position + self.add_hui + self.add_cai + self.cmd+self.data
        crc16_calc = crc16_setup.crc16()
        self.crc = crc16_calc.createcrc_hex(self.mess_calibration_current)
        self.mess_calibration_current = self.mess_calibration_current + self.crc
    def read_current(self):
        self.begin='00'
        self.position='01'
        self.cmd='07'
        self.mess_read_current=self.start_byte + self.begin + self.num + self.position + self.add_hui + self.add_cai + self.cmd
        crc16_calc = crc16_setup.crc16()
        self.crc = crc16_calc.createcrc_hex(self.mess_read_current)
        self.mess_read_current=self.mess_read_current+self.crc
    def set_road(self):
        self.begin = '00'
        self.position = '01'
        self.cmd = '02'
        #print self.add_cai[7:]
        #print str((int(self.add_cai[7:])-1)*2+1)

        self.data='0'+str((int(self.add_cai[7:])-1)*2+1)
        self.mess_setroad = self.start_byte + self.begin + self.num + self.position + self.add_hui + self.add_cai + self.cmd+self.data
        crc16_calc = crc16_setup.crc16()
        self.crc=crc16_calc.createcrc_hex(self.mess_setroad)
        self.mess_setroad=self.mess_setroad+self.crc








