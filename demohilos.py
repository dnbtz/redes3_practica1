import threading

def contar():
    contador = 0
    while contador<10000:
        contador+=1
        print('Hilo:',
              threading.current_thread().getName(),
              'con identificador:',
              threading.current_thread().ident,
              'Contador:', contador)

NUM_HILOS = 3

for num_hilo in range(NUM_HILOS):
    hilo = threading.Thread(name='hilo%s' %num_hilo,
                            target=contar)
    hilo.start()