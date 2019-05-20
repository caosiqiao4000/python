import xlrd
import xlwt

def get_values(excel_name):

    wash = xlrd.open_workbook(excel_name)#打开Excel文件
    sheet1 = wash.sheet_by_name("Sheet1")#根据sheet名获取对应Excel值
    sheet2 = wash.sheet_by_name("Sheet2")

    # print(sheet2)#根据表单名字，获取Excel表内容。返回的是一个存放地址

    type1 = sheet1.col_values(1)[1::]    #列值，读取型号，获取型号对应的数量值
    num = sheet1.col_values(2)[1::]
    print(sheet1.cell(1,2).value, sheet1.cell(1,2))#获取某个单元格的内容
    dict1 = dict(zip(type1, num))    #to be dict
    # print(type1, dict1)

    wash_row = sheet2.nrows#获取总行数，
    # print(wash_row)# 6
    wash_list = {}

    for i in type1:
        sum1 = 0
        for j in range(1, wash_row):
            if i == sheet2.row_values(j)[0]:    #以列表形式返回当前行的内容，
                sum1 += sheet2.row_values(j)[1]
        wash_list[i] = sum1
    print(wash_list)

#定义函数打开excel并将数值做成列表

def open_excel(file_path):#这个代码，是copy的
    book_data = xlrd.open_workbook(file_path)#打开Excel文件，读取
    # a = book_data.sheets()#通过索引顺序获取
    book_sheet = book_data.sheet_by_index(0) #通过索引顺序，0-n，从0开始， 打开Excel文件的中第一个表
    rows_num = book_sheet.nrows #行数
    rows0 = book_sheet.row_values(0) #第一行的各个名称作为字典的键
    rows0_num = len(rows0) #这个可以知道有几列
    list1 = []

    for i in range(1, rows_num):
        rows_data = book_sheet.row_values(i) #取每一行的值作为列表
        rows_dir = {}
        for y in range(0, rows0_num): #将每一列的值与每一行对应起来
            rows_dir[rows0[y]] = rows_data[y]
        list1.append(rows_dir)
    return list1



if __name__ == "__main__":
    excel_name = 'test.xlsx'
    print(get_values(excel_name))
    a = open_excel(excel_name)
    print(a)