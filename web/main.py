from app import *
import xlsxwriter
import urllib.request
import shutil,os
import os.path
from os import path




def main():
    # Create an new Excel file and add a worksheet.
    workbook = xlsxwriter.Workbook('scrape_data.xlsx')
    worksheet = workbook.add_worksheet()  
    raw_html = simple_get('http://www.agriculture.gov.au/pests-diseases-weeds/plant#identify-pests-diseases')
    html = BeautifulSoup(raw_html, 'html.parser')
    x = html.find('ul', id='zz3_RootAspMenu' )
    h = x.find_all('li')
    if path.exists('pic'):
        shutil.rmtree('pic')
    os.mkdir('pic')
    row = col = j = 0
    title = ['name', 'image_url', 'origin', 'Secure any suspect specimens', 'See if you can identify the pest']
    for j, t in enumerate(title):
        worksheet.write(row + 1, col + j, t)

    for i in range(71 , 92):
        data = h[i]
        output = scrape_data(data)
        worksheet.write(i-70+1, 0, output['name'])
        worksheet.write(i-70+1, 1, output['image_url'])
        worksheet.write(i-70+1, 2, output['origin'])
        worksheet.write(i-70+1, 3, output['suspect_specimen'])
        # worksheet.write(i-70+1, 4, output['ae'])
        worksheet.write(i-70+1, 4, output['identify'])
        if output['image_url'] != 'error':
            urllib.request.urlretrieve("http://www.agriculture.gov.au" + str(output['image_url']), "./pic/pic"+str(i-70)+".jpg")
            worksheet.insert_image(i-70+1, 5, './pic/pic'+str(i-70)+'.jpg')
    workbook.close()

