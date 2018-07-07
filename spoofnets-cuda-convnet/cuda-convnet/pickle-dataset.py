
import os
import numpy as np
import random
from glob import glob

#from utilchiachia import get_folders_recursively, load_imgs - functions where inserted here
from scipy import misc
import optparse
import cPickle

# add here additional dataset classes
datasets = {'1':'MobBIOfake',
            '2':'ReplayAttack',
            '3':'BioSec',
            '4':'Warsaw',
            '5':'MaskAttack',
            '6':'LD13Biometrika',
            '7':'LD13CrossMatch',
            '8':'LD13Italdata',
            '9':'LD13Swipe',
           }

DEFAULT_IMG_TYPE = 'png'
DEFAULT_IMG_SIZE = 256

def pickle(file,dict):
    fo = open(file, 'wb')
    cPickle.dump(dict,fo)
    fo.close()


def unpickle(file):
    import cPickle
    fo = open(file, 'rb')
    dict = cPickle.load(fo)
    fo.close()
    return dict

def get_folders_recursively(path, type):
    """
    Helper function to recursively retrieve all folders containing files of
    type <type> in a given path.
    """

    folders = []

    for root, subFolders, files in os.walk(path):
        for file in files:
            if file[-len(type):] == type:
                folders += [os.path.relpath(root, path)]
                break

    return folders



def load_imgs(fnames, out_shape=None, dtype='uint8',
              flatten=True,  minmax_norm=False):

    if minmax_norm:
        assert ('float' in dtype)

    if flatten:
        n_channels = 1
    else:
        n_channels = 3

    if out_shape == None:
        # -- read first image to retrieve output shape
        out_shape = misc.imread(fnames[0], flatten).shape
        # -- check later if all images in the dataset have the same shape
        check_shape = True
    else:
        check_shape = False

    n_imgs = len(fnames)
    print "n_imgs: %d" % n_imgs
    img_set = np.empty((n_imgs,) + out_shape + (n_channels,), dtype=dtype)

    for i, fname in enumerate(fnames):

        arr = misc.imread(fname, flatten)

        if check_shape:
            assert arr.shape == out_shape
        else:
            arr = misc.imresize(arr, out_shape).astype(dtype)

        if flatten:
            arr.shape = arr.shape + (1,)

        if minmax_norm:
            arr -= arr.min()
            arr /= arr.max()

        img_set[i] = arr

    return img_set

def listoffiles(pathin, pathout, img_type):
    """
    Retrieve dataset metadata setting labels of images contained in a 'FAKE'
    path to 0 and images contained in a 'REAL' path to 1.
    """

    print pathin

    folders = np.array(sorted(get_folders_recursively(pathin, img_type)))

    all_fnames = []
    all_labels = []
    train_idxs = []
    devel_idxs = []
    test_idxs = []
    anon_idxs = []

    img_idx = 0
    for folder in folders:
        fnames = sorted(glob(os.path.join(pathin, folder, '*.%s'%(img_type))))

        for fname in fnames:

            rel_fname = str.lower(os.path.relpath(fname, pathin))

            if(('train/' in rel_fname)or('training/' in rel_fname)):
                all_fnames += [fname]
                all_labels += [int(('live' in rel_fname)or('real' in rel_fname))]
                train_idxs += [img_idx]
                img_idx += 1
            else:
                if(('test/' in rel_fname)or('testing/' in rel_fname)):
                    all_fnames += [fname]
                    all_labels += [int(('live' in rel_fname)or('real' in rel_fname))]
                    test_idxs += [img_idx]
                    img_idx += 1
                elif('devel/' in rel_fname):
                    all_fnames += [fname]
                    all_labels += [int(('live' in rel_fname)or('real' in rel_fname))]
                    devel_idxs += [img_idx]
                    img_idx += 1
                elif('anon/' in rel_fname):
                    all_fnames += [fname]
                    all_labels += [int(('live' in rel_fname)or('real' in rel_fname))]
                    anon_idxs += [img_idx]
                    img_idx += 1
                else:
                    pass


    r_dict = {'all_fnames': np.array(all_fnames),
              'all_labels': np.array(all_labels),
              'train_idxs': train_idxs,
              'devel_idxs': devel_idxs,
              'test_idxs': test_idxs,
              'anon_idxs': anon_idxs,
             }

    return r_dict;


def get_optparser():

    dataset_options = ''
    for k in sorted(datasets.keys()):
      dataset_options +=  ("     %s - %s \n" % (k, datasets[k]))

    usage = ("usage: %prog <DATASET> <DATASET_PATH> <OUTPUT_PATH> --img_type/-t <FILE TYPE> --img_size/-s <IMG SIZE>\n\n"
             "DATASET is an integer corresponding to the following supported "
             "datasets:\n" + dataset_options + "\n"
             "FILE TYPE is file type of the images to be loaded.\n"
             "IMG SIZE is shape of the output images."
            )

    parser = optparse.OptionParser(usage=usage)

    parser.add_option("--img_type", "-t",
                      default=DEFAULT_IMG_TYPE,
                      type="str",
                      metavar="STR",
                      help="[DEFAULT='%default']")

    parser.add_option("--img_size", "-s",
                      default=DEFAULT_IMG_SIZE,
                      type="int",
                      metavar="INT",
                      help="[DEFAULT='%default']")

    return parser


