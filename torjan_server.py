import base64
import socket
import threading
import os

def capture_screen(file_path):

    import win32gui
    import win32ui
    import win32con
    import win32api

# 获取桌面
    hdesktop = win32gui.GetDesktopWindow()

# 分辨率适应
    width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
    height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
    left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
    top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)

# 创建设备描述表
    desktop_dc = win32gui.GetWindowDC(hdesktop)
    img_dc = win32ui.CreateDCFromHandle(desktop_dc)

# 创建一个内存设备描述表
    mem_dc = img_dc.CreateCompatibleDC()

# 创建位图对象
    screenshot = win32ui.CreateBitmap()
    screenshot.CreateCompatibleBitmap(img_dc, width, height)
    mem_dc.SelectObject(screenshot)

# 截图至内存设备描述表
    mem_dc.BitBlt((0, 0), (width, height), img_dc, (left, top), win32con.SRCCOPY)

# 将截图保存到文件中
    screenshot.SaveBitmapFile(mem_dc, file_path)

# 内存释放
    mem_dc.DeleteDC()
    win32gui.DeleteObject(screenshot.GetHandle())

def delete(file_path):
    os.system("rm "+ file_path)

file_path = r".\pic.png"
del_path = "pic.png"
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
bind_ip = "127.0.0.1"
bind_port = 9999
address = bind_ip, bind_port
server.bind(address)
server.listen(5)
def client_handler(client):
    request = client.recv(1024)
    if request == "GET_PICTURE":
        print("capturing picture...")

        capture_screen(file_path)
        print("delivering picture...")
        picture = open(file_path,"rb")
        encoded_picture = base64.b64encode(picture.read())
        client.send(encoded_picture)

    else:
        response = "ERROR"
        client.send(response)

while True:
    client, addr = server.accept()
    print "get connection from %s:%d",(addr[0],addr[1])
    client_thread = threading.Thread(target=client_handler,args=(client,))
    client_thread.start()
    client_thread.join()
    delete(del_path)
