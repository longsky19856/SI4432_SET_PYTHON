# -*- coding: utf-8 -*-
from PyQt4.QtGui import *

from PyQt4.QtCore import *
from PyQt4 import QtCore, QtGui

import sys
import os
import serial
import serial.tools.list_ports
import  re

import com_init
import interface
import time
import binascii

try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QApplication.UnicodeUTF8


    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)


class TestDlg(QDialog, interface.Ui_dialog):
    message=com_init.message()
    def __init__(self, parent=None):
        super(TestDlg, self).__init__(parent)

        self.setupUi(self)


def opencom(dialog_c):
    tmp = dialog_c.pushButton.text()
    if tmp == "open":  # opne com
        #
        com_num = str(dialog_c.comboBox.currentText())
        com_baud = int(dialog_c.comboBox_2.currentText())
        print  com_num, com_baud
        # ser=com(com_num,com_baud)
        global ser
        ser = com_init.com(com_num, com_baud)
        try:
            ser.start()
        except :
            dialog_c.textEdit.append("can not open com")
        else:
            dialog_c.textEdit.append("open com success")
            dialog_c.pushButton.setText(_translate("Dialog", "close", None))
            dialog_c.pushButton_2.setEnabled(True)
            dialog_c.pushButton_3.setEnabled(True)
            dialog_c.pushButton_4.setEnabled(True)
            dialog_c.pushButton_5.setEnabled(True)
            dialog_c.pushButton_6.setEnabled(True)
            dialog_c.pushButton_7.setEnabled(True)
            dialog_c.pushButton_8.setEnabled(True)
            dialog_c.pushButton_9.setEnabled(True)
            dialog_c.pushButton_10.setEnabled(True)
            dialog_c.comboBox.setEnabled(False)
            dialog_c.comboBox_2.setEnabled(False)
    if tmp == "close":
        dialog_c.pushButton.setText(_translate("Dialog", "open", None))
        dialog_c.pushButton_2.setEnabled(False)
        dialog_c.pushButton_3.setEnabled(False)
        dialog_c.pushButton_4.setEnabled(False)
        dialog_c.pushButton_5.setEnabled(False)
        dialog_c.pushButton_6.setEnabled(False)
        dialog_c.pushButton_7.setEnabled(False)
        dialog_c.pushButton_8.setEnabled(False)
        dialog_c.pushButton_9.setEnabled(False)
        dialog_c.pushButton_10.setEnabled(False)
        dialog_c.comboBox.setEnabled(True)
        dialog_c.comboBox_2.setEnabled(True)
        dialog_c.textEdit.clear()
        ser.stop()


def setid(dialog_c):
    dialog_c.message.add_cai=str(dialog_c.lineEdit_2.text())
    dialog_c.message.add_hui=str(dialog_c.lineEdit.text())
    dialog_c.message.data=str(dialog_c.lineEdit_5.text())
    if len(dialog_c.message.add_cai)!=8 or len(dialog_c.message.add_hui)!=8 or len(dialog_c.message.data)!=8:
        dialog_c.textEdit.append('wrong input length')
    elif re.search(r'[^A-Fa-f0-9]',dialog_c.message.add_cai) or re.search(r'[^A-Fa-f0-9]',dialog_c.message.add_hui) or \
            re.search(r'[^A-Fa-f0-9]',dialog_c.message.data):
        dialog_c.textEdit.append('wrong input range ')
    else:
        dialog_c.message.set_id()
        dialog_c.textEdit.append('['+time.strftime("%X")+']'+"send:" + dialog_c.message.mess_setid)
        ser.Sender(dialog_c.message.mess_setid.decode("hex"))
        #read com data
        ser.my_serial.flushInput()
        time.sleep(3)
        tmp=ser.Reader()
        if tmp==None:
            dialog_c.textEdit.append('['+time.strftime("%X")+']'+"read:")
            dialog_c.textEdit.append('[' + time.strftime("%X") + ']' + "read:" + "set id no ok ,retry")
        else:
            dialog_c.textEdit.append('['+time.strftime("%X")+']'+"read:" + binascii.b2a_hex(tmp))
            tmp_hex = binascii.b2a_hex(tmp).upper()
            print tmp_hex
            tmp_in='5FAF010100'+dialog_c.message.add_hui+dialog_c.message.add_cai+'20'
            if re.search(tmp_in, tmp_hex)==None:
                #print  "set id no ok ,retry"
                dialog_c.textEdit.append('[' + time.strftime("%X") + ']' + "read:" + "set id no ok ,retry")
            else:
                dialog_c.textEdit.append('[' + time.strftime("%X") + ']' + "read:" + "set id ok")
                dialog_c.lineEdit_2.setText(_translate("dialog", str(dialog_c.lineEdit_5.text()), None))






