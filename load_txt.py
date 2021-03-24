import os

root_path = os.getcwd()
data_folder_path = os.path.join(root_path, 'merge_file')

print(data_folder_path)

##加载txt模型
def load_txtfile(data_folder_path):
    sorted(os.listdir(data_folder_path))
    for file in os.listdir(data_folder_path):
        file_path = os.path.join(data_folder_path,file)
        # output = open(file_path,'a+')
        max_frame = int(get_max_frame(file_path))
        for cur in range(max_frame+1):
            r,a,class_type,conf = get_single_frame(cur,file_path)
            print('success')
            #r,a = function(r,a)
            # for i in range(len(r)+1):
            #     output.write(cur,r[i],a[i],class_type[i],conf[i])






def get_single_frame(cur,file):
    r = []
    a = []
    class_type = []
    conf = []

    fileHandler = open(file, "r")
    line = fileHandler.readline()
    cur_frame = int(line.split(" ")[0])
    while(cur == cur_frame):
        r.append(line.split(" ")[1])
        a.append(line.split(" ")[2])
        class_type.append(line.split(" ")[3])
        conf.append(line.split(" ")[4])
        removeline(line,file)
        try:
            line = fileHandler.readline()
            cur_frame = int(line.split(" ")[0])
        except:
            pass
            break
    return r,a,class_type,conf

#从txt文件中获取最大的frame
def get_max_frame(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()  # 读取所有行
        first_line = lines[0]  # 取第一行
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