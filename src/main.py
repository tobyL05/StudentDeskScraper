from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import pprint as pp
import chromedriver_binary
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

path_to_chromedriver = "resources\\ChromeDriver\\chromedriver.exe"
win_size = "1024,768"
link = "http://apps.simprug.binus.sch.id/student/"

class browser:
	def __init__(self):
		ser = Service(path_to_chromedriver)
		chrome_options = webdriver.ChromeOptions()
		chrome_options.add_argument("--headless")
		chrome_options.add_argument("--window-size=%s" % win_size)
		chrome_options.add_argument("log-level=3")
		#chrome_options.add_experimental_option("detach",True)
		self.driver = webdriver.Chrome(service=ser,options=chrome_options)
		self.driver.get(link)
	
	def open_link(self):
		self.driver.get(link)
		try:
			element = WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.ID, "inputan")))
		except:
			return False
		return True
		
	def login(self,id,pwd):
		self.id = id
		self.pwd = pwd
		user = self.driver.find_element(By.ID,"txtBinusianID")
		passw = self.driver.find_element(By.ID,"txtPassword")
		user.send_keys(self.id)
		passw.send_keys(self.pwd)
		self.driver.find_element(By.ID,"btnLogin").click()
		try:
			element = WebDriverWait(self.driver, 1).until(EC.presence_of_element_located((By.CLASS_NAME, "error")))
		except:
			return True
		return False

	def getSemester(self):
		semSelect = self.driver.find_element(By.XPATH,'//*[@id="CPH_uclProgressReport2010Grade11_uclSemester_cmbSemester"]')	#find the select
		self.driver.execute_script("document.getElementById('CPH_uclProgressReport2010Grade11_uclSemester_cmbSemester').style.display='inline-block';") #make it visible
		semSelect = Select(self.driver.find_element(By.XPATH,'//*[@id="CPH_uclProgressReport2010Grade11_uclSemester_cmbSemester"]')) #init select
		return semSelect

	def getTerm(self):
		termSelect = self.driver.find_element(By.XPATH,'//*[@id="CPH_uclProgressReport2010Grade11_uclTermPeriode_cmbTermPeriod"]')
		self.driver.execute_script("document.getElementById('CPH_uclProgressReport2010Grade11_uclTermPeriode_cmbTermPeriod').style.display='inline-block';") #make it visible
		termSelect = Select(self.driver.find_element(By.XPATH,'//*[@id="CPH_uclProgressReport2010Grade11_uclTermPeriode_cmbTermPeriod"]'))
		return termSelect

	def getScores(self,term):
		self.driver.find_element(By.ID,"ucMenuCenter_rptMenuCenter_hplMenuCenter_1").click()
		pageLoad = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID,'CPH_uclProgressReport2010Grade11_pnlEvenTerm'))) 
		#self.driver.get("http://apps.simprug.binus.sch.id/student/Master/ProgressReport/ProgressReport.aspx?mnc=ZDw5qw%2bnpmb40fJyIZsqpg%3d%3d")

		if term == 1:
			try:
				self.getSemester().select_by_value('1') #select by value
				pageLoad = WebDriverWait(self.driver, 10).until(EC.invisibility_of_element((By.XPATH,'//*[@id="CPH_uclProgressReport2010Grade11_uclSemester_cmbSemester"]'))) #wait until select is invisible again
				try:
					self.getTerm().select_by_value('1')
					#pageLoad = WebDriverWait(self.driver, 10).until(EC.invisibility_of_element((By.XPATH,'//*[@id="CPH_uclProgressReport2010Grade11_uclTermPeriode_cmbTermPeriod"]'))) #wait until select is invisible again
				except:
					pass
			except:
				try:
					self.getTerm().select_by_value('1')
					#pageLoad = WebDriverWait(self.driver, 10).until(EC.invisibility_of_element((By.XPATH,'//*[@id="CPH_uclProgressReport2010Grade11_uclTermPeriode_cmbTermPeriod"]'))) #wait until select is invisible again
				except:
					pass
				pass

		elif term == 2:
			try:
				self.getSemester().select_by_value('1')
				pageLoad = WebDriverWait(self.driver, 10).until(EC.invisibility_of_element((By.XPATH,'//*[@id="CPH_uclProgressReport2010Grade11_uclSemester_cmbSemester"]'))) #wait until select is invisible again
				try:
					self.getTerm().select_by_value('2')
					pageLoad = WebDriverWait(self.driver, 10).until(EC.invisibility_of_element((By.XPATH,'//*[@id="CPH_uclProgressReport2010Grade11_uclTermPeriode_cmbTermPeriod"]'))) #wait until select is invisible again
				except:
					pass
			except:
				try:
					self.getTerm().select_by_value('2')
					pageLoad = WebDriverWait(self.driver, 10).until(EC.invisibility_of_element((By.XPATH,'//*[@id="CPH_uclProgressReport2010Grade11_uclTermPeriode_cmbTermPeriod"]'))) #wait until select is invisible again
				except:
					pass

		elif term == 3:
			try:
				self.getSemester().select_by_value('2')
				pageLoad = WebDriverWait(self.driver, 3).until(EC.invisibility_of_element((By.XPATH,'//*[@id="CPH_uclProgressReport2010Grade11_uclSemester_cmbSemester"]'))) #wait until select is invisible again
				try:
					self.getTerm().select_by_value('3')
					pageLoad = WebDriverWait(self.driver, 3).until(EC.invisibility_of_element((By.XPATH,'//*[@id="CPH_uclProgressReport2010Grade11_uclTermPeriode_cmbTermPeriod"]'))) #wait until select is invisible again
				except:
					pass
			except:
				try:
					self.getTerm().select_by_value('3')
					pageLoad = WebDriverWait(self.driver, 3).until(EC.invisibility_of_element((By.XPATH,'//*[@id="CPH_uclProgressReport2010Grade11_uclTermPeriode_cmbTermPeriod"]'))) #wait until select is invisible again
				except:
					pass
			
		else:
			try: #check if already selected
				self.getSemester().select_by_value('2')
				pageLoad = WebDriverWait(self.driver, 3).until(EC.invisibility_of_element((By.XPATH,'//*[@id="CPH_uclProgressReport2010Grade11_uclSemester_cmbSemester"]'))) #wait until select is invisible again
				try: 
					self.getTerm().select_by_value('4')
					pageLoad = WebDriverWait(self.driver, 3).until(EC.invisibility_of_element((By.XPATH,'//*[@id="CPH_uclProgressReport2010Grade11_uclTermPeriode_cmbTermPeriod"]'))) #wait until select is invisible again
				except: #if all already selected
					pass
			except:
				try: 
					self.getTerm().select_by_value('4')
					pageLoad = WebDriverWait(self.driver, 3).until(EC.invisibility_of_element((By.XPATH,'//*[@id="CPH_uclProgressReport2010Grade11_uclTermPeriode_cmbTermPeriod"]'))) #wait until select is invisible again
				except: #if all already selected
					pass

		scores = self.driver.find_element(By.ID,"CPH_uclProgressReport2010Grade11_pnlEvenTerm").get_attribute('outerHTML') #select the table
		scoresDF = pd.read_html(scores)
		#pp.pprint(scoresDF)
		return scoresDF

	def getName(self):
		name = self.driver.find_element(By.XPATH,'//*[@id="top-nav"]/ul[2]/li[2]/a/span')
		return name.text

	def quitBrowser(self):
		self.driver.quit()

def start():
	test = browser()
	test.login("1670004246","070505-02")
	#print(test.getName())
	pp.pprint(test.getScores(1))
	test.quitBrowser()

if __name__ == "__main__":
	start()

