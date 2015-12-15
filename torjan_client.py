import time
def picture_handler():
    command = "GET_PICTURE"
    import socket
    pic_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    host_ip = "127.0.0.1"
    host_port = 9999
    address = host_ip, host_port
    # connect the goal
    pic_socket.connect(address)
    # send the command to capture the screen
    pic_socket.send(command)
    # get the response
    response = pic_socket.recv(1024**2*16)
    if response != "ERROR":
        encoded_picture = response
        time_now = time.strftime("%Y-%m-%d-%H-%M-%S")
        pic_to_store = open("screen" + time_now+ ".jpg" ,"wb")
        import base64
        pic_to_store.write(base64.b64decode(encoded_picture))
        pic_to_store.close()
        print "picture get!"
    else:print "Get failed!"

def main():
    import threading
    while True:
        command = raw_input(">torjean>")
        if command == "q":
            break
        threading.Thread(target=picture_handler).start()
main()