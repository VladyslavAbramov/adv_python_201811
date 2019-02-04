from tkinter import *
from socket import *
from threading import Thread


def server(host, port):
    with socket(AF_INET, SOCK_STREAM) as sock:
        sock.bind((host, port)) # '' - ANY, '<broadcast>'
        sock.listen()
        print('Start listening on', host, port)

        def tk_build():
            root = Tk()
            label_text = StringVar()

            def on_click(evt):
                message = label_text.get()
                text_area.insert(END, message + '\n')
                label_text.set('')
                text_area.see(END)
                client.sendall(bytes(message, 'utf-8'))

            lbl = LabelFrame(root, text='Lets start')
            lbl.pack(padx=15, pady=15)

            global text_area
            text_area = Text(lbl, height=5, width=30)
            text_area.pack(fill=X)

            label = Entry(lbl, width=35, textvariable=label_text)
            label.pack(side=LEFT, pady=5)
            label.bind('<Return>', on_click)

            button = Button(lbl, text='Send', height=2)
            button.pack(side=RIGHT, pady=5)
            button.bind('<Button-1>', on_click)

            print('tk build')
            root.mainloop()

        Thread(target=tk_build).start()

        while True:
            client, addr = sock.accept()  # blocking
            print('Incoming connection from', addr)
            Thread(target=handler, args=[client]).start()


def handler(client):
    with client:
        while True:
            data = client.recv(1024)  # blocking
            if not data:
                break
            data = data.decode()
            print(data)
            text_area.insert(END, data + '\n')
            text_area.see(END)


def client(HOST, PORT):
    with socket(AF_INET, SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))

        def tk_build(sock):
            root = Tk()
            label_text = StringVar()

            def on_click(evt):
                message = label_text.get()
                text_area.insert(END, message + '\n')
                label_text.set('')
                text_area.see(END)
                sock.sendall(bytes(message, 'utf-8'))

            lbl = LabelFrame(root, text='Lets start')
            lbl.pack(padx=15, pady=15)

            global text_area
            text_area = Text(lbl, height=5, width=30)
            text_area.pack(fill=X)

            label = Entry(lbl, width=35, textvariable=label_text)
            label.pack(side=LEFT, pady=5)
            label.bind('<Return>', on_click)

            button = Button(lbl, text='Send', height=2)
            button.pack(side=RIGHT, pady=5)
            button.bind('<Button-1>', on_click)

            print('tk build')
            root.mainloop()
        Thread(target=tk_build, args=[sock]).start()

        while True:
            # case with Thread
            # Thread(target=handler_listen, args=[sock]).start()

            # case without Thread
            data = sock.recv(1024)
            print('Client: received ' + data.decode())
            data = data.decode()
            text_area.insert(END, data + '\n')
            text_area.see(END)


def handler_listen(sock):
    with sock:
        while True:
            data = sock.recv(1024)  # blocking
            if not data:
                break
            data = data.decode()
            print(data)
            text_area.insert(END, data + '\n')
            text_area.see(END)


if __name__ == '__main__':
    import sys
    args = sys.argv[1:]
    method, host, port, *_ = args
    if method == '--listen':
        server(host, int(port))
    elif method == '--connect':
        client(host, int(port))

