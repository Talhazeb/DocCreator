import configparser
import os
from cryptography.fernet import Fernet

class Author:
    def __init__(self, full_name, short_name, email, phone, mobile_phone, role,
                 extra_info1, extra_info2, extra_info3, extra_info4, extra_info5, password):
        self.full_name = full_name
        self.short_name = short_name
        self.email = email
        self.phone = phone
        self.mobile_phone = mobile_phone
        self.role = role
        self.extra_info1 = extra_info1
        self.extra_info2 = extra_info2
        self.extra_info3 = extra_info3
        self.extra_info4 = extra_info4
        self.extra_info5 = extra_info5
        self.password = password

    def to_dict(self):
        return {
            'SignerFullName': self.full_name,
            'SignerShortName': self.short_name,
            'SignerEmail': self.email,
            'SignerPhone': self.phone,
            'SignerMobilePhone': self.mobile_phone,
            'SignerRole': self.role,
            'SignerExtraInfo1': self.extra_info1,
            'SignerExtraInfo2': self.extra_info2,
            'SignerExtraInfo3': self.extra_info3,
            'SignerExtraInfo4': self.extra_info4,
            'SignerExtraInfo5': self.extra_info5
        }

    def save(self, config):
        signers_dir = config.get_signers_dir()
        ini_path = os.path.join(signers_dir, f"Signer-{self.short_name}.ini")
        
        author_config = configparser.ConfigParser()
        author_config['Author'] = self.to_dict()
        
        with open(ini_path, 'w') as configfile:
            author_config.write(configfile)

    def encrypt_signature(self, signature_path, config):
        signers_dir = config.get_signers_dir()
        encrypted_path = os.path.join(signers_dir, f"Signer-{self.short_name}-Signatur.png")
        
        key = Fernet.generate_key()
        fernet = Fernet(key)
        
        with open(signature_path, 'rb') as file:
            signature = file.read()
        
        encrypted_signature = fernet.encrypt(signature)
        
        with open(encrypted_path, 'wb') as file:
            file.write(encrypted_signature)
        
        # Save the key securely (in this example, we're saving it in the INI file, but in a real-world scenario, 
        # you might want to use a more secure method)
        ini_path = os.path.join(signers_dir, f"Signer-{self.short_name}.ini")
        author_config = configparser.ConfigParser()
        author_config.read(ini_path)
        author_config['Signature'] = {'key': key.decode()}
        
        with open(ini_path, 'w') as configfile:
            author_config.write(configfile)

    @staticmethod
    def load(short_name, config):
        signers_dir = config.get_signers_dir()
        ini_path = os.path.join(signers_dir, f"Signer-{short_name}.ini")
        
        if not os.path.exists(ini_path):
            return None
        
        author_config = configparser.ConfigParser()
        author_config.read(ini_path)
        
        author_data = author_config['Author']
        
        return Author(
            full_name=author_data['SignerFullName'],
            short_name=author_data['SignerShortName'],
            email=author_data['SignerEmail'],
            phone=author_data['SignerPhone'],
            mobile_phone=author_data['SignerMobilePhone'],
            role=author_data['SignerRole'],
            extra_info1=author_data['SignerExtraInfo1'],
            extra_info2=author_data['SignerExtraInfo2'],
            extra_info3=author_data['SignerExtraInfo3'],
            extra_info4=author_data['SignerExtraInfo4'],
            extra_info5=author_data['SignerExtraInfo5'],
            password=''  # Password is not stored in the INI file for security reasons
        )

    def decrypt_signature(self, config):
        signers_dir = config.get_signers_dir()
        encrypted_path = os.path.join(signers_dir, f"Signer-{self.short_name}-Signatur.png")
        ini_path = os.path.join(signers_dir, f"Signer-{self.short_name}.ini")
        
        if not os.path.exists(encrypted_path) or not os.path.exists(ini_path):
            return None
        
        author_config = configparser.ConfigParser()
        author_config.read(ini_path)
        
        key = author_config['Signature']['key'].encode()
        fernet = Fernet(key)
        
        with open(encrypted_path, 'rb') as file:
            encrypted_signature = file.read()
        
        try:
            decrypted_signature = fernet.decrypt(encrypted_signature)
            return decrypted_signature
        except:
            return None

    @staticmethod
    def delete(short_name, config):
        signers_dir = config.get_signers_dir()
        ini_path = os.path.join(signers_dir, f"Signer-{short_name}.ini")
        signature_path = os.path.join(signers_dir, f"Signer-{short_name}-Signatur.png")
        
        if os.path.exists(ini_path):
            os.remove(ini_path)
        
        if os.path.exists(signature_path):
            os.remove(signature_path)
            