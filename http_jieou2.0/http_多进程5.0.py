import socket
import re
import multiprocessing
from time import  ctime
# import dynamic.httpmodle
import sys
class   WSGIserver():


    def __init__(self,port,app,static):
        self.tcp_service = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_service.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.tcp_service.bind(('', port))
        self.tcp_service.listen(128)
        self.static = static

        self.app = app
    def deal_data(self,client):


            content_data = client.recv(1024).decode()
            list_request = content_data.splitlines()
            head=''
            print(list_request)
            head = re.match(r'[^/]+(/[^ ]*)',list_request[0])




            if head:
                file_path = head.group(1)
                if head.group(1) == "/" :
                     file_path =  r'/index.html'
            if not file_path.endswith('.html'):
                try:
                    f = open(self.static+file_path, 'rb')
                except:
                    response = "HTTP/1.1 404 NOT FOUND\r\n"
                    response += "\r\n"
                    response += "------file not found-----"
                    client.send(response.encode("utf-8"))
                else:
                    text = f.read()
                    f.close()
                    head = 'HTTP/1.1 200 OK\r\n'
                    head+='\r\n'
                    client.send(head.encode('utf-8'))
                    client.send(text)

            else:
               env = dict()
               env['file_path'] = file_path
               comeback_data = self.app(env,self.start_response)
               self.head_respone = 'HTTP/1.1 %s OK\r\n' % head
               for i in self.contont_head:
                   self.head_respone += '%s :%s \r\n' % (i[0], i[1])
               self.head_respone += '\r\n'

               a = self.head_respone + comeback_data

               client.send(a.encode('utf-8'))

            client.close()

    def start_response(self,head,contont_head):

        self.head_respone =head
        self.contont_head = [('severs','1.0')]
        self.contont_head += contont_head

    def run(self):

        while True:
            client, client_adr = self.tcp_service.accept()
            p1 = multiprocessing.Process(target=self.deal_data, args=(client,))
            p1.start()
            client.close()

        tcp_service.close()
           

def main():
    if len(sys.argv) == 3:
        all_name = sys.argv[2]
        w = re.match( r'([^:]+):(.*)' ,all_name)
        modle_name =w.group(1)
        

        with open('./server.conf' ,'r')as f :        
            con_info = eval(f.read())

        sys.path.append(con_info["dynamic"])
        find_name = __import__(modle_name)
        app = getattr(find_name, w.group(2)  )

        port =int(sys.argv[1])
        wgsi = WSGIserver(port,app,con_info['static'])
        wgsi.run()
    else:
        print('输入错误')
        print('请按照“python3 8888  httpmodle:application”')
        return  


if __name__ == '__main__':
    main()

















