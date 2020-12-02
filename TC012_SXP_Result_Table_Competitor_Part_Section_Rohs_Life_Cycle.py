from maximtaf import drivers, control, dbutility, report
from selenium.webdriver.common.by import By
import unittest
from actions import action
import config

# Declare public variables
driver = None

tc_execflag = ''
qc_tester = ''
qc_tc_exec_path = ''
qc_ts_name = ''


class TC012_SXP(unittest.TestCase):
    def TC012_SXP_Result_Table_Competitor_Part_Section_Rohs_Life_Cycle(self):
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
            tc_execflag, qc_tester, qc_tc_exec_path, qc_ts_name = DBData.ReadTCExecDetailsFromDB(appname,
                                                                                                 strCurrTestName)
            # ****************************** START ******************************
            blnCrossSearchResultsFlag = False
            if tc_execflag.lower().strip() == 'Yes'.lower().strip():
                testcasedescription = strCurrTestName

                # Initialize Report
                reportfilepath, screenshotpath = report.InitializeReport(config.ReportRootPath, strCurrTestName,
                                                                         testcasedescription)

                # Read Test Data
                SXP_User = DBData.ReadParaValueFromDB(appname, strCurrTestName, "DT_SXP_USER")
                SXP_Password = DBData.ReadParaValueFromDB(appname, strCurrTestName, "DT_SXP_PASSWORD")
                strRootPart = DBData.ReadParaValueFromDB(appname, strCurrTestName, "DT_ROOT_PART");
                RootPartCompetitorName = DBData.ReadParaValueFromDB(strCurrTestName, "DT_ROOT_PART_COMPETITOR_NAME");
                RootPartDescription = DBData.ReadParaValueFromDB(strCurrTestName, "DT_ROOT_PART_DESCRIPTION");

                strLsColumnList = []
                strLsColumnList.extend(str(StrColList).split(";"));
                strLsColumnValue = []
                strLsColumnValue.extend(str(strColumnValues).split(';'));
                # ****************************** START ******************************
                # Login and Login Validation
                action.login(driver, reportfilepath, base_url, SXP_User, SXP_Password, screenshotpath)

                # Step 2 and 3 START : Enter "MAX232ACPE+" and Press "Enter" or Click Search icon
                # Set Search Text
                driver.find_element_by_id("cross-search-bar").send_keys(strRootPart)

                control.wait(1)
                report.CaptureScreenShot(f"Search KeyWord {strRootPart}", screenshotpath)
                # Click Search icon

                driver.find_element_by_id("cross-search-bar").submit()
                control.wait(10)

                # Check Page loader image and increase wait time
                if control.IsElementPresent((By.XPATH, "//*[@id='divContent']/div[3]/img"), "Page Loading"):
                    control.wait(30)

                # Displayed
                # validate Cross Search Results Section
                control.wait(10)
                # CrossSearchResults = []

                CrossSearchResults = driver.find_element_by_xpath(
                    "//div[@id='divContent']/div[@class='cross-search-parent-container']")
                control.wait(60)

                if CrossSearchResults.is_displayed() and not CrossSearchResults.text.find("No results"):
                    control.ScrollToElementbyRef(CrossSearchResults, "Cross Search Results Section")
                    control.wait(1)
                    if CrossSearchResults.text.find("results for") and (CrossSearchResults.text.find(strRootPart)):
                        report.ReportHTMLLog("Pass", f"Validate Cross Search Results for Part : {strRootPart}",
                                             f" Cross Search Results for Part : {strRootPart} has been displayed")
                        report.CaptureScreenShot(f"Validate Cross Search Results for Part : {strRootPart}",
                                                 screenshotpath)
                        blnCrossSearchResultsFlag = True
                    else:
                        report.ReportHTMLLog("Fail", f"Validate Cross Search Results for Part : {strRootPart}",
                                             f" Cross Search Results for Part : {strRootPart} has not been displayed")
                        report.CaptureScreenShot(f"Validate Cross Search Results for Part : {strRootPart}",
                                                 screenshotpath)
                        # Assert.Fail("Validate Cross Search Results for Part : " + strRootPart, "  Cross Search Results for Part : " + strRootPart + " has not been displayed");
                        self.Assert(f"Validate Cross Search Results for Part :{strRootPart}",
                                    f"  Cross Search Results for Part : {strRootPart} has not been displayed")
                else:
                    report.ReportHTMLLog("Fail", f"Validate Cross Search Results for Part : {strRootPart}",
                                         f"  Cross Search Results for Part : {strRootPart}  has not been displayed")
                    report.CaptureScreenShot(f"Validate Cross Search Results for Part : {strRootPart}", screenshotpath)
                    self.assertIs(CrossSearchResults.is_displayed(),
                                  f"Validate Cross Search Results for Part :{strRootPart},Cross Search Results for Part : {strRootPart} has not been displayed")
                # //********************** Step 2 and 3 END : Enter "MAX232ACPE+" and Press "Enter" or Click Search icon **********************
                # //********************** Step 4 START : Price/Unit field in search results **********************
                if blnCrossSearchResultsFlag:
                    CompetitorParts = driver.find_elements_by_xpath("//div[@class='crossref-part']/div[@id='CrossInfo']/div[@class='js-section-header col-lg-12 crossref-cross']")

                    if(len(CompetitorParts) >= 1):
                        for intPRowCnt, competiror_part in enumerate(CompetitorParts,start=0):
                            #MAX232IN (Texas Instruments)
                            if competiror_part.text == strRootPart + f" ({RootPartCompetitorName})\r\n{RootPartDescription}":
                                report.ReportHTMLLog("Pass",f"Validate Results for Competitor Part : {strRootPart} Cross Search Results for Competitor Part : {strRootPart} has been displayed")
                                report.CaptureScreenShot(f"Validate Cross Search Results for Competitor Part : {strRootPart}",ScreenShotPath)
                            elif (intPRowCnt + 1) == len(CompetitorParts):
                                report.ReportHTMLLog("Fail", f"Validate Results for Competitor Part : {strRootPart}",
                                                      f"  Cross Search Results for Competitor Part : {strRootPart}  has not been displayed")
                                Control.CaptureScreenShot(f"Validate Results for Competitor Part : {strRootPart}",
                                                          screenshotpath)
                                self.assertIs(not CrossSearchResults.is_displayed(),f"Validate Cross Search Results for Part :{strRootPart},Cross Search Results for Part : {strRootPart} has not been displayed")
                            break
                    else:
                        report.ReportHTMLLog("Fail",f"Validate Cross Search Results Part Numbers for Part : {strRootPart}",
                                              f"  Cross Search Results Part Numbers for Part : {strRootPart} are not been displayed")
                        report.CaptureScreenShot(f"Validate Cross SearchResults Part Numbers for Part : {strRootPart}",screenshotpath)
                        self.assertIs(len(CompetitorParts) == 0,f"Validate Cross Search Results Part Numbers for Part :{strRootPart}" ,
                                    f"  Cross Search Results  Part Numbers for Part : {strRootPart}  are not been displayed")


            # ****************************** END ********************************


        except Exception as ex:
            report.ReportHTMLLog("Fail", " Exception ", str(ex))
            report.CaptureScreenShot("Exception ", screenshotpath)
            self.tearDown()

    def tearDown(self):
        # Close driver
        drivers.close()
        # End HTML Report :
        report.EndReport()


if __name__ == '__main__':
    TC012_SXP.TC012_SXP_Result_Table_Competitor_Part_Section_Rohs_Life_Cycle()
