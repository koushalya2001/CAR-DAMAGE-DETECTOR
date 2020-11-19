from flask import Flask,jsonify,request
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import os
import time
def getReviewstwo(zone):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("enable-automation")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    search = "car service center {}".format(zone) 
    url =f"https://www.google.com/search?q={search}"
    names,addresses,phones,userstars,openstatuses=[],[],[],[],[]
    driver.get(url)
    wait = WebDriverWait(driver, 10) 
    menu_bt = wait.until(EC.element_to_be_clickable( (By.XPATH, '//div[@class="hdtb-mitem hdtb-imb"]//a')) )
    menu_bt.click()
    recent_rating_bt = driver.find_elements_by_xpath('//div[@class="section-result-text-content"]')
    nametrial=[]
    name=driver.find_elements_by_xpath('//div[@class="section-result-text-content"]//h3[@class="section-result-title"]//span')
    address=driver.find_elements_by_xpath('//div[@class="section-result-text-content"]//span[@class="section-result-location"]')
    phone=driver.find_elements_by_xpath('//div[@class="section-result-text-content"]//span[@class="section-result-info section-result-phone-number"]//span')
    userstar=driver.find_elements_by_xpath('//div[@class="section-result-text-content"]//span[@class="cards-rating-score"]')
    openstatus=driver.find_elements_by_xpath('//div[@class="section-result-hours-phone-container"]//span[@class="section-result-info section-result-closed" and not(contains(@style, "display:none"))]//span[1] | //div[@class="section-result-hours-phone-container"]//span[@class="section-result-info section-result-opening-hours" and not(contains(@style, "display:none"))]//span[1]')
    time.sleep(3)
    for f, b in zip(name, address):
        names.append(f.text)
        addresses.append(b.text)
    
    for p in phone:
        phones.append(p.text)
    for q in openstatus:
        if q.text==".":
        	openstatuses.append(" ")  
        	print(q.text)
        else:
           print(q.text)    
           openstatuses.append(q.text)
    for r in userstar :
        userstars.append(r.text) 
    score_titles = [{"name": t, "address": s,"phone":u,"rating":v,"status":w} for t, s, u, v, w in zip(names,addresses,phones,userstars,openstatuses)] 
    shops=json.dumps(score_titles)
    print(shops)
    userstars.clear()
    openstatuses.clear()
    phones.clear()
    names.clear()
    addresses.clear()
    userstar.clear()
    openstatus.clear()
    phone.clear()
    name.clear()
    address.clear()
    driver.quit()
    return shops
app = Flask(__name__)
@app.route("/damagedetails/<string:zone>")
def get(zone):
    assert zone==request.view_args['zone']
    review=getReviewstwo(zone)
    print(review)
    return jsonify({"area":review})


if __name__== "__main__":
    app.run(host='0.0.0.0',port=8080)
    
