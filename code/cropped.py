import matplotlib.image as mpimg
import h5py

with h5py.File('digitStruct.mat', 'r') as f:
    length = len(f.get('digitStruct').get('bbox'))
    for i in range(length):
        img = mpimg.imread('./test/' + str(i + 1) + '.png')
        item = f['digitStruct']['bbox'][i].item()
        top = 1e8
        left = 1e8
        bottom = 0
        right = 0
        if len(f[item]['top'].value) == 1:
            top = min(f[item]['top'].value.item(), top)
            left = min(f[item]['left'].value.item(), left)
            bottom = max(f[item]['top'].value.item() + f[item]['height'].value.item(), bottom)
            right = max(f[item]['left'].value.item() + f[item]['width'].value.item(), right)
        else:
            for j in range(len(f[item]['top'].value)):
                top = min(f[f[item]['top'].value[j].item()].value[0][0], top)
                left = min(f[f[item]['left'].value[j].item()].value[0][0], left)
                bottom = max(f[f[item]['top'].value[j].item()].value[0][0] + f[f[item]['height'].value[j].item()].value[0][0], bottom)
                right = max(f[f[item]['left'].value[j].item()].value[0][0] + f[f[item]['width'].value[j].item()].value[0][0], right)
        top = max(top, -1)
        left = max(left, -1)
        img = img[int(top + 1):int(bottom), int(left + 1):int(right), :]
        mpimg.imsave('./cropped/' + str(i + 1) + '.png', img)
