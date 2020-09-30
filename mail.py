import configparser
import email
import imaplib

class Mail_Client():
    def __init__(self, *args):
        print(args)
        self.mail_address = args[0][0]
        self.password = args[0][1]
        self.ssl_port = args[0][2]
        self.mail_server_out = args[0][3]
        self.mail_server_in = args[0][4]
        self.mails = {}

    def __str__(self):
        return self.mail_address


    def login_imap(self):
        self.inbox = imaplib.IMAP4_SSL(self.mail_server_in)
        self.inbox.login(self.mail_address, self.password)

    def check_inbox(self):
        self.inbox.select("inbox")
        self.status, self.data = self.inbox.search(None, "ALL")
        self.mail_ids = []
        for block in self.data:
            self.mail_ids += block.split()
        # Checking for all the mail IDs from the search
        for id in self.mail_ids:
            self.status, self.data = self.inbox.fetch(id, ("RFC822"))   
            for response_part in self.data:
                if isinstance(response_part, tuple):
                    message = email.message_from_bytes(response_part[1])
                    mail_from = message["from"]
                    mail_subject = message["subject"]
                    print(message)

                    if message.is_multipart():
                        for part in message.get_payload():
                            if part.get_content_type() == "text/plain":
                                mail_content += part.get_payload()
                    else:
                        mail_content = message.get_payload()
            self.mails[id] = {
                "sender" : mail_from,
                "subject" : mail_subject,
                "message" : mail_content
                }

    

class Mail():

    def __init__(self, *args):
        pass





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
    mail_client.check_inbox()
    print(mail_client.mails)


if __name__ == "__main__":
    main()