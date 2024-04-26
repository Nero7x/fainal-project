import tensorflow as tf
from keras.utils import pad_sequences
import numpy as np

class RelationshipFinder:

    def transform_input_text(self, texts):
        temp = []
        for line in texts:
            x = []
            for word in line.lower().split(' '):
                wid = 1
                if word in self.input_word2idx:
                    wid = self.input_word2idx[word]
                x.append(wid)
                if len(x) >= self.max_input_seq_length:
                    break
            temp.append(x)
        temp = pad_sequences(temp, maxlen=self.max_input_seq_length)

        print(temp.shape)
        return temp
    


    def split_target_text(self, texts):
        temp = []
        for line in texts:
            x = []
            line2 = 'START ' + line.lower() + ' END'
            for word in line2.split(' '):
                x.append(word)
                if len(x) + 1 > self.max_target_seq_length:
                    x.append('END')
                    break
            temp.append(x)
        return temp
    

    def generate_batch(self, x_samples, y_samples, batch_size):
        encoder_input_data_batch = []
        decoder_input_data_batch = []
        decoder_target_data_batch = []
        line_idx = 0
        while True:
            for recordIdx in range(0, len(x_samples)):
                target_words = y_samples[recordIdx]
                x = x_samples[recordIdx]
                decoder_input_line = []
            
                for idx in range(0, len(target_words)-1):
                    w2idx = 0
                    w = target_words[idx]
                    if w in self.target_word2idx:
                        w2idx = self.target_word2idx[w]
                    decoder_input_line += [w2idx]
                    decoder_target_label = np.zeros((self.num_target_tokens,))
                
                    w2idx_next= 0
                    if target_words[idx+1] in self.target_word2idx:
                        w2idx_next= self.target_word2idx[target_words[idx+1]]
                    
                    decoder_target_label[w2idx_next] = 1
                
                    decoder_input_data_batch.append(decoder_input_line)
                    encoder_input_data_batch.append(x)
                    decoder_target_data_batch.append(decoder_target_label)
                
                line_idx += 1
            
                if line_idx >= batch_size:
                    yield (pad_sequences(encoder_input_data_batch, self.max_input_seq_length),
                            pad_sequences(decoder_input_data_batch,RecursiveRNNv22.MAX_DECODER_SEQ_LENGTH), np.array(decoder_target_data_batch))
                    line_idx= 0
                    encoder_input_data_batch= []
                    decoder_input_data_batch= []
                    decoder_target_data_batch= []


    def conv_maxpool(inputs, filter_sizes, embedding_size, num_filters, seq_max_length):
        pooled_outputs = []
        for i, filter_size in enumerate(filter_sizes):
            with tf.variable_scope("conv-maxpool-%s" % filter_size):
                # Convolution
                filter_shape = [filter_size, embedding_size, 1, num_filters]
                W = tf.get_variable("weights", filter_shape,
                                    initializer=tf.truncated_normal_initializer(stddev=0.1))
                b = tf.get_variable("biases", [num_filters], initializer=tf.constant_initializer(0.0))

                conv = tf.nn.conv2d(inputs,
                                W,
                                strides=[1, 1, 1, 1],
                                padding='VALID',
                                name='conv')

                # Activation function
                h = tf.nn.relu(tf.nn.bias_add(conv, b), name='relu')

                # Maxpool
                pooled = tf.nn.max_pool(h,
                                    ksize=[1, seq_max_length - filter_size + 1 , 1 , 1],
                                    strides=[1 , 1 , 1 , 1],
                                    padding='VALID',
                                    name='pool')
            
                pooled_outputs.append(pooled)
    
        return pooled_outputs
    

    def my_function(inputs, num_filters_total, num_classes, l2_reg_lambda, input_y):
        with tf.name_scope('softmax'):
            softmax_w = tf.Variable(tf.truncated_normal([num_filters_total, num_classes], stddev=0.1), name='softmax_w')
            softmax_b = tf.Variable(tf.constant(0.1, shape=[num_classes]), name='softmax_b')

        # Add L2 regularization to output layer
        l2_loss = tf.nn.l2_loss(softmax_w)
        l2_loss += tf.nn.l2_loss(softmax_b)

        scores = tf.matmul(inputs, softmax_w) + softmax_b
        predictions = tf.argmax(scores, 1, name='predictions')

        # Loss
        with tf.name_scope('loss'):
            losses = tf.nn.softmax_cross_entropy_with_logits(labels=input_y, logits=scores)
            # Add L2 losses
            loss = tf.reduce_mean(losses) + l2_reg_lambda * l2_loss

        # Accuracy
        with tf.name_scope('accuracy'):
            correct_predictions = tf.equal(predictions, tf.argmax(input_y, 1))
            accuracy = tf.reduce_mean(tf.cast(correct_predictions, 'float'), name='accuracy')
    
        return predictions, loss, accuracy
