# Vegetation-Segmentation
This repository shows the utilization of U-Net architecture to perform vegetation segmentation from street-view images of the IDD. The following videos and images show an implementation of the model.

The architecture of the model is drawn using the visualkeras module.
![u_net_arch_3d](https://github.com/Shirish2004/Vegetation-Segmentation/assets/91938605/1569fea6-411e-4e2f-919e-d9089b9c073f)
### U-Net architecture Layered View 3D
![u_net_arch_2d](https://github.com/Shirish2004/Vegetation-Segmentation/assets/91938605/6bfed136-ec9d-47d0-adc1-81ca4a956353)
### U-Net architecture Layered View 2D
![Screenshot 2023-10-03 085414](https://github.com/Shirish2004/Vegetation-Segmentation/assets/91938605/b9f37233-ae17-4e19-8abb-f1e936a01122)
![Screenshot 2023-10-03 085432](https://github.com/Shirish2004/Vegetation-Segmentation/assets/91938605/6d7a6036-e8dd-47a3-9038-59bc66592d66)
![Screenshot 2023-10-03 085444](https://github.com/Shirish2004/Vegetation-Segmentation/assets/91938605/af1fd70d-a505-4cc7-94c0-dcbcffa2789a)
![Screenshot 2023-10-03 085527](https://github.com/Shirish2004/Vegetation-Segmentation/assets/91938605/4cf4931a-ec3f-4692-889d-cfcbf0f83972)
![Screenshot 2023-10-03 085542](https://github.com/Shirish2004/Vegetation-Segmentation/assets/91938605/bac1508d-f725-4f89-b56b-7081b346026d)

# Dataset
The dataset has been adapted from the IDD-Segmentation, and to prepare one of your own, you could follow the comments mentioned in the scripts or carry your work with stored arrays. One can also work with the dataset specifically required for a similar task by cloning this repository and starting their work with the vegetation dataset.

# Notebooks 
There are different notebooks in this repository. For organization and EDA-related purposes, please have a look at the seg.ipynb file, and for further organization and model building, please follow tf_seg.ipynb.

# Results and inference
the real_time_inference_sematic_seg.py script shows the implementation of the model in real-time mode. The following video is an example.
https://github.com/Shirish2004/Vegetation-Segmentation/assets/91938605/e4c61596-e3da-48b6-8db2-588901a3a48c
