
import os
import numpy as np
import random
from glob import glob

from utilchiachia import get_folders_recursively, load_imgs
import optparse
import cPickle
 
# add here additional dataset classes
#datasets = {'1': MobBIOfake,
#            '2': ReplayAttack,
#            '3': BioSec,
#            '4': Warsaw,
#            '5': MaskAttack,
#            '6': LD13Biometrika,
#            '7': LD13CrossMatch,
#            '8': LD13Italdata,
#            '9': LD13Swipe,
#           }


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



def listoffiles( pathin , pathout , extension):
    """
        Retrieve dataset metadata setting labels of images contained in a 'FAKE'
        path to 0 and images contained in a 'REAL' path to 1.
        """

    print pathin

    folders = np.array(sorted(get_folders_recursively(
                       pathin,extension)))

    all_fnames = []
    all_labels = []
    train_idxs = []
    test_idxs = []

    img_idx = 0


    for folder in folders:
        fnames = sorted(glob(os.path.join(pathin, folder,
                                          '*.' + extension)))
        print folder

        for fname in fnames:

            rel_fname = str.lower(os.path.relpath(fname, pathin))

            all_fnames += [fname]
            # -- Giovani
            # all_labels += [int('live' in rel_fname)]
            all_labels += [int('real' in rel_fname)]

            if 'train' in rel_fname:
                train_idxs += [img_idx]
            else:
                if 'test' in rel_fname:
                    test_idxs += [img_idx]
                else:
                    raise ValueError('undifined image label')

            img_idx += 1
    # import pdb; pdb.set_trace()
    r_dict = {'all_fnames': np.array(all_fnames),
              'all_labels': np.array(all_labels),
              'train_idxs': train_idxs,
              'test_idxs': test_idxs,
              }

    return r_dict;


def get_optparser():

#    dataset_options = ''
#    for k in sorted(datasets.keys()):
#      dataset_options +=  ("     %s - %s \n" % (k, datasets[k].__name__))

    usage = ("usage: %prog <DATASET_PATH> <OUTPUT_PATH> <format> <nchannels> <nrows> <ncols>\n\n"
#             "DATASET is an integer corresponding to the following supported "
#             "datasets:\n" + dataset_options
            )

    parser = optparse.OptionParser(usage=usage)

    return parser


def main():
    parser = get_optparser()
    opts, args = parser.parse_args()

    if len(args) != 6:
        parser.print_help()
    else:
        dataset_path = args[0]
        output_path = args[1]
	extension = args[2]
	nchannels = int(args[3])
	nrows     = int(args[4])
	ncols     = int(args[5])
    
        r_dict = listoffiles(pathin=dataset_path ,
                             pathout=output_path ,
                             extension=extension )

        nbatches = 4
        print "loading images: %d" %r_dict['all_fnames'].shape
        data = load_imgs(r_dict['all_fnames'],(nrows,ncols),flatten=(nchannels==1), dtype='uint8')
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

        dict = { 'num_cases_per_batch' : len(r_dict['all_labels'][r_dict['train_idxs']]) / nbatches,
#                 'label_names'         : ['Spoof','Live'],
                 'label_names'         : ['FAKE','REAL'],
                 'num_vis'             : nchannels*nrows*ncols,
                 # -- Giovani
                 'data_mean'           : data[:,r_dict['train_idxs']].mean(axis=1,dtype='float32').reshape(nchannels*nrows*ncols,1)
               }

        print dict

        pickle(os.path.join(output_path,'batches.meta'),dict)



        ## for training data
        labels = r_dict['all_labels'][r_dict['train_idxs']] 
 
        # import pdb; pdb.set_trace()

        neg_idxs = np.where(labels==0)[0] 
        pos_idxs = np.where(labels==1)[0] 

        n_neg_batch = len(neg_idxs) / nbatches 
        n_pos_batch = len(pos_idxs) / nbatches 

        # -- prune samples if necessary to have equal sized splits  
        neg_idxs = neg_idxs[:n_neg_batch*nbatches] #.reshape( nbatches, -1) 
        pos_idxs = pos_idxs[:n_pos_batch*nbatches] #.reshape( nbatches, -1) 

        # randomly samples for each batch
        # neg_idxs = neg_idxs[random.sample(range(len(neg_idxs)),len(neg_idxs))].reshape(nbatches,-1)
        # pos_idxs = pos_idxs[random.sample(range(len(pos_idxs)),len(pos_idxs))].reshape(nbatches,-1)

        # -- Giovani
        neg_idxs = neg_idxs.reshape(nbatches,-1)
        pos_idxs = pos_idxs.reshape(nbatches,-1)
        rng = np.random.RandomState(42)

        for s in xrange(nbatches): 

            # -- Giovani
            # -- scramble batch samples
            batch_idxs = np.hstack((neg_idxs[s], pos_idxs[s]))
            batch_idxs = batch_idxs[rng.permutation(batch_idxs.size)]

            dict = {'data'  : data[:,batch_idxs],
                    'labels': labels[batch_idxs]
                   } 

        # dict = {'data'  : data[:,np.hstack((neg_idxs[s], pos_idxs[s]))],
        #         'labels': labels[np.hstack((neg_idxs[s], pos_idxs[s]))]
        #         } 

	    print "data/labels: {0}/{1}".format(dict['data'].shape,dict['labels'].shape)
    
            pickle(os.path.join(output_path,'data_batch_%d' % (s+1)),dict)


        ## for testing data
        labels = r_dict['all_labels'][r_dict['test_idxs']] 
 
        neg_idxs = np.where(labels==0)[0] 
        pos_idxs = np.where(labels==1)[0] 
 
        dict = {'data'  : data[:,np.hstack((neg_idxs, pos_idxs))], 
                'labels': labels[np.hstack((neg_idxs, pos_idxs))]
               } 

        print "data/labels: {0}/{1}".format(dict['data'].shape,dict['labels'].shape)
    
        pickle(os.path.join(output_path,'data_batch_%d' % (nbatches+1)),dict)


if __name__ == "__main__":
    main()
