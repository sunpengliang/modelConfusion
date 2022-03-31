# README #
**Program files:**

- load_txt.py: Load the file from the origin_file folder and output the file in result folder.
- merge_file.py: Merge the different models' result.
- wlf.py: The realization of weight location fusion method.
- sort.sh : Sort the txt files by frame from merge_file folder.
- senet/hgwisenet.py：The Network structure of hgwisenet.


**File folder sturcture:**

- origin_file：The original files folder, subfolders are different models result.
- merge_file: Merge and sort the file from the origin_file folder.
- reuslt: The folder which saves the result files.

# Citation
This is the official codes of the following paper.
https://doi.org/10.1145/3460426.3463654
```bibtex
@inproceedings{sun2021squeeze,
  title={Squeeze-and-Excitation network-Based Radar Object Detection With Weighted Location Fusion},
  author={Sun, Pengliang and Niu, Xuetong and Sun, Pengfei and Xu, Kele},
  booktitle={Proceedings of the 2021 International Conference on Multimedia Retrieval},
  pages={545--552},
  year={2021}
}
```

## What is this repository for? ##
Ensemble of the models.
SEnet-based rader detection model.
