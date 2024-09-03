
#Writed by Koray Argün

#Imports
import os,sys,string,random
#List Creation Algorithm
def create_sezars_list(sezars_number):
    sezars_list=["ü","Ü","İ","ı","ö","Ö","ç","ş","Ç","Ş","ğ","Ğ"]
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
def encrypt_algorithm(key,sezars_list,mystery_number):
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
print("WELCOME TO FILE ENCRYPTER")
#Argument Intake and List Creation
try:
    command=sys.argv[1]
    folder_path=sys.argv[2]
    mystery_number=sys.argv[3]
    sezars_number=sys.argv[4]
    sezars_list=create_sezars_list(int(sezars_number))
except Exception as error:
    print("#"*100,error,"#"*100,sep="\n",end="\n")
    exit()
#Folder Encryption Function
def encrypt_folder():
    try:
        total_size=0
        for f in os.walk(folder_path):
            path=f[0]
            files=f[2]
            for i in files:
                total_size+=int(os.path.getsize(f"{path}\\{i}"))
        pointer=100/total_size
        byte_count=0
        percent=0
        for f in os.walk(folder_path):
            path=f[0]
            files=f[2]
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
                            file.write(encrypt_algorithm(str(k),sezars_list,int(mystery_number)))
                        byte_count+=1
                        percent=int(byte_count*pointer)
                        print(f"Encrypting... (%{percent})",end="\r")
                    file.close()
                except Exception as error:
                    print("#"*31+f"  !!! '{i}' can't encoding !!!  "+"#"*31+"\n",error,"#"*100,sep="\n",end="\n")
                    continue
    except Exception as error:
        print("#"*100,error,"#"*100,sep="\n",end="\n")
        exit()
#Folder Decryption Function
def decrypt_folder():
    try:
        total_size=0
        for f in os.walk(folder_path):
            path=f[0]
            files=f[2]
            for i in files:
                new_i=i.split(".")
                name=new_i[:-1]
                file_name=""
                for a in name:
                    file_name+=a+"."
                file=open(f"{path}\\{file_name}txt","r")
                content=file.read()
                total_size+=int(content.split("!point!")[0].split("!point2!")[0])
                file.close()
        pointer=100/total_size
        byte_count=0
        percent=0
        for f in os.walk(folder_path):
            path=f[0]
            files=f[2]
            for i in files:
                try:
                    new_i=i.split(".")
                    name=new_i[:-1]
                    file_name=""
                    for a in name:
                        file_name+=a+"."
                    file=open(f"{path}\\{file_name}txt","r")
                    content=file.read()
                    code2=content.split("!point!")[1]
                    code=code2.split("!end!")
                    extention=content.split("!point!")[0].split("!point2!")[1]
                    file.close()
                    file=open(f"{path}\\{file_name}txt","wb")
                    byte_list=[]
                    for b in code[1:]:
                        sayi=""
                        for k in b:
                            sayi+=decrypt_algorithm(k,sezars_list,int(mystery_number))
                        byte_list.append(int(sayi))
                        byte_count+=1
                        percent=int(byte_count*pointer)
                        print(f"Decrypting... (%{percent})",end="\r")
                    file.write(bytes(byte_list))
                    file.close()
                    os.rename(f"{path}\\{file_name}txt",f"{path}\\{file_name}{extention}")
                except Exception as error:
                    print("#"*31+f"  !!! '{i}' can't decoding !!!  "+"#"*31+"\n",error,"#"*100,sep="\n",end="\n")
                    continue
    except Exception as error:
        print("#"*100,error,"#"*100,sep="\n",end="\n")
        exit()
#Command Intake
if command=="encrypt":
    encrypt_folder()
    print("\nEncrypted Successfully.\n")
elif command=="decrypt":
    decrypt_folder()
    print("\nDecrypted Successfully.\n")
else:
    print(f"- Invalid command : '{command}' -")
    exit()
