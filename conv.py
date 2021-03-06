import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("/tmp/data/", one_hot = True)

n_classes = 10
batch_size = 128

x = tf.placeholder('float', [None,784])
y = tf.placeholder('float')

keep_rate = 0.8

def conv2d(x,W):
    return tf.nn.conv2d(x,W,strides=[1,1,1,1],padding='SAME')
def maxpool2d(x):
    return tf.nn.max_pool(x,ksize=[1,2,2,1],strides=[1,2,2,1],padding='SAME')

def conv_nn(x):
    weights={
        'W_conv1' : tf.Variable(tf.random_normal([5,5,1,32])),
        'W_conv2' : tf.Variable(tf.random_normal([5,5,32,64])),
        'W_fc' : tf.Variable(tf.random_normal([7*7*64,1024])),
        'W_out' : tf.Variable(tf.random_normal([1024,n_classes]))
        }
    bias={
        'b_conv1' : tf.Variable(tf.random_normal([32])),
        'b_conv2' : tf.Variable(tf.random_normal([64])),
        'b_fc' : tf.Variable(tf.random_normal([1024])),
        'b_out' : tf.Variable(tf.random_normal([n_classes]))
        }
    x = tf.reshape(x, shape=[-1,28,28,1])

    conv1 = tf.nn.relu(conv2d(x, weights['W_conv1']) + bias['b_conv1'])
    conv1 = maxpool2d(conv1)

    conv2 = tf.nn.relu(conv2d(conv1, weights['W_conv2']) + bias['b_conv2'])
    conv2 = maxpool2d(conv2)

    fc = tf.reshape(conv2, [-1,7*7*64])
    fc = tf.nn.relu(tf.matmul(fc, weights['W_fc']) + bias['b_fc'])
    fc = tf.nn.dropout(fc, keep_rate)

    output = tf.matmul(fc, weights['W_out']) + bias['b_out']
    return output
def train(x):
    pred = conv_nn(x)
    cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=pred, labels=y))
    optimizer = tf.train.AdamOptimizer().minimize(cost)

    epochs = 2
    with tf.Session() as sess:
        sess.run(tf.initialize_all_variables())
        for epoch in range(epochs):
            epoch_loss = 0
            for epoch in range(int(mnist.train.num_examples/batch_size)):
                epoch_x, epoch_y = mnist.train.next_batch(batch_size = 128)
                _, c = sess.run([optimizer, cost], feed_dict={x:epoch_x, y:epoch_y})
                epoch_loss += c
            print('Epoch :',epoch,'Epoch loss : ',epoch_loss,sep='   ')
        correct = tf.equal(tf.argmax(pred, 1), tf.argmax(y, 1))
        accuracy = tf.reduce_mean(tf.cast(correct, 'float'))
        print('Accuracy:',accuracy.eval({x:mnist.test.images, y:mnist.test.labels}))
train(x)