def readpara(dialog_c):
    dialog_c.textEdit.append("read: 11 22 ff")
    tmp = dialog_c.comboBox_2.currentText()
    print  dialog_c.comboBox_2.currentIndex()
    dialog_c.textEdit.append(tmp)
def resetpara(dialog_c):
    dialog_c.message.add_cai = str(dialog_c.lineEdit_2.text())
    dialog_c.message.add_hui = str(dialog_c.lineEdit.text())
    if len(dialog_c.message.add_cai) != 8 or len(dialog_c.message.add_hui) != 8:
        dialog_c.textEdit.append('wrong input length')
    elif re.search(r'[^A-Fa-f0-9]', dialog_c.message.add_cai) or re.search(r'[^A-Fa-f0-9]',dialog_c.message.add_hui):
        dialog_c.textEdit.append('wrong input range ')
    else:
        dialog_c.message.reset_para()
        dialog_c.textEdit.append('[' + time.strftime("%X") + ']' + "send:" + dialog_c.message.mess_resetpara)
        ser.Sender(dialog_c.message.mess_resetpara.decode("hex"))
        # read com data
        ser.my_serial.flushInput()
        time.sleep(2)
        tmp = ser.Reader()
        if tmp == None:
            dialog_c.textEdit.append('[' + time.strftime("%X") + ']' + "read:")
        else:
            dialog_c.textEdit.append('[' + time.strftime("%X") + ']' + "read:" + binascii.b2a_hex(tmp))
def calibration_current(dialog_c):
    dialog_c.message.add_cai = str(dialog_c.lineEdit_2.text())
    dialog_c.message.add_hui = str(dialog_c.lineEdit.text())
    dialog_c.message.data = str(dialog_c.lineEdit_3.text())
    if len(dialog_c.message.add_cai) != 8 or len(dialog_c.message.add_hui) != 8:
        dialog_c.textEdit.append('wrong input length')
    elif re.search(r'[^A-Fa-f0-9]', dialog_c.message.add_cai)or re.search(r'[^A-Fa-f0-9]',dialog_c.message.add_hui) or \
            re.search(r'[^0-9]+(.[^0-9]{1})', dialog_c.message.data):
        dialog_c.textEdit.append('wrong input range ')
    else:
        dialog_c.message.calibration_current()
        dialog_c.textEdit.append('[' + time.strftime("%X") + ']' + "send:" + dialog_c.message.mess_calibration_current)
        ser.Sender(dialog_c.message.mess_calibration_current.decode("hex"))
        # read com data
        ser.my_serial.flushInput()
        time.sleep(3)
        tmp = ser.Reader()
        if tmp == None:
            dialog_c.textEdit.append('[' + time.strftime("%X") + ']' + "read:")
        else:
            dialog_c.textEdit.append('[' + time.strftime("%X") + ']' + "read:" + binascii.b2a_hex(tmp))

def read_current(dialog_c):
    dialog_c.message.add_cai = str(dialog_c.lineEdit_2.text())
    dialog_c.message.add_hui = str(dialog_c.lineEdit.text())
    dialog_c.message.read_current()
    dialog_c.textEdit.append('[' + time.strftime("%X") + ']' + "send:" + dialog_c.message.mess_read_current)
    ser.Sender(dialog_c.message.mess_read_current.decode("hex"))
    ser.my_serial.flushInput()
    time.sleep(3)
    tmp = ser.Reader()
    if tmp == None:
        dialog_c.textEdit.append('[' + time.strftime("%X") + ']' + "read:")
    else:
        dialog_c.textEdit.append('[' + time.strftime("%X") + ']' + "read:" + binascii.b2a_hex(tmp))
        #get data
        tmp_hex=binascii.b2a_hex(tmp).upper()
        #print tmp_hex
        a = int(re.search('5FAF',tmp_hex).span()[0])
        #print tmp_hex[a+28:a+32]
        #print tmp_hex[a + 32:a + 36]
        #print int(tmp_hex[a + 36:a + 40],16)
        #dialog_c.lineEdit_6.setText(_translate("Dialog", str(int(tmp_hex[a + 28:a + 32], 16)/10), None))
        dialog_c.lineEdit_6.setText(_translate("Dialog", str(float(int(tmp_hex[a + 28:a + 32], 16)) / 10), None))
        dialog_c.lineEdit_7.setText(_translate("Dialog", str(int(tmp_hex[a + 32:a + 36], 16)), None))
        dialog_c.lineEdit_8.setText(_translate("Dialog", str(int(tmp_hex[a + 36:a + 40],16)) , None))
        dialog_c.lineEdit_8.setText(_translate("Dialog", str(int(tmp_hex[a + 36:a + 40], 16)), None))
        dialog_c.lineEdit_10.setText(_translate("Dialog", str(int(tmp_hex[a + 40:a + 44], 16)), None))

