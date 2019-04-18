import matplotlib.image as mpimg
import h5py

def convert(s):
    l = len(s)
    r = 5 - l
    while r > 0:
        s += '10'
        r -= 1
    return "b'{}'".format(s)


with h5py.File('digitStruct.mat', 'r') as f:
    length = len(f.get('digitStruct').get('bbox'))
    fw = open('label.txt', 'w')
    for i in range(length):
        img = mpimg.imread('./test/' + str(i + 1) + '.png')
        item = f['digitStruct']['bbox'][i].item()
        """top = 1e8
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
        mpimg.imsave('./cropped/' + str(i + 1) + '.png', img)"""

        if len(f[item]['label'].value) == 1:
            if f[item]['label'].value.item() == 10:
                fw.write(str(i + 1) + ' ' + convert(str(0)) + '\n')
            else:
                fw.write(str(i + 1) + ' ' + convert(str(int(f[item]['label'].value.item()))) + '\n')

        else:
            s = ''
            for j in range(len(f[item]['label'].value)):
                if f[f[item]['label'].value[j].item()].value[0][0] == 10:
                    s += str(0)
                else:
                  s += str(int(f[f[item]['label'].value[j].item()].value[0][0]))
            fw.write(str(i + 1) + ' ' + convert(s) + '\n')
