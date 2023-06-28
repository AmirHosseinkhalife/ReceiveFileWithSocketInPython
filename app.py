import socket
import os

# ایجاد سوکت    
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# تعریف آی پی و پورت سوکت
serverSocket.bind(("localhost", 8888))

# تعیین تعداد اتصال در لحظه
serverSocket.listen(1)

while True:
    # در انتظار برقراری ارتباط
    print("Waiting for a connection...")
    connection, clientAddress = serverSocket.accept()

    try:
        # ارتباط برقرار شده و اطلاعات برقرار کننده در دسترس است
        print("Connection from", clientAddress)

        # دریافت نام فایل
        fileNameLength = int.from_bytes(connection.recv(4), byteorder='big')
        fileName = connection.recv(fileNameLength).decode('utf-8')

        # ایجاد فایل برای تزریق بایت ها
        file = open(fileName, "wb")

        i = 1
        # دریافت فایل در پکت های 1 مگابایتی
        data = connection.recv(1048576)
        while data:
            file.write(data)
            print('received Part '+str(i))
            i = i+1
            data = connection.recv(1048576)

        # پایان دریافت فایل - بستن کانکشن و فایل
        file.close()
        connection.close()
        print("File received and connection closed.")
    except:
        # بستن کانکشن در صورت بروز خطا
        connection.close()
        print("Error receiving file.")