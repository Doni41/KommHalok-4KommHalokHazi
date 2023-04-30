import sys
import socket
import select
import struct
import time

class ChecksumServer:
    # init function
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

        self.initSocket()
        self.initVariables()

    def startChecksumServer(self):        
        self.checksumLogic()
        self.createNewChecksum()
    
    def checksumLogic(self):
        while True:
            self.timeout = 1
            try:
                readables, _, _ = select.select(self.inputs, [], [], self.timeout)
                # if not readables:
                    # break
                for s in readables:
                    if s is self.proxy:
                        # print('kliens vagy szerver csatalkozik')
                        client, client_addr = s.accept()
                        self.inputs.append(client)
                    else:
                        data = s.recv(1024)
                        if not data:
                            self.inputs.remove(s)
                            s.close()
                        else:
                            msg = data.decode().split('|')
                            # print(msg)
                            if msg[0] == 'BE':
                                self.readFromClient(s, msg)
                            elif msg[0] == 'KI':
                                self.readFromServer(s, msg)
                                    

            except KeyboardInterrupt:
                for s in self.inputs:
                    s.close()
                # print("Checksum closing")
                break
    
    def readFromClient(self, s, msg):
        self.createNewChecksum(msg[1], int(msg[2]), 32, msg[4])
        s.send('OK'.encode())

    def readFromServer(self, s, msg):
        data_to_send = self.checksums[msg[1]]
        if time.time() - data_to_send['start_time'] > 60:
            self.checksums.remove(msg[1])
            msg = '0|'
            s.send(msg.encode())
        else:
            msg = '{}|{}'.format(data_to_send['byte_length'], data_to_send['checksum'])
            s.send(msg.encode())
    
    def initVariables(self):
        self.inputs = [self.proxy]
        self.timeout = 1.0
        self.select = ()

        self.checksums = {}

        # fajl id - checksum hossz - checksum - larajat (mp-ben)

    def initSocket(self):
        self.proxy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.proxy.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
        self.proxy_addr = (self.ip, self.port)
        self.proxy.bind(self.proxy_addr)
        self.inputs = [self.proxy]
        self.proxy.listen(10)



    def createNewChecksum(self, file_id, time_limit, byte_length, checksum):
        self.checksums[file_id] = {'time_limit': time_limit, 'byte_length': byte_length, 'checksum': checksum, 'start_time': time.time()}
        # print('created: ', self.checksums)


checksum_server = ChecksumServer(sys.argv[1], int(sys.argv[2]))
checksum_server.startChecksumServer()