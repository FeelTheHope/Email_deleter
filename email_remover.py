import imaplib
import customtkinter

#------------- Logic ----------
def Login():
    username = entry1.get()
    password = entry2.get()
    imapServer = username.split("@")
    imapServer = imapServer[1]
    global imap
    imap = imaplib.IMAP4_SSL("imap." + imapServer)
    imap.login(username, password)
    print("Logged in with server :" + imapServer)
    
def readBlacklist():
    imap.select("INBOX")
    file = open("emails.txt")
    blacklist = file.read()
    blacklist = blacklist.split("\n")
    print("red the blacklist")
    return blacklist

def delete():
    emails_to_delete = readBlacklist()
    tagToDelete(emails_to_delete)
    print("deleted")
    imap.expunge()

def tagToDelete(blacklist):
    for emails in blacklist:
        status, messages = imap.search(None, 'FROM',emails)
        #messages sara il nostro array contenente tutte le email provenienti da quella email
        messages = messages[0].split(b' ')

        for mail in messages:
            try:
                imap.store(mail,"+FLAGS","\\Deleted")
                print("%d mails found" % len(messages))
            except:
                print("no mail found for %s" %emails)

def Logout():
    imap.close()
    imap.logout()
    print("loged out sucseffuly")

#----------------- gui -------------------
customtkinter.set_appearance_mode("dark")

root = customtkinter.CTk()
root.geometry("500x350")

frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20,padx=60,fill="both", expand = True)


label = customtkinter.CTkLabel(master=frame,text="Email remover")
label.pack(pady= 12,padx=10)

entry1 = customtkinter.CTkEntry(master=frame,placeholder_text="Username")
entry1.pack(pady= 12,padx=10)

entry2 = customtkinter.CTkEntry(master=frame,placeholder_text="Password",show = "*")
entry2.pack(pady= 12,padx=10)

submit_button = customtkinter.CTkButton(master=frame,text= "Submit", command=Login)
submit_button.pack(pady = 12,padx = 10)

delete_emails_button = customtkinter.CTkButton(master=frame,text= "Delete emails", command=delete)
delete_emails_button.pack(pady = 12,padx = 10)

close_button = customtkinter.CTkButton(master=frame,text= "Log out", command=Logout)
close_button.pack(pady = 12,padx = 10)

root.mainloop()