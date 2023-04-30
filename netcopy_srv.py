import sys
import socket
import struct
import time
import hashlib

class NetcopyServer:
    # init function
    def __init__(self, srv_ip, srv_port, chsum_srv_ip, chsum_srv_port, file_id, file_path):
        self.srv_ip = srv_ip
        self.srv_port = srv_port
        self.chsum_srv_ip = chsum_srv_ip
        self.chsum_srv_port = chsum_srv_port
        self.file_id = file_id
        self.file_path = file_path

        
        self.initSocket()
        self.initVariables()

    # starting the server 
    def startNetcopyServer(self):
        self.sock.bind((self.srv_ip, self.srv_port))
        self.sock.listen(1)
        self.conn, self.addr = self.sock.accept()

        self.netcopyServerLogic()

        self.sock.close()

    # all netcopy server loginc
    def netcopyServerLogic(self):
        # print('Valaki csatlakozott,: ', self.addr)

        self.readFromClient()
        self.writeToFile()
        self.createChecksum()
        self.communicateWithChecksum()
    
    # reading data from client line by line
    def readFromClient(self):
        while True:
            msg = self.conn.recv(1024)
            # print(msg)
            self.file_lines.append(msg)
            if not msg:
                break
            # self.lines_as_string += msg

        self.lines_as_string = b"".join([line for line in self.file_lines])

        # print('File lines: ', self.file_lines)
        # print('Lines as string: ', self.lines_as_string)

        self.conn.close()
    
    # reading data from client
    def readAsString(self):
        while True:
            msg = self.conn.recv(1024)
            # print(msg)
            self.file_lines += msg
            if msg.decode() == '':
                break

            # print('File lines: ', self.file_lines)

        self.conn.close()

    # helper function but not used
    def readAsOneString(self):
        while True:
            msg = self.conn.recv(1024)
            # print(msg)
            self.file_lines += msg
            if msg.decode() == '':
                break

            # print('File lines: ', self.file_lines)

        self.conn.close()

    # writing file 
    def writeToFile(self):
        with open (self.file_path, "wb") as f:
            f.write(self.lines_as_string)
            f.close()

    # createing md5 checksum
    def createChecksum(self):
        self.m = hashlib.md5(self.lines_as_string)
        # print('MD5', self.m)

    # getting data from chekcsum server
    def communicateWithChecksum(self):
        # print('send to checksum server')
        # KI|< fajl azonosito >
        msg = 'KI|{}'.format(self.file_id)
        self.sock2.connect((self.chsum_srv_ip, self.chsum_srv_port))
        self.sock2.send(msg.encode())
        answer = self.sock2.recv(1024).decode()
        # print('answer: ', answer)
        parsed_answ = answer.split('|')
        if answer == '0|' or parsed_answ[1] != self.m.hexdigest():
            print('CSUM CORRUPTED')
        else:
            print('CSUM OK')

    # socket initialization
    def initSocket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # instance variable initialitazion
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