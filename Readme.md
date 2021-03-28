**Program files:**

- load_txt.py ：load输入文件和输出
- merge_file.py: 不同模型的文件进行结果组合
- wfn.py: weight fusion的实现
- sort.sh : linux下对模型结果组合后按照frame排序



**File folder sturcture:**

- origin_file：保存不同模型的结果的文件夹
- merge_file:融合后并排序，每次运行load_txt.py后会清空
- reuslt: 保存模型融合后的文件

