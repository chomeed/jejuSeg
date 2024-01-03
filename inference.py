from mmseg.apis import init_model, inference_model,show_result_pyplot

config_path = 'mmsegmentation/configs/_ours_/segformer-b0_500_jeju.py'
checkpoint_path = 'mmsegmentation/experiments/iter_500.pth'
img_path = 'LC_JJ_AP25_33606070_001_2019_FGT_1024.tiff'


model = init_model(config_path, checkpoint=checkpoint_path, device='cpu')
result = inference_model(model, img_path)
print(result)
print(result.pred_sem_seg.data.shape)
# vis_iamge = show_result_pyplot(model, img_path, result, out_file='result.png')

new_image = result.pred_sem_seg.data[0]

import numpy as np 
import cv2 

# mask = np.zeros(result.pred_sem_seg.data.shape,np.uint8)
# cv2.drawContours(mask,[cnt],0,255,-1)
# pixelpoints = np.transpose(np.nonzero(mask))

contours, hierarchy = cv2.findContours(result.pred_sem_seg.data[0].numpy().astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
print(len(contours), type(contours), hierarchy)
print(np.concatenate(contours).reshape(-1, 2)[:, 0])
# largest_contour = max(contours, key=cv2.contourArea)

# cv2.drawContours(new_image, contours, -1, (0, 255, 0), 2) 
# cv2.drawContours(new_image, largest_contour, -1, (0, 0, 255), 2)

import matplotlib.pyplot as plt

plt.imshow(new_image, cmap='gray')
plt.scatter(np.concatenate(contours).reshape(-1, 2)[:, 0], np.concatenate(contours).reshape(-1, 2)[:, 1], s=2)
plt.show()