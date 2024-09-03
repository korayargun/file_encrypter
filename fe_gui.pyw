from tkinter import *
from tkinter import filedialog
from functools import partial
import os,string,random

#List Creation Algorithm
def create_sezars_list(sezars_number):
    sezars_list = ["ü","Ü","İ","ı","ö","Ö","ç","ş","Ç","Ş","ğ","Ğ"]
    for i in string.ascii_letters:
        sezars_list.append(i)
    for i in string.digits:
        sezars_list.append(i)
    for i in string.whitespace:
        sezars_list.append(i)
    for i in string.punctuation:
        if (i=="'")or(i=='"'):
            continue
        else:
            sezars_list.append(i)
    random.seed(sezars_number)
    random.shuffle(sezars_list)
    return sezars_list
#Encryption Algorithm
def encrpt_algorithm(key,sezars_list,mystery_number):
    encrypted_key=""
    for i in key:
        if (i=="'")or(i=='"'):
            encrypted_key+=i
        else:
            dex=sezars_list.index(i)+mystery_number
            if dex>len(sezars_list):
                encrypted_key+=sezars_list[dex%len(sezars_list)]
            elif dex==len(sezars_list):
                encrypted_key+=sezars_list[0]
            else:
                encrypted_key+=sezars_list[dex]
    return encrypted_key
#Decryption Algorithm
def decrypt_algorithm(encrypted_key,sezars_list,mystery_number):
    key=str()
    for i in encrypted_key:
        if (i=="'")or(i=='"'):
            key+=i
        else:
            dex=sezars_list.index(i)-mystery_number
            if dex<len(sezars_list)*-1:
                key+=sezars_list[dex%(len(sezars_list)*-1)]
            else:
                key+=sezars_list[dex]
    return key

#File Encryption Function
def encrypt_folder(folder_path):
    try:
        for f in os.walk(folder_path):
            path = f[0]
            files = f[2]
            for i in files:
                try:
                    new_i=i.split(".")
                    extention=new_i[-1]
                    name=new_i[:-1]
                    file_name=""
                    for a in name:
                        file_name+=a+"."
                    file_size = os.path.getsize(f"{path}\\{i}")
                    os.rename(f"{path}\\{i}",f"{path}\\{file_name}txt")
                    file = open(f"{path}\\{file_name}txt","rb")
                    content=file.read()
                    code = list(content)
                    file.close()
                    file=open(f"{path}\\{file_name}txt","w")
                    file.write("")
                    file.close()
                    file=open(f"{path}\\{file_name}txt","a")
                    file.write(str(file_size)+"!point2!"+extention+"!point!")
                    for b in code:
                        file.write("!end!")
                        for k in str(b):
                            file.write(encrpt_algorithm(str(k),sezars_list,int(mystery_number)))
                    file.close()
                except Exception as error:
                    print("#"*100,"#"*31+f"  !!! '{i}' can't encoding !!!  "+"#"*31+"\n",error,"\n"+"#"*100,"#"*100,sep="\n",end="\n")
                    continue
    except Exception as error:
        print("#"*100,"#"*100+"\n",error,"\n"+"#"*100,"#"*100,sep="\n",end="\n")
#File Decryption Function
def decrypt_folder(folder_path):
    try:
        for f in os.walk(folder_path):
            path = f[0]
            files = f[2]
            for i in files:
                try:
                    new_i=i.split(".")
                    name=new_i[:-1]
                    file_name=""
                    for a in name:
                        file_name+=a+"."
                    file=open(f"{path}\\{file_name}txt","r")
                    content=file.read()
                    code2 = content.split("!point!")[1]
                    code = code2.split("!end!")
                    extention=content.split("!point!")[0].split("!point2!")[1]
                    file.close()
                    file=open(f"{path}\\{file_name}txt","wb")
                    byte_list = []
                    for b in code[1:]:
                        sayi = ""
                        for k in b:
                            sayi += decrypt_algorithm(k,sezars_list,int(mystery_number))
                        byte_list.append(int(sayi))
                    file.write(bytes(byte_list))
                    file.close()
                    os.rename(f"{path}\\{file_name}txt",f"{path}\\{file_name}{extention}")
                except Exception as error:
                    print("#"*100,"#"*31+f"  !!! '{i}' can't decoding !!!  "+"#"*31+"\n",error,"\n"+"#"*100,"#"*100,sep="\n",end="\n")
                    continue
    except Exception as error:
        print("#"*100,"#"*100+"\n",error,"\n"+"#"*100,"#"*100,sep="\n",end="\n")

