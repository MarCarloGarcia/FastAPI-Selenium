from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
from extract import *
import os


SECRET = os.getenv("SECRET")

#
app = FastAPI(
    title="Coding Allstars Developer Trial Task"
)

class Msg(BaseModel):
    msg: str
    secret: str


@app.get("/")

async def root():
    return {"message":"go to /docs"}

'''
@app.get("/homepage")
async def demo_get():
    driver = createDriver()
    homepage = getGoogleHomepage(driver)
    driver.close()
    return homepage


@app.post("/backgroundDemo")
async def demo_post(inp: Msg, background_tasks: BackgroundTasks):
    
    background_tasks.add_task(doBackgroundTask, inp)
    return {"message": "Success, background task started"}
'''



@app.get("/get_url")
async def get_url(q: str):
    driver = createDriver()
    url = q
    homepage = open_url(driver, url)
    driver.close()
    print(homepage)
    return homepage
