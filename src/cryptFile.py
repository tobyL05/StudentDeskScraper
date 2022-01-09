from cryptography.fernet import Fernet
import keyring as kr
import os

class Encryptor():
	def __init__(self):
		#generate key
		self.key = Fernet.generate_key()
		#save key to a file
		open("studesk.key",'x')
		with open("studesk.key",'wb') as filekey:
			filekey.write(self.key)

	def encrypt(self,id,pwd):
		f = Fernet(self.key)
		return f.encrypt(str(id).encode()),f.encrypt(str(pwd).encode())
		#encrypt details
		#return encrypted details 

class Decryptor():
	def __init__(self):
		#read key
		with open("studesk.key",'rb') as filekey:
			self.key = filekey.read()

	def decrypt(self):
		f = Fernet(self.key)
		#get details from keyring
		user = kr.get_password("StudentDesk2","studeskUser")
		pwd = kr.get_password("StudentDesk2","studeskPwd")

		#use key to decrypt details
		userDec = f.decrypt(user.encode())
		pwdDec = f.decrypt(pwd.encode())

		return userDec,pwdDec
		#return user and pass 
		#login

if __name__ == "__main__":
	kr.delete_password("StudentDesk2","studeskUser")
