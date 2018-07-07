# -*- coding: utf-8 -*-

import json

from antispoofing.cfpa.utils import *
from antispoofing.cfpa.classification.baseclassifier import BaseClassifier, metric_hter, metric_bal_accuracy
from sklearn.utils import class_weight


class FaceSpoofNet(BaseClassifier):
    """ This class implements a detector for face-based spoofing using a shallow Convolutional Neural Network (CNN).
    """

    def __init__(self, output_path, dataset,
                 input_shape=128,
                 n_channel=3,
                 epochs=150,
                 batch_size=64,
                 loss_function='categorical_crossentropy',
                 lr=0.01,
                 decay=0.0,
                 optimizer='Adadelta',
                 regularization=0.0001,
                 device_number=0,
                 force_train=False,
                 fine_tuning=False,
                 seed=42,
                 ):

        super(FaceSpoofNet, self).__init__(output_path, dataset,
                                           input_shape=input_shape,
                                           n_channel=n_channel,
                                           force_train=force_train,
                                           seed=seed,
                                           )

        self.output_path = output_path
        self.dataset = dataset
        self.force_train = force_train
        self.seed = seed

        self.input_shape = (input_shape, input_shape, n_channel)
        self.epochs = epochs
        self.batch_size = batch_size
        self.loss_function = loss_function
        self.lr = lr
        self.decay = decay
        self.optimizer = optimizer
        self.regularization = regularization
        self.device_number = device_number

        self.verbose = True
        self.model = None
        self.num_classes = 2
        self.fine_tuning = fine_tuning

    def set_gpu_configuration(self):
        """ This function is responsible for setting up which GPU will be used during the processing and some configurations related
        to GPU memory usage when the TensorFlow is used as backend.
        """

        if self.verbose:
            print('-- setting the GPU configurations', flush=True)

        if 'tensorflow' in keras.backend.backend():
            os.environ["CUDA_VISIBLE_DEVICES"] = self.device_number

            os.environ['PYTHONHASHSEED'] = '0'
            np.random.seed(self.seed)
            rn.seed(self.seed)
            tf.set_random_seed(self.seed)

            K.clear_session()
            gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.95, allow_growth=True, allocator_type='BFC')
            K.set_session(K.tf.Session(graph=tf.get_default_graph(),
                                       config=K.tf.ConfigProto(gpu_options=gpu_options,
                                                               intra_op_parallelism_threads=1,
                                                               inter_op_parallelism_threads=1,
                                                               allow_soft_placement=True,
                                                               log_device_placement=True)))

    def spoofnet(self, y):

        # -- first layer
        y = Conv2D(filters=16, kernel_size=(5, 5), strides=(1, 1), padding='same')(y)
        y = Activation('relu')(y)
        y = MaxPooling2D(pool_size=(3, 3), strides=(2, 2))(y)

        # -- second layer
        y = Conv2D(filters=64, kernel_size=(5, 5), strides=(1, 1), padding='same')(y)
        y = Activation('relu')(y)
        y = MaxPooling2D(pool_size=(3, 3), strides=(2, 2))(y)

        return y

    def architecture_definition(self):
        """
        In this method we define the architecture of our CNN.
        """

        img_input = Input(shape=self.input_shape, name='input_1')

        x = self.spoofnet(img_input)

        # -- flatten the output of the previous layer
        x = Flatten(name='flatten')(x)

        # -- classification block
        predictions = Dense(self.num_classes, activation='softmax', name='predictions',
                            kernel_regularizer=keras.regularizers.l2(self.regularization))(x)

        self.model = keras.models.Model(img_input, predictions, name='mcnn')

        # -- force using random weights
        for layer in self.model.layers[:-1]:
            layer.trainable = False

        if self.verbose:
            print(self.model.summary())

        # -- saving the CNN architecture definition in a .json file
        model_json = json.loads(self.model.to_json())
        json_fname = os.path.join(self.output_path, 'model.json')
        with open(json_fname, mode='w') as f:
            print("--saving json file:", json_fname)
            sys.stdout.flush()
            f.write(json.dumps(model_json, indent=4))

    def fit_model(self, x_train, y_train, x_validation=None, y_validation=None, class_weights=None, output_path=''):
        """ Fit a model classification.

        Args:
            x_train (numpy.ndarray): A multidimensional array containing the feature vectors (or images) to be used to train a classifier.
            y_train (numpy.ndarray): A multidimensional array containing the labels refers to the feature vectors that will be used during the training stage.
            x_validation (numpy.ndarray, optional): A multidimensional array containing the feature vectors (or images) to be used to test the classifier.
            y_validation (numpy.ndarray, optional): A multidimensional array containing the labels refers to the feature vectors that will be used for testing the classification model.
            class_weights (dict): A dictionary containig class weights for unbalanced datasets.
            output_path (str):
        """

        # -- configure the GPU that will be used
        self.set_gpu_configuration()

        # -- define the architecture
        self.architecture_definition()

        # -- choose the optimizer that will be used during the training process
        optimizer_methods = {'SGD': keras.optimizers.SGD,
                             'Adam': keras.optimizers.Adam,
                             'Adagrad': keras.optimizers.Adagrad,
                             'Adadelta': keras.optimizers.Adadelta,
                             }

        try:
            opt = optimizer_methods[self.optimizer]
        except KeyError:
            raise Exception('The optimizer %s is not being considered in this work yet:' % self.optimizer)

        # --  configure the learning process
        self.model.compile(loss=self.loss_function, optimizer=opt(lr=self.lr, decay=self.decay),
                           metrics=['accuracy',
                                    keras.metrics.categorical_crossentropy,
                                    keras.metrics.binary_crossentropy,
                                    keras.losses.categorical_hinge,
                                    metric_bal_accuracy,
                                    metric_hter,
                                    ])

        # -- normalization step
        x_train = x_train/255.

        callbacks = []

        if x_validation is None:
            validation_split = 0.0
            validation_data = None
        else:
            validation_split = 0.0
            x_validation = x_validation/255.
            validation_data = (x_validation, y_validation)

        # -- fit a model
        history = self.model.fit(x_train, y_train,
                                 batch_size=self.batch_size,
                                 epochs=self.epochs,
                                 verbose=1,
                                 callbacks=callbacks,
                                 validation_split=validation_split,
                                 validation_data=validation_data,
                                 shuffle=True,
                                 class_weight=class_weights,
                                 )


    def training(self, x_train, y_train, x_validation=None, y_validation=None, prefix=''):
        """ This method implements the training process of our CNN.

        Args:
            x_train (numpy.ndarray): Training data
            y_train (numpy.ndarray): Labels of the training data
            x_validation (numpy.ndarray, optional): Testing data. Defaults to None.
            y_validation (numpy.ndarray, optional): Labels of the testing data. Defaults to None.
            prefix (str):

        """

        output_path = os.path.join(self.output_path, prefix)
        safe_create_dir(output_path)

        output_model = os.path.join(output_path, "model.hdf5")
        output_weights = os.path.join(output_path, "weights.hdf5")

        if self.force_train or not os.path.exists(output_model) or self.fine_tuning:
            print('-- training ...', flush=True)
            print('-- training size:', x_train.shape, flush=True)

            # -- compute the class weights for unbalanced datasets
            class_weights = class_weight.compute_class_weight('balanced', np.unique(y_train), y_train)
            print('-- class_weights', class_weights, flush=True)

            # -- convert class vectors to binary class matrices.
            y_train = keras.utils.to_categorical(y_train, self.num_classes)
            print('--y_train', y_train)
            if y_validation is not None:
                y_validation = keras.utils.to_categorical(y_validation, self.num_classes)

            # -- fit the model
            self.fit_model(x_train, y_train,
                           x_validation=x_validation, y_validation=y_validation, class_weights=class_weights, output_path=output_path)

            # -- save the fitted model
            print("-- saving model", output_model)
            sys.stdout.flush()

            self.model.save(output_model)
            self.model.save_weights(output_weights)
        else:
            print('-- model already exists in', output_model)
            sys.stdout.flush()

    def testing(self, x_test, y_test, prefix=''):
        """ This method is responsible for testing the fitted model.

        Args:
            x_test (numpy.ndarray): Testing data
            y_test (numpy.ndarray): Labels of the Testing data
            prefix (str):

        Returns:
            dict: A dictionary with the ground-truth, the predicted scores and the predicted labels for the testing data, such as {'gt': y_test, 'predicted_labels': y_pred, 'predicted_scores': y_scores}

        """

        output_path = os.path.join(self.output_path, prefix)
        safe_create_dir(output_path)

        output_model = os.path.join(output_path, "model.hdf5")

        # -- configure the GPU that will be used
        self.set_gpu_configuration()

        # -- load the fitted model
        self.model = keras.models.load_model(output_model,
                                             custom_objects={'categorical_crossentropy': keras.metrics.categorical_crossentropy,
                                                             'binary_crossentropy': keras.metrics.binary_crossentropy,
                                                             'categorical_hinge': keras.losses.categorical_hinge,
                                                             'metric_bal_accuracy': metric_bal_accuracy,
                                                             'metric_hter': metric_hter,
                                                             },
                                             )

        # -- normalization step
        for i in range(len(x_test)):
            x_test[i] = x_test[i] / 255.

        # -- generates output predictions for the testing data.
        scores = self.model.predict(x_test, batch_size=self.batch_size, verbose=0)

        # -- get the predicted scores and labels for the testing data
        y_pred = np.argmax(scores, axis=1)
        y_scores = scores[:, 1]

        # -- define the output dictionary
        r_dict = {'gt': y_test,
                  'predicted_labels': y_pred,
                  'predicted_scores': y_scores,
                  }

        return r_dict
