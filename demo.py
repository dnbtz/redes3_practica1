from fpdf import FPDF
from createRRD import create
import _thread
import time
import rrdtool
from getSNMP import consultaSNMP
from creaPDF import create_pdf


def haceupdate(nom,comunidad,host,oid,identificador):
    while 1:
        total = int(
            consultaSNMP(comunidad, host, oid))

        valor = "N:" + str(total)+ ':' + str(total)
        #print (valor)
        file = "%s%s.rrd"  % (nom,identificador)
        file2 = "%s%s.xml"  % (nom,identificador)
        rrdtool.update(file, valor)
        rrdtool.dump(file,file2)
        time.sleep(1)
        ret = rrdtool.graph("%s%s.png" % (nom,identificador),
                            "--start", '1582827060',
                            "--end", "1582827360",
                            "--vertical-label=Cantidad",
                            "DEF:inoctets=" + file + ":inoctets:AVERAGE",
                            "DEF:outoctets=" + file + ":outoctets:AVERAGE",
                            "AREA:inoctets#00FF00:%s" % nom,
                            "LINE1:outoctets#0000FF:Tiempo\r")
        time.sleep(10)

    if ret:
        print (rrdtool.error())
        time.sleep(300)


def monitoriza(threadName, ip, ver, comu, puerto):
    create(threadName, '1')
    create(threadName, '2')
    create(threadName, '3')
    create(threadName, '4')
    create(threadName, '5')
    _thread.start_new_thread(haceupdate, (threadName, comu, ip, '1.3.6.1.2.1.2.2.1.11.1', '1',))
    _thread.start_new_thread(haceupdate, (threadName, comu, ip, '1.3.6.1.2.1.4.3.0', '2',))
    _thread.start_new_thread(haceupdate, (threadName, comu, ip, '1.3.6.1.2.1.5.21.0', '3',))
    _thread.start_new_thread(haceupdate, (threadName, comu, ip, '1.3.6.1.2.1.6.10.0', '4',))
    _thread.start_new_thread(haceupdate, (threadName, comu, ip, '1.3.6.1.2.1.7.1.0', '5',))
    #print("%s: %s" % (threadName, time.ctime(time.time())))


def deleteLine():
    nombre = input("Dame el nombre del agente: ")
    fn = 'base.txt'
    f = open(fn)
    output = []
    string = nombre
    for line in f:
        if not line.startswith(string):
            output.append(line)
    f.close()
    f = open(fn, 'w')
    f.writelines(output)
    f.close()
    print("Agente eliminado\n")
    main()


def escribe():
    texto = input("Dame el agente con el formato 'nombre,ip,version,comunidad,puerto': ")
    fn = 'base.txt'
    f = open(fn, "a")
    f.write(texto)
    f.write("\n")
    f.close()
    print("Agente agregado, se inicia la monitorizacion\n")
    nom, ip, ver, comu, puerto = texto.split(',')
    _thread.start_new_thread(monitoriza, (nom, ip, ver, comu, puerto,))
    main()


def muestratodo():
    fh = open('base.txt', "r")
    contenido = fh.read()
    print("\n")
    print("Agentes monitorizando actualmente con estado 'up': ")
    print(cuenta())
    print("\n")
    print(contenido)
    fh.close()
    print("\n")
    main()


def cuenta():
    num_lines = 0
    with  open('base.txt', "r") as f:
        for line in f:
            num_lines += 1
    print(num_lines)


def divide(nombre):
    file = open('base.txt')
    while True:
        line = file.readline()
        if not line:
            break
        if nombre in line:
            return line
            #nom, ip, ver, comu, puerto = line.split(',')
            #print(nom)
            #print(ip)
            #print(ver)
            #print(comu)
            #print(puerto)


def creaPDF():
    agente = input("Dame el nombre del agente: ")
    infobase = divide(agente)
    if infobase is None:
        print("No está registrado ese agente")
        main()
    nom, ip, ver, comu, puerto = infobase.split(',')
    fn = 'base.txt'
    f = open(fn)
    for line in f:
        if line.startswith("windows"):
            logo = "windows_logo.png"
        else:
            logo = "ubuntu-logo.jpg"
    f.close()
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    pdf.set_font("Arial", size=7)
    pdf.image(logo, 10, 8, 33)
    pdf.set_font('Arial', 'B', 15)

    # Add an address
    pdf.cell(100)
    infoagente = str(consultaSNMP(comu, ip, '1.3.6.1.2.1.1.1.0'))
    pdf.cell(0, 5, "Reporte de agente: " + infoagente, ln=1)
    pdf.cell(100)
    infoagente2 = str(consultaSNMP(comu, ip, '1.3.6.1.2.1.1.3.0'))
    pdf.cell(0, 5, txt="Uptime: "+ infoagente2 + "", ln=1)
    pdf.cell(200, 45, "Paquetes unicast que ha recibido una interfaz", ln=1, align="C")
    pdf.image("%s1.png" % nom, 50, 50, 99)
    pdf.cell(200, 50, "Paquetes recibidos a protocolos IPv4, incluyendo los que tienen errores.", ln=1, align="C")
    pdf.image("%s2.png" % nom, 50, 100, 99)
    pdf.cell(200, 55, "Mensajes ICMP echo que ha enviado el agente", ln=1, align="C")
    pdf.image("%s3.png" % nom, 50, 150, 99)
    pdf.cell(200, 56, "Segmentos recibidos, incluyendo los que se han recibido con errores.", ln=1, align="C")
    pdf.image("%s4.png" % nom, 50, 200, 99)
    pdf.cell(200, 65, "Datagramas entregados a usuarios UDP", ln=1, align="C")
    pdf.image("%s5.png" % nom, 50, 50, 99)
    pdf.output("%s.pdf" % nom)
    main()


def main():
    print("Menu principal")
    print("1. Agregar agente")
    print("2. Eliminar agente")
    print("3. Resumen de los agentes")
    print("4. Generar reporte")
    x = input("Opción: ")

    if x == '1':
        escribe()
    if x == '2':
        deleteLine()
    if x == '3':
        muestratodo()
    if x == '4':
        creaPDF()


main()

# divide("Windows")

# https://thispointer.com/python-how-to-delete-specific-lines-in-a-file-in-a-memory-efficient-way/
# https://mistonline.in/wp/delete-line-text-file-using-python/
# https://www.tutorialspoint.com/python/python_multithreading.htm

# 1.1 es 1.3.6.1.2.1.2.2.1.11.1 win si graf 0 lin si graf chido
# 1.2 es 1.3.6.1.2.1.4.3.0 win si graf chido lin si graf chido
# 1.3 es 1.3.6.1.2.1.5.21.0 win si graf 0 lin si  graf  chido
# 1.4 es 1.3.6.1.2.1.6.10.0 win si graf 0 lin si graf chido
# 1.5 es 1.3.6.1.2.1.7.1.0 win si graf chido lin si graf chido
