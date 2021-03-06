# import required libraries
import numpy as np
import function2 as functionx

# IMPORTANT: change if approximating a different function
# the function we are approximating
func = "function2"

# how many nodes in each layer
nodes_in_input_layer = functionx.input_nodes
nodes_in_hidden_layer1 = functionx.hidden1_nodes
nodes_in_hidden_layer2 = functionx.hidden2_nodes
nodes_in_output_layer = functionx.output_nodes

# whether or not the ANN should read in data
read_in_data = True

# whether or not the ANN should train
train = True

# whether or not the ANN should save data
save = True

# whether or not the ANN should display the weights and biases
display = True

# whether or not the ANN should test itself
test = True

# how many epochs the program should do
num_epochs = 200000

# how often the program should tell the user its progress
# (measured in epochs)
progress_rate = 10000

# the learning rate
lr = 0.025

# getting the input features from the .csv file
input_features = np.loadtxt(func + '/' + func + '_inputs.csv', delimiter=',', ndmin=functionx.input_array_dim)
input_features = input_features.reshape(functionx.input_array_r, functionx.input_array_c)

# getting the target outputs from the .csv file
target_output = np.loadtxt(func + '/' + func + '_desired_outputs.csv', delimiter=',', ndmin=functionx.output_array_dim)
target_output = target_output.reshape(functionx.output_array_r, functionx.output_array_c)

# setting up the weights and biases
# reading in the weights and biases
if read_in_data:
    dim = 0
    if (nodes_in_input_layer * nodes_in_hidden_layer1) > 1:
        dim = 2
    else:
        dim = 1
    weight_hidden1 = np.loadtxt(func + '/' + 'weight_hidden1.csv', delimiter=',', ndmin=dim)
    if (nodes_in_hidden_layer1 * nodes_in_hidden_layer2) > 1:
        dim = 2
    else:
        dim = 1
    weight_hidden2 = np.loadtxt(func + '/' + 'weight_hidden2.csv', delimiter=',', ndmin=dim)
    if (nodes_in_hidden_layer2 * nodes_in_output_layer) > 1:
        dim = 2
    else:
        dim = 1
    weight_output = np.loadtxt(func + '/' + 'weight_output.csv', delimiter=',', ndmin=dim)
    bias1 = np.loadtxt(func + '/' + 'bias1.csv', delimiter=',', ndmin=1)
    bias2 = np.loadtxt(func + '/' + 'bias2.csv', delimiter=',', ndmin=1)
    bias_op = np.loadtxt(func + '/' + 'bias_op.csv', delimiter=',', ndmin=1)
else:
    # randomly assigning the weights and biases in we are not
    # supposed to read them in from the .csv files
    weight_hidden1 = np.random.rand(nodes_in_input_layer, nodes_in_hidden_layer1)
    weight_hidden2 = np.random.rand(nodes_in_hidden_layer1, nodes_in_hidden_layer2)
    weight_output = np.random.rand(nodes_in_hidden_layer2, nodes_in_output_layer)
    bias1 = np.random.rand(nodes_in_hidden_layer1)
    bias2 = np.random.rand(nodes_in_hidden_layer2)
    bias_op = np.random.rand(nodes_in_output_layer)


# to normalize the input and output data
def normalize(input_arr, output_arr):
    input_arr = (input_arr - functionx.input_normalization_min) / (functionx.input_normalization_max - functionx.input_normalization_min)
    output_arr = (output_arr - functionx.output_normalization_min) / (functionx.output_normalization_max - functionx.output_normalization_min)


# do the actual normalization
normalize(input_features, target_output)


# the sigmoid function
def sigmoid(x):
    return 1 / (1 + np.exp(-x))


# the derivative of the sigmoid function
def sigmoid_der(x):
    return sigmoid(x) * (1 - sigmoid(x))


# forward propagation
def forward_prop(arr):
    # normalize the input values
    arr = (arr - functionx.input_normalization_min) / (functionx.input_normalization_max - functionx.input_normalization_min)
    # predicting for the values
    # taking the inputs
    single_point = np.array(arr)
    # first step
    result1 = np.dot(single_point, weight_hidden1) + bias1
    # second step
    result2 = sigmoid(result1)
    # third step
    result3 = np.dot(result2, weight_hidden2) + bias2
    # fourth step
    result4 = sigmoid(result3)
    # fifth step
    result5 = np.dot(result4, weight_output) + bias_op
    # sixth step
    result6 = sigmoid(result5)
    # denormalize everything after the calculations have been done
    single_point = (single_point * (functionx.input_normalization_max - functionx.input_normalization_min)) + functionx.input_normalization_min
    result6 = (result6 * (functionx.output_normalization_max - functionx.output_normalization_min)) + functionx.output_normalization_min
    # print the final result
    print("inputs:")
    print(single_point)
    print("outputs:")
    print(result6)


