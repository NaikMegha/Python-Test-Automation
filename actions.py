from maximtaf import drivers, control, dbutility, report
from selenium.webdriver.common.by import By
from selenium import webdriver
import config, unittest
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
# driver = None

reportfolderpath = ""
ReportRootPath = config.ReportRootPath
# strReportImageFolderPath = config.strReportImageFolderPath
# ScreenShotPath = config.ScreenShotPath

class action:

    # def __init__(self):
    #     self.reportfolderpath = ""
    #     self.driver = config.driver
    #     self.ReportRootPath = config.ReportRootPath
    #     self.strReportImageFolderPath = config.strReportImageFolderPath
    #     self.ScreenShotPath = config.ScreenShotPath
    #     # self.reportfilepath = config.
    # Login
    def login(driver, reportfilepath, base_url, username, password, screenshotpath):
        # global driver
        global ReportRootPath
        # global strReportImageFolderPath
        driver.get(base_url)

        report.ReportHTMLLog("Pass", "Launch SXP URL", " SXP URL " + base_url + " Launched")
        control.wait(10)
        # Check Spinner :

        if not driver.find_element_by_xpath("//div[@class='loading-spinner']").is_displayed():
            driver.find_element_by_id("loginlink").click()
            if driver.find_element_by_id("loginlink").is_displayed():
                driver.find_element_by_name("username").send_keys(username)
                driver.find_element_by_name("password").send_keys(password)
                driver.find_element_by_xpath(
                    "//*[@id='gigya-login-form']/div/div/div/input[@type='submit' and @class='gigya-input-submit']").click()
            else:
                report.ReportHTMLLog("Fail", "Page Load Time", " Home Page is not loaded in 15 Seconds.")
                report.CaptureScreenShot("Test Image", screenshotpath)
        else:
            report.ReportHTMLLog.ReportHTMLLog("Fail", "Spinner Time", " Spinner is not loaded in 30 Seconds.")
            # report.capturescreenshot(driver, "Test Image", screenshotpath)
        #action.login_validation(base_url, username, password, screenshotpath)

    # Login Validation
    def login_validation(base_url, username, password, screenshotpath):
        for logincheck in range(5):
            if control.IsElementPresent((By.ID, 'logoutlink'), '10') and control.IsElementVisible(
                    (By.ID, 'logoutlink'), '10'):
                report.ReportHTMLLog("Pass", "SXP Login", "SXP Login Successful with URL: " + base_url + " and User : " + username)
                report.CaptureScreenShot('Login Successfully', screenshotpath)
                break
            elif logincheck == 5:
                report.ReportHTMLLog("Fail", "SXP Login",
                                      "SXP Login is not Successful with URL: " + base_url + " and User : " + password)
                report.CaptureScreenShot('step description', screenshotpath)

    # Log out
    def logout(base_url, username, password, screenshotpath):
        # global driver
        global ReportRootPath, imagecount
        if control.IsElementPresent((By.ID, 'logoutlink'), '10') and control.IsElementVisible((By.ID, 'logoutlink'),
                                                                                              '10'):
            control.ClickLink((By.ID, 'logoutlink'), "Logout")
            # <a id="logoutlink" h
            report.ReportHTMLLog("Pass", "SXP Logout", " SXP Logout is Successful.")
            report.CaptureScreenShot('SXP Logout is Successful', screenshotpath)
        else:
            report.ReportHTMLLog("Fail", "SXP Logout", " SF Logout is not Successful.")
            report.CaptureScreenShot('SXP Logout is not Successful', screenshotpath)


    def search_part(reportfilepath, strMultiPartNums, strMultiNegativePartNums, screenshotpath):
        arrPartNums = str(strMultiPartNums).split(';')
        for strPartNum in arrPartNums:
            # Scrool to top of the page
            control.ScrollToTop()
            # control.ScrollToElement(driver, (By.LINK_TEXT, "ORDER"), "Scroll To Order") {TypeError}can only concatenate str (not "AttributeError") to str
            control.wait(1)
            # click on Order
            control.ClickLinkByText("ORDER", "ORDER")
            # click on SEARCH PRICE AND AVAILABILITY
            control.ClickLinkByText("SEARCH PRICE AND AVAILABILITY", "SEARCH PRICE AND AVAILABILITY")
            #  CloseChatWindowIfExist
            # Action.CloseChatWindowIfExist()
            # Enter Part
            control.SetText((By.NAME, 'partSearchField'), strPartNum, 'PartNum')
            control.wait(1)
            report.CaptureScreenShot('step description', screenshotpath)
            # Click search
            control.ClickButton((By.ID, 'searchButton'), 'Search')
            control.wait(1)
            # Validate and click on view orderable parts
            if control.IsElementPresent((By.XPATH, "//div[@class='purple uppercase smallest partOption pointer width160' and @href='javascript:void(0)']"), '05'):
                control.wait(2)
                # if (driver.find_elements(By.XPATH, "//div/img[@class='partOptionImg rotate1']")):# partOptionImg rotate2 Already Expand the Item
                if (control.IsElementPresent((By.XPATH, "//div/img[@class='partOptionImg rotate1']"),'10')): # partOptionImg rotate2 Already Expand the Item
                    control.ClickLink((By.XPATH, "//div[@class='purple uppercase smallest partOption pointer width160' and @href='javascript:void(0)']"), "View Orderable Parts")
                    control.wait(1)
                    # report.CaptureScreenShot('step description', screenshotpath)
                # elif (driver.find_elements(By.XPATH, "//div/img[@class='partOptionImg rotate2']")):# partOptionImg rotate2 Already Expand the Item
                elif (control.IsElementPresent((By.XPATH, "//div/img[@class='partOptionImg rotate2']"), '10')):  # partOptionImg rotate2 Already Expand the Item
                    control.wait(1)
                    # report.CaptureScreenShot('step description', screenshotpath)
                else:
                    report.ReportHTMLLog("Fail", "View Orderable Parts", "View Orderable Parts are not displayed")

                # report.CaptureScreenShot('View Orderable Parts', screenshotpath)

            # Validate and Part num
            if control.IsElementPresent((By.LINK_TEXT, strPartNum), '10'):
                report.ReportHTMLLog("Pass", "Part num Search", strPartNum + " Part num is displayed ")
                report.CaptureScreenShot("Part num Search", screenshotpath)
            else:
                report.ReportHTMLLog("Fail", "Part num Search", strPartNum + " Part num is not displayed ")
                report.CaptureScreenShot("Part num Search", screenshotpath)
                # GE.EndReport()
                # Assert.Fail(strPartNum + " Part num is not displayed ")
                # assertRaises(strPartNum + " Part num is not displayed ")
                # assert assert.ra

        arrNegativePartNums = str(strMultiNegativePartNums).split(';')
        for strNegativePartNum in arrNegativePartNums:
            # Scrool to top of the page
            control.ScrollToTop()
            # click on Order
            control.ClickLinkByText('ORDER', 'ORDER')
            # click on SEARCH PRICE AND AVAILABILITY
            control.ClickLinkByText("SEARCH PRICE AND AVAILABILITY", "SEARCH PRICE AND AVAILABILITY")
            #  CloseChatWindowIfExist
            # Action.CloseChatWindowIfExist()
            # Enter Part
            control.SetText((By.NAME, 'partSearchField'), strNegativePartNum, 'PartNum')
            # Click search
            control.ClickButton((By.ID, 'searchButton'), 'Search')
            control.wait(2)
            report.CaptureScreenShot('step description', screenshotpath)
            # Validate and click on view orderable parts
            if control.CheckElementExistByPartialText((By.XPATH, "//div/span[@class='bold']"),
                                                      "Sorry, no results could be found",
                                                      "Sorry, no results could be found"):
                report.ReportHTMLLog("Pass", "Verify Part num Search Results", "Sorry, no results could be found for " + strPartNum + " is displayed Successfully ")
                report.CaptureScreenShot("Verify Part num Search Results", screenshotpath)
            else:
                report.ReportHTMLLog("Fail", "Verify Part num Search Results",
                                      "Sorry, no results could be found for " + strPartNum + " is not displayed Successfully ")
                report.CaptureScreenShot("Verify Part num Search Results", screenshotpath)