def clear_textEdit(dialog_c):
    dialog_c.textEdit.clear()
def setroad(dialog_c):
    dialog_c.message.add_cai = str(dialog_c.lineEdit_2.text())
    dialog_c.message.add_hui = str(dialog_c.lineEdit.text())
    dialog_c.message.set_road()
    dialog_c.textEdit.append('[' + time.strftime("%X") + ']' + "send:" + dialog_c.message.mess_setroad)
    ser.Sender(dialog_c.message.mess_setroad.decode("hex"))
    ser.my_serial.flushInput()
    time.sleep(3)
    tmp = ser.Reader()
    if tmp == None:
        #dialog_c.textEdit.append('[' + time.strftime("%X") + ']' + "read:")
        dialog_c.textEdit.append('[' + time.strftime("%X") + ']' + "read:" + "set road no ok ,retry")
    else:
        dialog_c.textEdit.append('[' + time.strftime("%X") + ']' + "read:" + binascii.b2a_hex(tmp))
        tmp_hex = binascii.b2a_hex(tmp).upper()
        print tmp_hex
        tmp_in = '5FAF010100' + dialog_c.message.add_hui + dialog_c.message.add_cai + '02'
        if re.search(tmp_in, tmp_hex) == None:
            # print  "set id no ok ,retry"
            dialog_c.textEdit.append('[' + time.strftime("%X") + ']' + "read:" + "set road no ok ,retry")
        else:
            dialog_c.textEdit.append('[' + time.strftime("%X") + ']' + "read:" + "set road ok")
def next_board(dialog_c):


    dialog_c.message.add_cai = str(dialog_c.lineEdit_2.text())
    dialog_c.message.add_hui = str(dialog_c.lineEdit.text())
    if  dialog_c.message.add_cai[4:]=='0003':
        dialog_c.message.add_hui=str(int(dialog_c.message.add_hui[0:4])+1)+'0000'
        dialog_c.message.add_cai=dialog_c.message.add_hui[0:4]+'0001'
    else:
        dialog_c.message.add_cai = dialog_c.message.add_cai[0:7]+str(int(dialog_c.message.add_cai[7:])+1)

    dialog_c.lineEdit.setText(_translate("dialog", dialog_c.message.add_hui, None))
    dialog_c.lineEdit_5.setText(_translate("dialog", dialog_c.message.add_cai, None))
    dialog_c.lineEdit_2.setText(_translate("dialog", "01010101", None))
def setsn(dialog_c):
    dialog_c.message.add_cai = str(dialog_c.lineEdit_2.text())
    tmp_time=time.strftime('%Y%m%d', time.localtime(time.time()))
    tmp_num='ABC'
    tmp_serial=int(dialog_c.message.add_cai[7:])
    if tmp_serial>3:
        dialog_c.textEdit.append('[' + time.strftime("%X") + ']' + _translate("dialog", "ID错误", None))
    else:
        tmp_sn = tmp_time + dialog_c.message.add_cai + tmp_num[tmp_serial - 1:tmp_serial]
        dialog_c.lineEdit_9.setText(_translate("dialog", tmp_sn, None))
        dialog_c.textEdit.append('[' + time.strftime("%X") + ']' +_translate("dialog", "生成SN码成功", None))






















def init_interface(dialog_c):
    plist = list(serial.tools.list_ports.comports())
    if len(plist) <= 0:
        print("没有发现端口!")
    else:
        i = 0
        while i < len(plist):
            #print  str(plist[i][0])
            dialog_c.comboBox.addItem(_fromUtf8(""))
            dialog_c.comboBox.setItemText(i, _translate("Dialog", str(plist[i][0]), None))
            i = i + 1


    dialog_c.pushButton.clicked.connect(lambda: opencom(dialog_c))
    dialog_c.pushButton_2.clicked.connect(lambda: readpara(dialog_c))
    dialog_c.pushButton_3.clicked.connect(lambda: setid(dialog_c))
    dialog_c.pushButton_4.clicked.connect(lambda: resetpara(dialog_c))
    dialog_c.pushButton_5.clicked.connect(lambda: calibration_current(dialog_c))
    dialog_c.pushButton_6.clicked.connect(lambda: read_current(dialog_c))
    dialog_c.pushButton_7.clicked.connect(lambda: clear_textEdit(dialog_c))
    dialog_c.pushButton_8.clicked.connect(lambda: setroad(dialog_c))
    dialog_c.pushButton_9.clicked.connect(lambda: next_board(dialog_c))
    dialog_c.pushButton_10.clicked.connect(lambda: setsn(dialog_c))




app = QApplication(sys.argv)

dialog = TestDlg()
init_interface(dialog)


dialog.show()

app.exec_()