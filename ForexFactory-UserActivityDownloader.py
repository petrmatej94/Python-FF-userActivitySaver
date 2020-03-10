from selenium import webdriver
import time
import urllib.request
import os


directory = r"*****\PythonForexFactoryDownloader"

options = webdriver.ChromeOptions()
options.add_argument("headless")

browser = webdriver.Chrome(executable_path='chromedriver.exe', chrome_options=options)
browser2 = webdriver.Chrome(executable_path='chromedriver.exe', chrome_options=options)

browser.get("https://www.forexfactory.com/<username>")
time.sleep(2)

nav = browser.find_element_by_class_name("member_activity__table")
urls = nav.find_elements_by_tag_name('a')


current_files = os.listdir(directory + "\pages")

for url in urls:
    address = url.get_attribute('href')
    if 'post' in address or 'attachment' in address:
        if 'post' in address:
            file_name = "%s.html" % address.split('#')[1]
        elif 'attachment' in address:
            file_name = "%s.png" % address.split('?')[1]
        else:
            continue

        if file_name not in current_files:
            browser2.get(address)
            html = str(browser2.page_source)
	    
	    # Bypass web protection against saving web page
            html = html.replace("<script", "").replace("</script>", "")

            file_name = "%s\pages\%s" % (directory, file_name)

            if '.html' in file_name:
                with open(file_name, "w", encoding="utf-8") as f:
                    f.write(html)
                    print("Wrote %s" % file_name)

            if '.png' in file_name:
                urllib.request.urlretrieve(address, file_name)

browser.quit()
browser2.quit()


