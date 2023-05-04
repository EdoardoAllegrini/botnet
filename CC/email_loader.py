EMAIL_PATH = r"/home/eddi/Desktop/hw_cybersec/CC/email.json"

def load_email(email_path):
    import json
    with open(email_path) as f:
        f_d = json.load(f)
    
    return f_d    

if __name__ == "__main__":
    load_email(EMAIL_PATH)