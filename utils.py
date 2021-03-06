import torch.nn as nn
import torch

class Normalize(nn.Module):
    def __init__(self, ms = None):
        super(Normalize, self).__init__()
        if ms == None:
            self.ms = [(0.485, 0.456, 0.406), (0.229, 0.224, 0.225)]
    def forward(self, input):
        x = input.clone()
        for i in range(x.shape[1]):
            x[:,i] = (x[:,i] - self.ms[0][i]) / self.ms[1][i]
        return x

def rot(img):
    rand_angle = torch.randint(0, 4, size=(1,)).item()   # 0,1,2,3
    assert rand_angle in [0,1,2,3], 'check rand_angle'
    if rand_angle == 0:
        img = img
    elif rand_angle == 1:
        img = torch.flip(img, dims = [3]).permute(0,1,3,2)
    elif rand_angle == 2:
        img = torch.flip(img, dims = [2])
        img = torch.flip(img, dims = [3])
    elif rand_angle == 3:
        img = torch.flip(img.permute(0,1,3,2), dims=[3])
    return img

def horizontal_flip(img):
    rand_flip = torch.randint(0, 2, size=(1,)).item()  # 0,1
    assert rand_flip in [0, 1], 'check rand_flip'
    img = torch.flip(img, dims = [3])
    return img

def shuffle(img, mode):
    assert mode in [0, 1], 'check shuffle mode'
    if mode == 0:
        patch_0 = img[:, 0:112,0:112]
        patch_1 = img[:, 0:112,112:224]
        patch_2 = img[:, 112:224, 0:112]
        patch_3 = img[:, 112:224, 112:224]
        rand_ind = torch.randperm(4)
        img_0 = torch.cat((eval('patch_{}'.format(rand_ind[0])),
                         eval('patch_{}'.format(rand_ind[1]))),dim=2)
        img_1 = torch.cat((eval('patch_{}'.format(rand_ind[2])),
                         eval('patch_{}'.format(rand_ind[3]))),dim=2)
        return torch.cat((img_0, img_1), dim=1)
    else:
        # four possibilities, for easy training
        img = img.permute(1, 2, 0)
        img = img.reshape(2, 112, 224, 3)
        rand_shuffle_1 = torch.randint(0, 2, size=(1,)).item()
        img = img[[rand_shuffle_1, 1 - rand_shuffle_1]]
        img = img.reshape(224, 224, 3)
        img = img.permute(1, 0, 2)
        img = img.reshape(2, 112, 224, 3)
        rand_shuffle_2 = torch.randint(0, 2, size=(1,)).item()
        img = img[[rand_shuffle_2, 1 - rand_shuffle_2]]
        img = img.reshape(224, 224, 3)
        return img.permute(2, 1, 0)


def aug(img_input):
    for img_ind in range(img_input.shape[0]):
        img_input[img_ind:img_ind + 1] = horizontal_flip(img_input[img_ind:img_ind + 1])
    return img_input

def mk_proto_ls(n_imgs):
    tar_ind_ls = torch.tensor(list(range(int(2 * n_imgs)))).reshape((2, n_imgs)).permute((1, 0)).reshape(-1)
    tar_ind_ls_ex = []
    for i_f in list(range(n_imgs)):
        for i_s in list(range(n_imgs, n_imgs * 2)):
            if i_f != i_s - n_imgs:
                tar_ind_ls_ex.append([i_f, i_s])
    tar_ind_ls_ex = torch.tensor(tar_ind_ls_ex)[torch.randperm(len(tar_ind_ls_ex))].reshape(-1)
    tar_ind_ls = torch.cat((tar_ind_ls, tar_ind_ls_ex))
    return tar_ind_ls