# backpropagation
if train:
    for epoch in range(num_epochs):
        # multiply the input for the ANN matrix with the weights between
        # the input and hidden layer1 matrices to get the input for the
        # hidden layer1
        input_hidden1 = np.dot(input_features, weight_hidden1) + bias1

        # get the output of the hidden layer1
        # (which is just the sigmoid of the input to the hidden layer1)
        output_hidden1 = sigmoid(input_hidden1)

        # multiply the output of the hidden layer1 (which is the input for
        # the hidden layer2) with the weights between the hidden layer1 and
        # hidden layer2 to get the input for the hidden layer2
        input_hidden2 = np.dot(output_hidden1, weight_hidden2) + bias2

        # get the output of the hidden layer2
        # (which is just the sigmoid of the input to the hidden layer2)
        output_hidden2 = sigmoid(input_hidden2)

        # multiply the output of the hidden layer2 (which is the input for
        # the output layer) with the weights between the hidden layer2 and
        # output layer to get the input for the output layer
        input_op = np.dot(output_hidden2, weight_output) + bias_op

        # get the output of the output layer
        # (which is just the sigmoid of the input to the output layer)
        output_op = sigmoid(input_op)

        if epoch % progress_rate == 0:
            # calculate the mean squared error and display it to the user
            # along with which epoch the program is on
            error_out = ((1 / 2) * (np.power((output_op - target_output), 2)))
            print("epoch =")
            print(epoch)
            print("error =")
            print(error_out.sum())

        # derivatives for the output layer
        derror_douto = output_op - target_output
        douto_dino = sigmoid_der(input_op)
        # the derivative that will be used to calculate gradient descent
        # for the bias and for the output layer
        deriv_op = derror_douto * douto_dino
        dino_dwo = output_hidden2
        # put all the derivatives together for derror/dwo (which is needed
        # for gradient descent)
        # we have to transpose the dino/dwo to make it compatible with the
        # other matrices
        derror_dwo = np.dot(dino_dwo.T, deriv_op)

        # derivatives for the hidden layer2
        # derror/douto and douto/dino have been defined above
        derror_dino2 = derror_douto * douto_dino
        dino_douth2 = weight_output
        # combine the two previous derivatives into derror/douth1
        # we have to transpose the dino/douth2 to make it compatible with
        # the other matrix
        derror_douth2 = np.dot(derror_dino2, dino_douth2.T)
        douth_dinh2 = sigmoid_der(input_hidden2)
        dinh_dwh2 = input_hidden1
        # separating out calculations to make gradient descent for the
        # bias easier
        deriv2 = douth_dinh2 * derror_douth2
        # combine all the previous derivatives into derror/dwh2
        # we have to transpose the dinh/dwh2 to make it compatible with the
        # other matrix
        derror_dwh2 = np.dot(dinh_dwh2.T, deriv2)

        # derivatives for the hidden layer1
        # derror/dino2 and douto/douth2 have been defined above
        # dino/douth2 needs to be transposed to make it a compatible matrix
        # derror_dino1 = derror_dino2 * dino_douth2.T
        derror_dino1 = np.dot(derror_dino2, dino_douth2.T)
        dino_douth1 = weight_hidden2
        # combine the two previous derivatives into derror/douth2
        # we have to transpose the dino/douth1 to make it compatible with
        # the other matrix
        derror_douth1 = np.dot(derror_dino1, dino_douth1.T)
        douth_dinh1 = sigmoid_der(input_hidden1)
        dinh_dwh1 = input_features
        # separating out calculations to make gradient descent for the
        # bias easier
        deriv1 = douth_dinh1 * derror_douth1
        # combine all the previous derivatives into derror/dwh1
        # we have to transpose the dinh/dwh1 to make it compatible with the
        # other matrix
        derror_dwh1 = np.dot(dinh_dwh1.T, deriv1)

        # update the weights
        weight_output -= lr * derror_dwo
        weight_hidden2 -= lr * derror_dwh2
        weight_hidden1 -= lr * derror_dwh1

        # update the biases
        for i in deriv_op:
            bias_op -= lr * i
        for j in deriv2:
            bias2 -= lr * j
        for k in deriv1:
            bias1 -= lr * k

# # save all the ANN data
# save_data(save)
if save:
    np.savetxt(func + '/' + 'weight_hidden1.csv', weight_hidden1, delimiter=',')
    np.savetxt(func + '/' + 'weight_hidden2.csv', weight_hidden2, delimiter=',')
    np.savetxt(func + '/' + 'weight_output.csv', weight_output, delimiter=',')
    np.savetxt(func + '/' + 'bias1.csv', bias1, delimiter=',')
    np.savetxt(func + '/' + 'bias2.csv', bias2, delimiter=',')
    np.savetxt(func + '/' + 'bias_op.csv', bias_op, delimiter=',')
    print("the ANN has been saved")

if display:
    # display the final value of the weights
    print("weight_hidden1")
    print(weight_hidden1)
    print("bias1")
    print(bias1)
    print("weight_hidden2")
    print(weight_hidden2)
    print("bias2")
    print(bias2)
    print("weight_output")
    print(weight_output)
    print("bias_op")
    print(bias_op)

if test:
    if func == "function1":
        forward_arr = np.array([0, 0], dtype=np.float64)
        forward_prop(forward_arr)
        forward_arr = np.array([1, 0], dtype=np.float64)
        forward_prop(forward_arr)
        forward_arr = np.array([0, 1], dtype=np.float64)
        forward_prop(forward_arr)
        forward_arr = np.array([1, 1], dtype=np.float64)
        forward_prop(forward_arr)
    elif func == "function2":
        forward_arr = np.array([1, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=np.float64)
        forward_prop(forward_arr)
