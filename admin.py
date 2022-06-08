from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException, InvalidSessionIdException
import json
import time
import pandas as pd
from lxml import html
import numpy as np
import re
import os

head = '''
<!DOCTYPE html>
<html>
<head>
<!-- Required meta tags -->
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
<!-- Check Browser, as well as Hostname and set JS, CSS, Favicon path based on that-->

<!-- Favicon --><!-- cpcommit -->
<!-- <link rel="shortcut icon" type="image/x-icon" href="https://www.sec.gov/favicon.ico"> -->

<script>
	(function() {
		var hostName = window.location.hostname;

		var browserAccepted = function() {

			var ua = window.navigator.userAgent;
			var trident = ua.indexOf('Trident/'); //IE 11;
			var msie = ua.indexOf('MSIE '); // IE 10 or older
			if (msie > 0) {
				return false;
			}
			return true;
		}();

		var pathToLibs = 'https://www.sec.gov/js';
		var pathToError = '/';
		if (hostName === 'www-test.sec.gov' || hostName === 'www.sec.gov') {
			pathToLibs = 'https://www.sec.gov/ixviewer/js';
			pathToError = '/ixviewer/';
		}
		if (browserAccepted) {

			// css
			document
					.write('<link rel="stylesheet" href=' + pathToLibs + '/css/custom-bootstrap.css>');
			document
					.write('<link rel="stylesheet" href=' + pathToLibs + '/lib/fontawesome/css/all.min.css>');
			document
					.write('<link rel="stylesheet" href=' + pathToLibs + '/css/app.css>');

			// js
			document
					.write('<script type="text/javascript" src="' + pathToLibs + '/lib/jquery-3.3.1.slim.min.js"><\/script>');
			document
					.write('<script type="text/javascript" src="' + pathToLibs + '/lib/popper.min.js"><\/script>');
			document
					.write('<script type="text/javascript" src="' + pathToLibs + '/lib/bootstrap.min.js"><\/script>');
			document
					.write('<script type="text/javascript" src="' + pathToLibs + '/lib/moment.js"><\/script>');
			document
					.write('<script type="text/javascript" src="' + pathToLibs + '/lib/vanilla-picker.min.js"><\/script>');
			document
					.write('<script type="text/javascript" src="' + pathToLibs + '/lib/he.js"><\/script>');

			var date = new Date();
			var todaysDate = date.getDate() + '-' + (date.getMonth() + 1) + '-'
					+ date.getFullYear();
			document.write('<script type = "text/javascript" defer=true src="'
					+ pathToLibs + '/production.min.js?d=' + todaysDate
					+ '"><\/script>');
		} else {
			// user us on a browser that we do not support
			var currentUrl = window.location.href.split('?')[0];
			var browserError = currentUrl.substring(0, currentUrl
					.lastIndexOf('/'));
			browserError += pathToError + 'browser-error.html?url='
					+ encodeURIComponent(window.location.href);
			window.location.href = browserError;
		}
	})();
</script><link rel="stylesheet" href="https://www.sec.gov/ixviewer/js/css/custom-bootstrap.css"><link rel="stylesheet" href="https://www.sec.gov/ixviewer/js/lib/fontawesome/css/all.min.css"><link rel="stylesheet" href="https://www.sec.gov/ixviewer/js/css/app.css"><script type="text/javascript" src="https://www.sec.gov/ixviewer/js/lib/jquery-3.3.1.slim.min.js"></script><script type="text/javascript" src="https://www.sec.gov/ixviewer/js/lib/popper.min.js"></script><script type="text/javascript" src="https://www.sec.gov/ixviewer/js/lib/bootstrap.min.js"></script><script type="text/javascript" src="https://www.sec.gov/ixviewer/js/lib/moment.js"></script><script type="text/javascript" src="https://www.sec.gov/ixviewer/js/lib/vanilla-picker.min.js"></script><style>.picker_wrapper.no_alpha .picker_alpha{display:none}.picker_wrapper.no_editor .picker_editor{position:absolute;z-index:-1;opacity:0}.picker_wrapper.no_cancel .picker_cancel{display:none}.layout_default.picker_wrapper{display:-webkit-box;display:flex;-webkit-box-orient:horizontal;-webkit-box-direction:normal;flex-flow:row wrap;-webkit-box-pack:justify;justify-content:space-between;-webkit-box-align:stretch;align-items:stretch;font-size:10px;width:25em;padding:.5em}.layout_default.picker_wrapper input,.layout_default.picker_wrapper button{font-size:1rem}.layout_default.picker_wrapper>*{margin:.5em}.layout_default.picker_wrapper::before{content:'';display:block;width:100%;height:0;-webkit-box-ordinal-group:2;order:1}.layout_default .picker_slider,.layout_default .picker_selector{padding:1em}.layout_default .picker_hue{width:100%}.layout_default .picker_sl{-webkit-box-flex:1;flex:1 1 auto}.layout_default .picker_sl::before{content:'';display:block;padding-bottom:100%}.layout_default .picker_editor{-webkit-box-ordinal-group:2;order:1;width:6.5rem}.layout_default .picker_editor input{width:100%;height:100%}.layout_default .picker_sample{-webkit-box-ordinal-group:2;order:1;-webkit-box-flex:1;flex:1 1 auto}.layout_default .picker_done,.layout_default .picker_cancel{-webkit-box-ordinal-group:2;order:1}.picker_wrapper{box-sizing:border-box;background:#f2f2f2;box-shadow:0 0 0 1px silver;cursor:default;font-family:sans-serif;color:#444;pointer-events:auto}.picker_wrapper:focus{outline:none}.picker_wrapper button,.picker_wrapper input{box-sizing:border-box;border:none;box-shadow:0 0 0 1px silver;outline:none}.picker_wrapper button:focus,.picker_wrapper button:active,.picker_wrapper input:focus,.picker_wrapper input:active{box-shadow:0 0 2px 1px dodgerblue}.picker_wrapper button{padding:.4em .6em;cursor:pointer;background-color:whitesmoke;background-image:-webkit-gradient(linear, left bottom, left top, from(gainsboro), to(transparent));background-image:-webkit-linear-gradient(bottom, gainsboro, transparent);background-image:linear-gradient(0deg, gainsboro, transparent)}.picker_wrapper button:active{background-image:-webkit-gradient(linear, left bottom, left top, from(transparent), to(gainsboro));background-image:-webkit-linear-gradient(bottom, transparent, gainsboro);background-image:linear-gradient(0deg, transparent, gainsboro)}.picker_wrapper button:hover{background-color:white}.picker_selector{position:absolute;z-index:1;display:block;-webkit-transform:translate(-50%, -50%);transform:translate(-50%, -50%);border:2px solid white;border-radius:100%;box-shadow:0 0 3px 1px #67b9ff;background:currentColor;cursor:pointer}.picker_slider .picker_selector{border-radius:2px}.picker_hue{position:relative;background-image:-webkit-gradient(linear, left top, right top, from(red), color-stop(yellow), color-stop(lime), color-stop(cyan), color-stop(blue), color-stop(magenta), to(red));background-image:-webkit-linear-gradient(left, red, yellow, lime, cyan, blue, magenta, red);background-image:linear-gradient(90deg, red, yellow, lime, cyan, blue, magenta, red);box-shadow:0 0 0 1px silver}.picker_sl{position:relative;box-shadow:0 0 0 1px silver;background-image:-webkit-gradient(linear, left top, left bottom, from(white), color-stop(50%, rgba(255,255,255,0))),-webkit-gradient(linear, left bottom, left top, from(black), color-stop(50%, rgba(0,0,0,0))),-webkit-gradient(linear, left top, right top, from(gray), to(rgba(128,128,128,0)));background-image:-webkit-linear-gradient(top, white, rgba(255,255,255,0) 50%),-webkit-linear-gradient(bottom, black, rgba(0,0,0,0) 50%),-webkit-linear-gradient(left, gray, rgba(128,128,128,0));background-image:linear-gradient(180deg, white, rgba(255,255,255,0) 50%),linear-gradient(0deg, black, rgba(0,0,0,0) 50%),linear-gradient(90deg, gray, rgba(128,128,128,0))}.picker_alpha,.picker_sample{position:relative;background:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='2' height='2'%3E%3Cpath d='M1,0H0V1H2V2H1' fill='lightgrey'/%3E%3C/svg%3E") left top/contain white;box-shadow:0 0 0 1px silver}.picker_alpha .picker_selector,.picker_sample .picker_selector{background:none}.picker_editor input{font-family:monospace;padding:.2em .4em}.picker_sample::before{content:'';position:absolute;display:block;width:100%;height:100%;background:currentColor}.picker_arrow{position:absolute;z-index:-1}.picker_wrapper.popup{position:absolute;z-index:2;margin:1.5em}.picker_wrapper.popup,.picker_wrapper.popup .picker_arrow::before,.picker_wrapper.popup .picker_arrow::after{background:#f2f2f2;box-shadow:0 0 10px 1px rgba(0,0,0,0.4)}.picker_wrapper.popup .picker_arrow{width:3em;height:3em;margin:0}.picker_wrapper.popup .picker_arrow::before,.picker_wrapper.popup .picker_arrow::after{content:"";display:block;position:absolute;top:0;left:0;z-index:-99}.picker_wrapper.popup .picker_arrow::before{width:100%;height:100%;-webkit-transform:skew(45deg);transform:skew(45deg);-webkit-transform-origin:0 100%;transform-origin:0 100%}.picker_wrapper.popup .picker_arrow::after{width:150%;height:150%;box-shadow:none}.popup.popup_top{bottom:100%;left:0}.popup.popup_top .picker_arrow{bottom:0;left:0;-webkit-transform:rotate(-90deg);transform:rotate(-90deg)}.popup.popup_bottom{top:100%;left:0}.popup.popup_bottom .picker_arrow{top:0;left:0;-webkit-transform:rotate(90deg) scale(1, -1);transform:rotate(90deg) scale(1, -1)}.popup.popup_left{top:0;right:100%}.popup.popup_left .picker_arrow{top:0;right:0;-webkit-transform:scale(-1, 1);transform:scale(-1, 1)}.popup.popup_right{top:0;left:100%}.popup.popup_right .picker_arrow{top:0;left:0}</style><script type="text/javascript" src="https://www.sec.gov/ixviewer/js/lib/he.js"></script><script type="text/javascript" defer="true" src="https://www.sec.gov/ixviewer/js/production.min.js?d=20-4-2022"></script>
<title>Inline XBRL Viewer</title>
<style type="text/css" id="customized-styles"> #dynamic-xbrl-form [enabled-taxonomy="true"][continued-taxonomy="false"]{border-top:2px solid #FF6600;border-bottom:2px solid #FF6600;display:inline;} #dynamic-xbrl-form [enabled-taxonomy="true"][continued-main-taxonomy="true"]{box-shadow:-2px 0px 0px 0px #FF6600, 2px 0px 0px 0px #FF6600;} #dynamic-xbrl-form [enabled-taxonomy="true"][text-block-taxonomy="true"]{box-shadow:-2px 0px 0px 0px #FF6600, 2px 0px 0px 0px #FF6600;border-top:none;border-bottom:none;} #dynamic-xbrl-form [highlight-taxonomy="true"]{background-color:#FFD700 !important;} #dynamic-xbrl-form [highlight-taxonomy="true"] > *{background-color:#FFD700 !important;} #dynamic-xbrl-form [selected-taxonomy="true"][continued-main-taxonomy="true"]{box-shadow:-2px 0px 0px 0px #003768, 2px 0px 0px 0px #003768;} #dynamic-xbrl-form [selected-taxonomy="true"][text-block-taxonomy="true"]{box-shadow:-2px 0px 0px 0px #003768, 2px 0px 0px 0px #003768;} #dynamic-xbrl-form [selected-taxonomy="true"][continued-taxonomy="false"]{border:3px solid #003768 !important;display:inline;} #dynamic-xbrl-form [hover-taxonomy="true"]{background-color:rgba(255,0,0,0.3);} .tagged-data-example-1{border-top:2px solid #FF6600;border-bottom:2px solid #FF6600;} .search-results-example-1{background-color:#FFD700;} .tag-shading-exmple-1:hover{background-color:rgba(255,0,0,0.3);} .selected-fact-example-1{border:3px solid #003768 !important;}</style></head>
<body style="overflow:auto">
'''
body = '''
</body>
</html>'''
reader = pd.read_excel("cid.xlsx", engine='openpyxl').values.tolist()
for i in reader:
    try:
        url, path = False, False
        if not pd.isna(i[3]):
            url, path = i[3], 2020
        elif not pd.isna(i[4]):
            url, path = i[4], 2021
        if url and path:
            if not os.path.exists(f'{path}/{i[0]}.html'):
                capa = DesiredCapabilities.CHROME
                capa["pageLoadStrategy"] = "none"
                driver = webdriver.Chrome('/home/tst/Downloads/chromedriver_linux64/chromedriver', desired_capabilities=capa)
                driver.set_page_load_timeout(1)
                driver.get(url)
                time.sleep(5)
                tr = driver.find_element(By.XPATH, "//table[@class='tableFile']").find_element(By.TAG_NAME, "tbody").find_element(By.XPATH,
                                                                                                                                  "//tr//td[contains(text(), '10-K')]").find_element(
                    By.XPATH, "..")
                url = tr.find_element(By.XPATH, ".//td//a[@href]").get_attribute('href')
                driver.get(url)
                time.sleep(5)
                div = driver.find_element(By.XPATH, "//div[@id='dynamic-xbrl-form']")
                html = div.get_attribute('innerHTML')
                try:
                    none_div = div.find_element(By.XPATH, "//div[@style='display:none']")
                    html.replace(none_div.get_attribute('outerHTML'), '')
                except NoSuchElementException:
                    pass
                html = head + html + body
                open(f'{path}/{i[0]}.html', 'w').write(html)
                print("Done")
                driver.close()
    except InvalidSessionIdException as err:
        # open(f'{path}/{i[0]}.html', 'w')
        print(err.msg)
    except WebDriverException as werr:
        # open(f'{path}/{i[0]}.html', 'w')
        print(werr.msg)
    except Exception as e:
        # open(f'{path}/{i[0]}.html', 'w')
        print(e)

# data = {}
# for i in ['2020', '2021']:
#     for j in os.listdir(i):
#         symbol = j.replace('.html', '')
#         if symbol in data:
#             data[symbol] = data[symbol] + ',' + i
#         else:
#             data[symbol] = i
# print(data)
