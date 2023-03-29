from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import requests
from io import BytesIO
from PIL import Image, ImageFilter
import numpy as np
from selenium.webdriver.support import expected_conditions as EC


#Set to true when running local - testing
#set to false when running remotely - deployed (uses limited saucelab)
runOnLocal = 0

def createDriver() -> webdriver.Chrome:

    if runOnLocal:
        print("running in local")
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        prefs = {"profile.managed_default_content_settings.images":2}
        chrome_options.headless = True

        chrome_options.add_experimental_option("prefs", prefs)
        myDriver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        return myDriver

    else:
        USERNAME = 'oauth-mcarlo.rg-11d9a'
        ACCESS_KEY = 'b19834d6-f40b-4b6b-a347-3f8d2a5b11ba'
        # Set options
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # example option
        #options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

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


'''
def getGoogleHomepage(driver: webdriver.Chrome) -> str:
    driver.get("https://www.google.com")
    return driver.page_source

def doBackgroundTask(inp):
    print("Doing background task")
    print(inp.msg)
    print("Done")
'''


def open_url(driver: webdriver.Chrome,
             url: str) -> str:
    driver.implicitly_wait(10)
    driver.get(url)
    driver.maximize_window()
    get_page_source = driver.page_source
    hindi = check_Hindi(get_page_source)

    img_id = driver.find_element(By.ID, "learning-illus")
    img_element = img_id.find_element(By.XPATH, "//img[@alt='Never stop learning.']")
    img_src = img_element.get_attribute("src")
    
    '''
    img_src = driver.find_element(By.ID, "learning-illus").get_attribute("src")
    '''
    print(img_src)
    image_HD = check_image(img_src)
    if not (hindi & image_HD):
        return "Fail"

    return "Pass"


#Check if Hindi
def check_Hindi(receive_page_source:str):
    # search for the text "अपना अगला कोर्स खोजें।" in the page source
    # get the page source
    if "पाठ्यक्रम" in receive_page_source:
        print("Found hindi on the webpage!")
        return True
    else:
        print("Could not find hindi on the webpage.")
        return False

def check_image(src:str):
    #print(src)
    response = requests.get(src)
    img = Image.open(BytesIO(response.content))

    img_gray = img.convert('L')  # convert the image to grayscale
    blur_radius = 2
    img_blur = img_gray.filter(ImageFilter.GaussianBlur(blur_radius))

    blur_score = 0
    for i in range(1, 9):
        kernel = ImageFilter.Kernel((3,3), [-1,-1,-1,-1,8,-1,-1,-1,-1])
        img_lap = img_blur.filter(kernel)
        variance = np.var(np.array(img_lap))
        blur_score += variance

    blur_score *= 100
    if blur_score > 300:
        print("Image is blurry")
        return False
    else:
        print("Image is not blurry")
        return True

