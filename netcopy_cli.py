import sys
import socket
import struct
import time
import hashlib

class NetcopyClient:
    def __init__(self, srv_ip, srv_port, chsum_srv_ip, chsum_srv_port, file_id, file_path):
        self.srv_ip = srv_ip
        self.srv_port = srv_port
        self.chsum_srv_ip = chsum_srv_ip
        self.chsum_srv_port = chsum_srv_port
        self.file_id = file_id
        self.file_path = file_path

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.initVariables()

    def startNetcopyClient(self):
        self.netCopyLogic()        
    
    def netCopyLogic(self):
        self.readBinaryFile()
        self.sendBinaryFiles()
        self.createChecksum()
        # self.communicateWithChecksum()

        self.sock.close()
    
    def readBinaryFile(self):
        with open (self.file_path, "rb") as f:
            # self.lines = f.read()
            self.lines = f.readlines()

        self.lines_as_string = b"".join([line for line in self.lines])


        print('File lines: ', self.lines)
        print('Print as string: ', self.lines_as_string)
        
    def sendBinaryFiles(self):
        self.sock.connect((self.srv_ip, self.srv_port))
        for s in self.lines:
            self.sock.send(s)
            # answer = self.sock.recv(1024)
        self.sock.close()
        # print(answer)

    def communicateWithChecksum(self):
        # BE|< fájl azon. >|< érvényesség másodpercben >|< checksum hossza bájtszámban >|< checksum bájtjai >
        msg = 'Be|{}|{}|{}|{}'.format(self.file_id, self.time_limit, 16, self.m)
        self.sock.connect((self.chsum_srv_ip, self.chsum_srv_port))
        self.sock.send(msg)
        answer = self.sock.recv(1024)
        print(answer.encode())
        
    
    def createChecksum(self):
        # self.m = hashlib.md5(self.lines)
        self.m = hashlib.md5(self.lines_as_string)

        print('MD5: ', self.m)

    def initVariables(self):
        self.packer = struct.Struct('i i 16s i')

        self.lines = []
        self.lines_as_string = ''

        self.m = ''
        self.m2 = ''
        self.time_limit = 60



netcopy_client = NetcopyClient(sys.argv[1], int(sys.argv[2]), sys.argv[3], int(sys.argv[4]), int(sys.argv[5]), sys.argv[6])
netcopy_client.startNetcopyClient()