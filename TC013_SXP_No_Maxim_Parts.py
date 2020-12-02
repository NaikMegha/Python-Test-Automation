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


class TC013_SXP(unittest.TestCase):

    def test_TC013_SXP_No_Maxim_Parts(self):
        try:
            global driver, imagename, imagecount, tc_execflag, qc_tester, qc_tc_exec_path, qc_ts_name

            appname = config.appname
            strCurrTestName = self._testMethodName.replace('test_', '').strip()

            # Initialize Report :
            base_url = config.base_url.strip()

            # Driver SetUp :
            implicitly_wait = config.implicitly_wait
            mobile_emulation = 'No'
            mobile_device = 'iPad'  # iPhone 6/7/8 Plus,iPhone X,iPad,iPad Pro
            driver = drivers.setup(config.drivertype, config.driverpath, mobile_emulation,
                                          mobile_device, implicitly_wait)

            # read execution flag from Database
            DBData = dbutility(config.DB_Prod_Server, config.DB_Name, config.DB_Port, config.DB_User,
                               config.DB_Prod_Pwd)
            tc_execflag, qc_tester, qc_tc_exec_path, qc_ts_name = DBData.ReadTCExecDetailsFromDB(appname, strCurrTestName)

            # Execution Flag If condition
            if tc_execflag.lower().strip() == 'Yes'.lower().strip():
                testcasedescription = strCurrTestName

                # Initialize Report
                reportfilepath, screenshotpath = report.InitializeReport(config.ReportRootPath, strCurrTestName, testcasedescription)

                # Read Test Data
                SF_User = DBData.ReadParaValueFromDB(appname, strCurrTestName, "DT_SF_USER")
                SF_Password = DBData.ReadParaValueFromDB(appname, strCurrTestName, "DT_SF_PASSWORD")
                strPartNum = DBData.ReadParaValueFromDB(appname, strCurrTestName, "DT_PART_NUM")

                # ****************************** START ******************************
                action.login(driver, reportfilepath, base_url, SXP_User, SXP_Password, screenshotpath)

                # Step 2 and 3 START : Enter "MAX232ACPE+" and Press "Enter" or Click Search icon
                # Set Search Text
                driver.find_element_by_id("cross-search-bar").send_keys(strPartNum)

                control.wait(1)
                report.CaptureScreenShot(f"Search KeyWord {strPartNum}", screenshotpath)
                # Click Search icon

                driver.find_element_by_id("cross-search-bar").click()
                control.wait(10)

                sText = driver.find_element_by_xpath(".//*[@id='js-cross-reference-results']").text;
                if str(sText).find("No results"):
                    report.ReportHTMLLog("Pass", "No results Validation", "No Results to show is displayed when there are no matching search")
                    report.CaptureScreenShot("No results Validation", screenshotpath)
                # ****************************** END ********************************

        except Exception as ex:
            report.ReportHTMLLog("Fail", " Test Script Exception ", f" Exception:{ex}");
            report.CaptureScreenShot(" ScreenShot at Test Script Exception  ", screenshotpath);
            control.wait(2)
            self.tearDown()
            control.wait(2)

    def tearDown(self):
        # Close driver
        driver.close()
        # End HTML Report :
        #report.EndReport()

if __name__ == '__main__':
    TC013_SXP.test_TC013_SXP_No_Maxim_Parts()
