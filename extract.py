from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver

USERNAME = 'oauth-mcarlo.rg-11d9a'
ACCESS_KEY = 'b19834d6-f40b-4b6b-a347-3f8d2a5b11ba'


def createDriver() -> webdriver.Chrome:
    # Set options
    options = webdriver.ChromeOptions()
    options.add_argument('--headless') # example option

    # Set desired capabilities
    caps = webdriver.DesiredCapabilities.CHROME.copy()
    caps['version'] = 'latest'
    caps['platform'] = 'Windows 10'
    caps['username'] = USERNAME
    caps['accessKey'] = ACCESS_KEY

    # Create remote webdriver object
    myDriver = webdriver.Remote(
        command_executor='https://oauth-mcarlo.rg-11d9a:b19834d6-f40b-4b6b-a347-3f8d2a5b11ba@ondemand.eu-central-1.saucelabs.com:443/wd/hub',
        options=options,
        desired_capabilities=caps
    )
    return myDriver

"""
def createDriver() -> webdriver.Chrome:
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    prefs = {"profile.managed_default_content_settings.images":2}
    chrome_options.headless = True

    chrome_options.add_experimental_option("prefs", prefs)
    #myDriver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    myDriver = webdriver.Remote(
        command_executor="http://192.168.1.10:4444/wd/hub",
        options=chrome_options
    )
    return myDriver
"""
def getGoogleHomepage(driver: webdriver.Chrome) -> str:
    driver.get("https://www.google.com")
    return driver.page_source

def doBackgroundTask(inp):
    print("Doing background task")
    print(inp.msg)
    print("Done")