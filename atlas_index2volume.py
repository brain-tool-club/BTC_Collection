import nibabel as nib
import pandas as pd
import numpy as np

# load atlas
img = nib.load('Yeo2011_7Networks_N1000.split_components.FSL_MNI152_2mm.nii.gz')
dt = img.get_fdata()

# calculate volume
##  volume number * voxel size then convert to cm^3, change lambada if you have different voxel size
roi_volume_dict = pd.Series(dt.flatten()).value_counts().map(lambda x: x*2*2*2/1000) 
del roi_volume_dict[0]
roi_volume_dict

# map the dict
output = []
for i in range(dt.shape[0]):
    layer = pd.DataFrame(dt[i])
    layer.replace(roi_volume_dict, inplace=True)
    output.append(layer.values)
output = np.array(output)

# save the output
output_img = nib.Nifti1Image(output, img.affine, img.header)
nib.save(output_img, 'atlas_volume.nii')
