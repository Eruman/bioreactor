#Тестовая программа для насоса без индикатора
#

import serial                              # pip3 install pyserial
from serial.tools import list_ports

import time

def init_ports():
    mon_ = 0
    available_ports = list_ports.comports()
    print(f'Доступные порты: {[x.device for x in available_ports]}')
    print()
    
    #Получаем список портов
    ports = list(list_ports.comports())
        
    #Получаем список портов и ищем нужное устройство
    for p in ports:
        if str(p).split(' - ')[1][:16] == 'USB-SERIAL CH340':
            print(str(p).split(' - ')[0], ' имеется!')
            name2 = str(p).split(' - ')[0]
            #Подключаемся к нужному устройству
            mon_ = serial.Serial(
                port=name2, baudrate=115200, bytesize=8, timeout=3, stopbits=serial.STOPBITS_ONE
                )  # open serial port
            time.sleep(1)
            print("Порт открыт.")
            
    print()
    return(mon_)

def close_port():
    #Отключаемся от устройства
    mon.close()
    print("Порт закрыт.")

if __name__ == "__main__":
    #global outdata
    mon = 0

    print("Стартую!")

    mon = init_ports()
    
    if mon == 0:
        print("Устройство не обнаружено.")
        exit()

    print('\nЖмите ENTER для запуска устройства.', end="")
    input()
    #Формат команды: rotate( угол, микропауза )
    #угол может быть нулевым, если нужно изменить только скорость вращения
    #mon.write(b'rotate(0, 2500)\n')

    #Активируем приводы
    for i in range(5):
        mon.write(b'rotate(180, 2000)\n')  # Отправляем команду на левое вращение насоса на 180 градусов с микропаузами 2 мс
        time.sleep(1)                      # Пауза длительностью 1 секунда
        mon.write(b'rotate(-180, 2000)\n') # Отправляем команду на правое вращение насоса на 180 градусов с микропаузами 2 мс
        time.sleep(1)                      # Пауза длительностью 1 секунда


    for i in range(5):
        mon.write(b'rotate(90, 1500)\n') # Отправляем команду на левое вращение насоса на 180 градусов с микропаузами 2000
        time.sleep(1)
        mon.write(b'rotate(-90, 3500)\n') # Отправляем команду на правое вращение насоса на 180 градусов со скоростью 2000
        time.sleep(1)
    
    for i in range(36):
        command = f'rotate({i*10}) \n'   # Отправляем команду на вращение насоса на i*10 градусов с предыдущей скоростью
        mon.write(command.encode())
        time.sleep(.2)

    #Отключаемся от устройства
    close_port()