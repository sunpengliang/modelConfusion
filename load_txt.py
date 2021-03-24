import os
import numpy as np

from wfn import weighted

root_path = os.getcwd()
data_folder_path = os.path.join(root_path, 'merge_file')

print(data_folder_path)

##加载txt模型
def load_txtfile(data_folder_path):
    sorted(os.listdir(data_folder_path))
    output_path = os.path.join(root_path, 'result')
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    for file in os.listdir(data_folder_path):
        file_path = os.path.join(data_folder_path,file)
        print(file_path)
        result_path = os.path.join(output_path, file)
        output = open(result_path,'a+')
        max_frame = int(get_max_frame(file_path))
        print(max_frame)
        for cur in range(max_frame+1):
            r,a,classes,conf = get_single_frame(cur,file_path)
            car,ped,cyc = weighted(r,a,conf,classes)
            total_result = []
            if(len(car) != 0):
                total_result+=car
            if (len(ped) != 0):
                total_result+=ped
            if (len(cyc) != 0):
                total_result+=cyc
            #total_result = np.array(total_result)
            total_result.sort(key=lambda x: x[2])

            len_l = len(total_result)
            if(len_l != 0):
                total_result = total_result[::-1]
                for i in range(len_l):
                    output.write("%d %f %f %s %f\n" % (cur,total_result[i][0],total_result[i][1],total_result[i][3],total_result[i][2]))
        output.close()






def get_single_frame(cur,file):
    r = []
    a = []
    classes = []
    conf = []

    fileHandler = open(file, "r")
    line = fileHandler.readline()
    cur_frame = int(line.split(" ")[0])
    while(cur == cur_frame):
        r.append(float(line.split(" ")[1]))
        a.append(float(line.split(" ")[2]))
        classes.append(line.split(" ")[3])
        conf.append(float(line.split(" ")[4]))
        removeline(line,file)
        try:
            line = fileHandler.readline()
            cur_frame = int(line.split(" ")[0])
        except:
            pass
            break
    return r,a,classes,conf

#从txt文件中获取最大的frame
def get_max_frame(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()  # 读取所有行
        #first_line = lines[0]  # 取第一行
        last_line = lines[-1]  # 取最后一行 print '文件' + fname + '第一行为：' + first_line print '文件' + fname + '最后一行为：'+ last_line
        max_frame = last_line.split(' ')[0]
    return max_frame

#去除特定行，暂时没有特别好的办法，就是重写
def removeline(line,file):
    with open(file, 'r') as r:
      lines = r.readlines()
      with open(file, 'w') as w:
         for l in lines:
             if l != line:
                w.write(l)


load_txtfile(data_folder_path)