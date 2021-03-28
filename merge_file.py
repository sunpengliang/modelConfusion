import os

root_path = os.getcwd()
data_folder_path = os.path.join(root_path, 'original_file')

data_saved_path = os.path.join(root_path,"merge_file")
print(data_saved_path)

if not os.path.exists(data_saved_path):
    os.makedirs(data_saved_path)

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
            output.close();

mergeFile(data_folder_path,data_saved_path)
