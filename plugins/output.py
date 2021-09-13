import os,time
import xlsxwriter


# -*- coding: utf-8 -*-
def write_excel():
    basedir = os.path.abspath(os.path.dirname(__file__))
    print(basedir)
    t1 = time.time()
    t1 = int(t1)
    workbook = xlsxwriter.Workbook(basedir+'\\excel\\'+str(t1)+'result.xlsx')#创建一个excel文件
    worksheet = workbook.add_worksheet(u'sheet1')#在文件中创建一个名为TEST的sheet,不加名字默认为sheet1
    worksheet.write(0, 0,'IP')
    worksheet.write(0, 1,'PORT')
    worksheet.write(0, 2,'BANNER')
    worksheet.write(0, 3,'SERVER')
    worksheet.write(0, 4,'STATUS')
    worksheet.write(0, 5,'TITLE')

    for i in range(8):
        for t in range(6):
            worksheet.write(i+1, t,t)
    workbook.close()
    print('ok')

write_excel()