def main():
    parser = get_optparser()
    opts, args = parser.parse_args()

    if len(args) != 3:
        parser.print_help()
        exit(1)
    else:
        try:
            dataset = datasets[args[0]]
        except KeyError:
            raise ValueError('invalid dataset option')

        dataset_path = args[1]
        output_path = args[2]
        img_type = opts.img_type
        img_size = opts.img_size

        r_dict = listoffiles(dataset_path, output_path, img_type)

    if(not os.path.exists(output_path)):
        os.makedirs(output_path)

    nbatches = 4
    print "loading images: %d" %r_dict['all_fnames'].shape
    data = load_imgs(r_dict['all_fnames'],(img_size,img_size), dtype='uint8')
    print '{0}'.format(data.shape)
    data = np.rollaxis(data, 3, 1)
    print '{0}'.format(data.shape)
    data = data.reshape(len(data),-1)
    print '{0}'.format(data.shape)
    data = data.T
    print '{0}'.format(data.shape)
    data = np.ascontiguousarray(data)
    print '{0}'.format(data.shape)
    print "done!"

    ## for meta file
    data_mean = data[:,r_dict['all_labels'][r_dict['train_idxs']]];
    print "data_mean: {0}".format(data_mean.shape)

    labels = []
    if((dataset in 'ReplayAttack')or(dataset in 'MaskAttack')):
        labels = ['attack','real']

    elif((dataset in 'MobBIOfake')or(dataset in 'BioSec')or\
        (dataset in 'Warsaw')):
        labels = ['FAKE','REAL']

    elif((dataset in 'LD13Biometrika')or(dataset in 'LD13CrossMatch')or\
        (dataset in 'LD13Italdata')or(dataset in 'LD13Swipe')):
        labels = ['Spoof','Live']

    p_dict = {'num_cases_per_batch': len(r_dict['all_labels'][r_dict['train_idxs']]) / nbatches,
              'label_names': labels,
              'num_vis': img_size*img_size,
              'data_mean': data[:,r_dict['all_labels'][r_dict['train_idxs']]].mean(axis=1,dtype='float32').reshape(img_size*img_size,1)
             }

    print p_dict

    pickle(os.path.join(output_path,'batches.meta'),p_dict)

    ## for training data
    labels = r_dict['all_labels'][r_dict['train_idxs']] 

    neg_idxs = np.where(labels==0)[0]
    pos_idxs = np.where(labels==1)[0]

    n_neg_batch = len(neg_idxs) / nbatches
    n_pos_batch = len(pos_idxs) / nbatches

    # -- prune samples if necessary to have equal sized splits  
    neg_idxs = neg_idxs[:n_neg_batch*nbatches] #.reshape( nbatches, -1) 
    pos_idxs = pos_idxs[:n_pos_batch*nbatches] #.reshape( nbatches, -1) 

    # randomly samples for each batch
    neg_idxs = neg_idxs[random.sample(range(len(neg_idxs)),len(neg_idxs))].reshape(nbatches,-1)
    pos_idxs = pos_idxs[random.sample(range(len(pos_idxs)),len(pos_idxs))].reshape(nbatches,-1)

    for s in xrange(nbatches): 
        p_dict = {'data': data[:,np.hstack((neg_idxs[s], pos_idxs[s]))], 
                  'labels': labels[np.hstack((neg_idxs[s], pos_idxs[s]))]}

        print "data/labels: {0}/{1}".format(p_dict['data'].shape,p_dict['labels'].shape)

        pickle(os.path.join(output_path,'data_batch_%d' % (s+1)),p_dict)

    ## for testing data
    if(len(r_dict['test_idxs']) != 0):
        labels = r_dict['all_labels'][r_dict['test_idxs']] 

        neg_idxs = np.where(labels==0)[0] 
        pos_idxs = np.where(labels==1)[0] 

        p_dict = {'data': data[:,np.hstack((neg_idxs, pos_idxs))], 
                  'labels': labels[np.hstack((neg_idxs, pos_idxs))]} 

        print "data/labels: {0}/{1}".format(p_dict['data'].shape,p_dict['labels'].shape)

        nbatches += 1
        pickle(os.path.join(output_path,'data_batch_%d' % (nbatches)),p_dict)

    ## for devel data
    if(len(r_dict['devel_idxs']) != 0):
        labels = r_dict['all_labels'][r_dict['devel_idxs']] 
     
        neg_idxs = np.where(labels==0)[0] 
        pos_idxs = np.where(labels==1)[0] 

        p_dict = {'data': data[:,np.hstack((neg_idxs, pos_idxs))], 
                  'labels': labels[np.hstack((neg_idxs, pos_idxs))]} 

        print "data/labels: {0}/{1}".format(p_dict['data'].shape,p_dict['labels'].shape)

        nbatches += 1
        pickle(os.path.join(output_path,'data_batch_%d' % (nbatches)),p_dict)

    ## for anon data
    if(len(r_dict['anon_idxs']) != 0):
        labels = r_dict['all_labels'][r_dict['anon_idxs']] 
     
        neg_idxs = np.where(labels==0)[0] 
        pos_idxs = np.where(labels==1)[0] 

        p_dict = {'data': data[:,np.hstack((neg_idxs, pos_idxs))], 
                  'labels': labels[np.hstack((neg_idxs, pos_idxs))]} 

        print "data/labels: {0}/{1}".format(p_dict['data'].shape,p_dict['labels'].shape)

        nbatches += 1
        pickle(os.path.join(output_path,'data_batch_%d' % (nbatches)),p_dict)



if __name__ == "__main__":
    main()
