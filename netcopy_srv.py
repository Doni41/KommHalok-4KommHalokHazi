import sys
import socket
import struct
import time
import hashlib

class NetcopyServer:
    def __init__(self, srv_ip, srv_port, chsum_srv_ip, chsum_srv_port, file_id, file_path):
        self.srv_ip = srv_ip
        self.srv_port = srv_port
        self.chsum_srv_ip = chsum_srv_ip
        self.chsum_srv_port = chsum_srv_port
        self.file_id = file_id
        self.file_path = file_path

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.initVariables()


    def startNetcopyServer(self):
        self.sock.bind((self.srv_ip, self.srv_port))
        self.sock.listen(1)
        self.conn, self.addr = self.sock.accept()

        self.netcopyServerLogic()

        self.sock.close()

    def netcopyServerLogic(self):
        print('Valaki csatlakozott,: ', self.addr)

        self.readFromClient()
        self.writeToFile()
        # self.createChecksum()
        # self.communicateWithChecksum()
    
    def readFromClient(self):
        while True:
            msg = self.conn.recv(1024)
            print(msg)
            self.file_lines.append(msg)
            if not msg:
                break
            # self.lines_as_string += msg

        self.lines_as_string = b"".join([line for line in self.file_lines])

        print('File lines: ', self.file_lines)
        print('Lines as string: ', self.lines_as_string)

        self.conn.close()
    
    def writeToFile(self):
        with open (self.file_path, "wb") as f:
            f.write(self.lines_as_string)
            # for line in self.file_lines:
            #     f.writelines(line)
    
    def communicateWithChecksum(self):
        # KI|< fajl azonosito >
        msg = 'KI|{}'.format(self.file_id)
        self.sock.connect((self.chsum_srv_ip, self.chsum_srv_port))
        self.sock.send(msg.encode())
        answer = self.sock.recv(1024).decode()
        parsed_answ = answer.split('|')
        if answer == '0|' or parsed_answ[1] != self.m.hexdigest():
            print('CSUM CORRUPTED')
        else:
            print('CSUM OK')
    
    def createChecksum(self):
        self.m = hashlib.md5(self.file_lines)
        print('MD5', self.m)

    def readAsString(self):
        while True:
            msg = self.conn.recv(1024)
            print(msg)
            self.file_lines += msg
            if msg.decode() == '':
                break

            print('File lines: ', self.file_lines)

        self.conn.close()

    def readAsOneString(self):
        while True:
            msg = self.conn.recv(1024)
            print(msg)
            self.file_lines += msg
            if msg.decode() == '':
                break

            print('File lines: ', self.file_lines)

        self.conn.close()


    def initVariables(self):
        self.data = []
        self.client_addr = []
        self.packer = ''

        self.conn = ''
        self.addr = ''

        self.file_lines = []
        self.lines_as_string = ''
        self.m = ''
    
netcopy_server = NetcopyServer(sys.argv[1], int(sys.argv[2]), sys.argv[3], int(sys.argv[4]), int(sys.argv[5]), sys.argv[6])
netcopy_server.startNetcopyServer()