from maximtaf import drivers, control, dbutility, report
from selenium.webdriver.common.by import By
import unittest
from actions import action
import config, actions

# Declare public variables
driver = None

tc_execflag = ''
qc_tester = ''
qc_tc_exec_path = ''
qc_ts_name = ''

class TC002_SXP(unittest.TestCase):

    def test_TC002_SXP_CrossRefSearchOption(self):
        try:
            global driver, imagename, imagecount, tc_execflag, qc_tester, qc_tc_exec_path, qc_ts_name

            appname = config.appname
            strCurrTestName = self._testMethodName.replace('test_', '').strip()

            #Initialize Report
            base_url = config.base_url.strip()

            #Driver Setup
            implicitly_wait = config.implicitly_wait
            mobile_emulation = 'No'
            mobile_device = ''
            driver = driver.setup(config.drivertype,config.driverpath,mobile_emulation,mobile_device,implicitly_wait)

            #Read execution flag from the database
            DBData = dbutility(config.DB_Prod_Server,config.DB_Name,config.DB_Port,config.DB_User,config.DB_Prod_Pwd)
            tc_execflag, qc_tester, qc_tc_exec_path, qc_ts_name = DBData.ReadTCExecDetailsFromDB(appname, strCurrTestName)

            # Execution Flag If condition
            if tc_execflag.lower().strip() == 'Yes'.lower().strip():
                testcasedescription = strCurrTestName

            # Initialize Report
            reportfilepath, screenshotpath = report.InitializeReport(config.ReportRootPath, strCurrTestName,
                                                                         testcasedescription)

            # Read Test Data
            SF_User = DBData.ReadParaValueFromDB(appname, strCurrTestName, "DT_SF_USER")
            SF_Password = DBData.ReadParaValueFromDB(appname, strCurrTestName, "DT_SF_PASSWORD")
            strMultiPartNums = DBData.ReadParaValueFromDB(appname, strCurrTestName, "DT_PART_NUM")
            strMultiNegativePartNums = DBData.ReadParaValueFromDB(appname, strCurrTestName, "DT_PART_NUM_NEGATIVE")

            # ****************************** START ******************************
            action.login(base_url,reportfilepath,SF_User,SF_Password)




            #****************************** END ***********************************

        except Exception as ex:
            report.ReportHTMLLog("Fail", " Exception ", str(ex))

        def tearDown(self):
            # Close driver
            drivers.close()
            # End HTML Report :
            report.EndReport()

if __name__ == '__main__':
    TC001_XX.test_TC001_XX_YYYY()







