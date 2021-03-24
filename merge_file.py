import os

root_path = os.getcwd()
data_folder_path = os.path.join(root_path, 'origin_file')

data_saved_path = os.path.join(root_path,"merge_file")
data_sort_path = os.path.join(root_path,"sort_file")
print(data_saved_path)

if not os.path.exists(data_saved_path):
    os.makedirs(data_saved_path)

if not os.path.exists(data_sort_path):
    os.makedirs(data_sort_path)

#merge the same file from different folders
def mergeFile(data_folder_path,data_saved_path):
    sorted(os.listdir(data_folder_path))
    for data_folder in os.listdir(data_folder_path):
        sub_folder_path = os.path.join(data_folder_path,data_folder)
        print(sub_folder_path)
        sorted(os.listdir(sub_folder_path))
        for file in os.listdir(sub_folder_path):
            file_path = os.path.join(sub_folder_path,file)
            print(file_path)
            output_path = os.path.join(data_saved_path,file)
            output = open(output_path, 'a+')
            for line in open(file_path):
                output.writelines(line)
            #output.write('\n')
            output.close();


#暂时不用，利用Linux的sort函数来按照frame来排序
def sort_file(data_saved_path,data_sort_path):
    for file in os.listdir(data_saved_path):
        print(file)
        file_path = os.path.join(data_saved_path, file)
        print(file_path)
        list = []
        with open(file_path, 'r') as f:
            for line in f:
                list.append(line.strip())
        print(list)
        sort_file = os.path.join(data_sort_path,file)
        with open(sort_file, "w") as f:
            for item in sorted(list):
                f.writelines(item)
                f.writelines('\n')
            f.close()


mergeFile(data_folder_path,data_saved_path)
