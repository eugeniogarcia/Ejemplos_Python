from multiprocessing import Process, Event
from multiprocessing import synchronize  
import itertools
import time
import sys

def spin(msg: str, done: synchronize.Event) -> None:  
    write, flush = sys.stdout.write, sys.stdout.flush
    for char in itertools.cycle('|/-\\'):  
        status = char + ' ' + msg
        write(status)
        flush()
        #Mueve el cursor para atras
        write('\x08' * len(status))
        #Bloquea la ejecución, de modo que el GIL se libera. Si pasados .1 segundos no se ha seteado done a true, devolvera false
        if done.wait(.1): 
            break
    write(' ' * len(status) + '\x08' * len(status))  


def slow_function():  
    # pretend waiting a long time for I/O
    time.sleep(3)
    return 42


def supervisor():
    #define un evento para comunicarnos con el thread
    done = Event()
    #crea un thread con el callable
    spinner = Process(target=spin,args=('thinking!', done))
    print('spinner object:', spinner)

    #arranca el proceso
    spinner.start()

    result = slow_function()  

    #Notifica al proceso
    done.set()

    #Esperamos a que termine el proceso
    spinner.join()

    return result


def main():
    result = supervisor()
    print('Answer:', result)


if __name__ == '__main__':
    main()