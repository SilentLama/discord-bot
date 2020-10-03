import configparser
import email
import imaplib
import json


class Mail_Client():
    def __init__(self, *args):
        print(args)
        self.mail_address = args[0][0]
        self.password = args[0][1]
        self.ssl_port = args[0][2]
        self.mail_server_out = args[0][3]
        self.mail_server_in = args[0][4]
        self.mails = {}
        # self.mail_address, self.password, self.ssl_port, self.mail_server_out, self.mail_server_in = args[0]


    def __str__(self):
        return self.mail_address


    def login_imap(self): 
        self.inbox = imaplib.IMAP4_SSL(self.mail_server_in)
        self.inbox.login(self.mail_address, self.password)


    def check_inbox(self, ): #TODO reassigning status variables, add filter param
        ''' return all mails in inbox '''
        self.inbox.select("inbox")
        self.status, self.data = self.inbox.search(None, "ALL")
        # catching status error
        if self.status == "OK":
            messages = []
            for id in self.data[0].split(): # -> returns a list of byte_ids
                status, raw_mail_data = self.inbox.fetch(id, ("RFC822")) 
                if status == "OK":
                    message = email.message_from_bytes(raw_mail_data[0][1])
                    subject = email.header.make_header((email.header.decode_header(message["Subject"])))
                    # check for multipart message with attachements oder html
                    if message.is_multipart():
                        for part in message.walk():
                            content_type = part.get_content_type()
                            disposition = str(part.get("Content-Disposition"))
                            # Look for plain text parts, skip attachements
                            if content_type == "text/plain" and "attachement" not in disposition:
                                charset = part.get_content_charset()
                                #decode the base64 unicode bytestring into plain text
                                body = part.get_payload(decode=True).decode(encoding=charset, errors="ignore")
                                break
                    else:
                        #not multipart means it's plain/text and doesn't have attachemetns
                        charset = message.get_content_charset()
                        body = message.get_payload(decode=True).decode(encoding=charset, errors="ignore")
                        
                    messages.append({"id" : id, "subject" : str(subject), "message" : body})    # TODO: might as well add Mail Objects to the list
            
                else: continue

            return messages
                            

    
    def save_to_json(self, mails): #TODO rename to "save"
        json_object = json.dumps(mails, indent= 4) #TODO uses legacy variables // self.mails currently not used
        with open ("mail_box.json", "w") as file:
            json.dump(json_object, file)


    def load_from_json(self): #TODO load mails from files
        pass

    #TODO maybe keep track of mails that have been posted on discord



class Mail(): # TODO clean Mail body, delete itself, mark itself as read // could also be done by MailClient

    def __init__(self, *args):
        pass
        # self.id = 
        # self.sender = 
        # self.subject = 
        # self.message = 





def read_config():
    ''' returns: mail, password, ssl_port, mail_server_out, mail_server_in in a tuple '''
    config = configparser.ConfigParser()
    config.read("bot_config.ini")
    mail = config["Mail"]["Mail_Adress"]
    password = config["Mail"]["Passwort"]
    ssl_port = config["Mail"]["SSL_Port"]
    mail_server_out = config["Mail"]["Mail_Server_Out"]
    mail_server_in = config["Mail"]["Mail_Server_In"]
    return mail, password, ssl_port, mail_server_out, mail_server_in


def create_config():
    config = configparser.ConfigParser()
    config["Mail"] = {
        "Mail_Adress": "XXXXXX",
        "Passwort" : "XXXXXX",
        "SSL_Port" : "465",
        "Mail_Server_Out": "smtp.gmail.com",
        "Mail_Server_In": "imap.gmail.com"
    }
    with open ("bot_config.ini", "w") as configfile:
        config.write(configfile)

def main():
    mail_client = Mail_Client(read_config())
    print(mail_client)
    mail_client.login_imap()
    print(mail_client.check_inbox())
    # mail_client.save_to_json(mail_client.mails)


if __name__ == "__main__":
    main()