def back(selection):
            global file_paths,mystery_number,sezars_number,warning_label
            try:
                del file_paths
                del mystery_number
                del sezars_number
            except:
                pass
            try:
                filebtn.destroy()
            except:
                pass
            try:
                toplabel.destroy()
                myslbl.destroy()
                szrlbl.destroy()
                mysget.destroy()
                szrsget.destroy()
            except:
                pass
            try:
                path_label.destroy()
            except:
                pass
            if selection==True:
                enbtn.destroy()
            else:
                debtn.destroy()
            try:
                warning_label.destroy()
            except:
                pass

            backbtn.destroy()
            main()

w=Tk()
w.title("File Encrypter")
w.config(bg="#AEB6BF")
w.geometry("242x200")
w.iconbitmap("icon.ico")

def main():

    global toplabel,enbutton,debutton

    toplabel=Label(w,text="File Encrypter",font=("Times New Roman",20),bg="#AEB6BF")
    toplabel.grid(row=0,column=0,columnspan=2,pady=10,padx=43)

    def choose(selection):

        global backbtn,filebtn,myslbl,mysget,szrlbl,szrsget,enbtn,debtn

        enbutton.destroy()
        debutton.destroy()

        backbtn = Button(w,text="< Back",command=partial(back,selection))
        backbtn.grid(row=0,column=0,columnspan=2,padx=0,sticky="nw")

        def get_path():
            global file_paths,path_label
            file_paths = filedialog.askdirectory()
            filebtn.destroy()
            path_label = Label(w,text="Folder selected.",bg="#AEB6BF",font=("Times New Roman",12))
            path_label.grid(row=1,column=0,columnspan=2)

        filebtn = Button(w,text="Choose Folder",command=get_path)
        filebtn.grid(row=1,column=0,columnspan=2)

        myslbl = Label(w,text="Mystery number :",bg="#AEB6BF",font=("Times New Roman",12))
        myslbl.grid(row=2,column=0)

        mysget = Entry(w,width=10)
        mysget.grid(row=2,column=1,pady=5)

        szrlbl = Label(w,text="Sezar's number :",bg="#AEB6BF",font=("Times New Roman",12))
        szrlbl.grid(row=3,column=0)

        szrsget = Entry(w,width=10)
        szrsget.grid(row=3,column=1,pady=5)

        if selection==True:
            toplabel.config(text="Encrypt")
            toplabel.grid(row=0,column=0,columnspan=2,pady=10,sticky="w",padx=70)
            def accept_en():
                global mystery_number,sezars_number,sezars_list,warning_label

                try:
                    warning_label.destroy()
                except:
                    pass

                try:
                    sezars_number = int(szrsget.get())
                    mystery_number = int(mysget.get())
                    file_path = file_paths

                    sezars_list = create_sezars_list(sezars_number)
                    encrypt_folder(file_path)
                    warning_label = Label(w,text="Encrypted",bg="green",fg="white",font=("Times New Roman",12))
                    warning_label.grid(row=5,column=0,columnspan=2,sticky="nwse")
                except:
                    warning_label = Label(w,text="Please choose folder and fill blanks.",bg="red",fg="white",font=("Times New Roman",12))
                    warning_label.grid(row=5,column=0,columnspan=2,sticky="nwse")

            enbtn = Button(w,text="Encrypt",command=accept_en)
            enbtn.grid(row=4,column=0,columnspan=2,pady=3)
        else:
            toplabel.config(text="Decrypt")
            toplabel.grid(row=0,column=0,columnspan=2,pady=10,sticky="w",padx=70)
            def accept_de():
                global mystery_number,sezars_number,sezars_list,warning_label

                try:
                    warning_label.destroy()
                except:
                    pass

                try:
                    sezars_number = int(szrsget.get())
                    mystery_number = int(mysget.get())
                    file_path = file_paths

                    sezars_list = create_sezars_list(sezars_number)
                    decrypt_folder(file_path)
                    warning_label = Label(w,text="Decrypted",bg="green",fg="white",font=("Times New Roman",12))
                    warning_label.grid(row=5,column=0,columnspan=2,sticky="nwse")
                except:
                    warning_label = Label(w,text="Please choose folder and fill blanks.",bg="red",fg="white",font=("Times New Roman",12))
                    warning_label.grid(row=5,column=0,columnspan=2,sticky="nwse")

            debtn = Button(w,text="Decrypt",command=accept_de)
            debtn.grid(row=4,column=0,columnspan=2,pady=3)

    enbutton=Button(w,text="Encrypt",command=partial(choose,True))
    enbutton.grid(row=1,column=0)

    debutton=Button(w,text="Decrypt",command=partial(choose,False))
    debutton.grid(row=1,column=1)

main()

w.mainloop()