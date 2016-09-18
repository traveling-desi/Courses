function [J grad] = nnCostFunction(nn_params, ...
                                   input_layer_size, ...
                                   hidden_layer_size, ...
                                   num_labels, ...
                                   X, y, lambda)
%NNCOSTFUNCTION Implements the neural network cost function for a two layer
%neural network which performs classification
%   [J grad] = NNCOSTFUNCTON(nn_params, hidden_layer_size, num_labels, ...
%   X, y, lambda) computes the cost and gradient of the neural network. The
%   parameters for the neural network are "unrolled" into the vector
%   nn_params and need to be converted back into the weight matrices. 
% 
%   The returned parameter grad should be a "unrolled" vector of the
%   partial derivatives of the neural network.
%

% Reshape nn_params back into the parameters Theta1 and Theta2, the weight matrices
% for our 2 layer neural network
Theta1 = reshape(nn_params(1:hidden_layer_size * (input_layer_size + 1)), ...
                 hidden_layer_size, (input_layer_size + 1));

Theta2 = reshape(nn_params((1 + (hidden_layer_size * (input_layer_size + 1))):end), ...
                 num_labels, (hidden_layer_size + 1));

% Setup some useful variables
m = size(X, 1);
         
% You need to return the following variables correctly 
J = 0;
Theta1_grad = zeros(size(Theta1));
Theta2_grad = zeros(size(Theta2));

% ====================== YOUR CODE HERE ======================
% Instructions: You should complete the code by working through the
%               following parts.
%
% Part 1: Feedforward the neural network and return the cost in the
%         variable J. After implementing Part 1, you can verify that your
%         cost function computation is correct by verifying the cost
%         computed in ex4.m
%
% Part 2: Implement the backpropagation algorithm to compute the gradients
%         Theta1_grad and Theta2_grad. You should return the partial derivatives of
%         the cost function with respect to Theta1 and Theta2 in Theta1_grad and
%         Theta2_grad, respectively. After implementing Part 2, you can check
%         that your implementation is correct by running checkNNGradients
%
%         Note: The vector y passed into the function is a vector of labels
%               containing values from 1..K. You need to map this vector into a 
%               binary vector of 1's and 0's to be used with the neural network
%               cost function.
%
%         Hint: We recommend implementing backpropagation using a for-loop
%               over the training examples if you are implementing it for the 
%               first time.
%
% Part 3: Implement regularization with the cost function and gradients.
%
%         Hint: You can implement this around the code for
%               backpropagation. That is, you can compute the gradients for
%               the regularization separately and then add them to Theta1_grad
%               and Theta2_grad from Part 2.
%

A_1 = X;
A_1 = [ones(m, 1) A_1];
Z_2 = A_1*Theta1';
A_2 = sigmoid(Z_2);
A_2 = [ones(m, 1) A_2];
Z_3 = A_2*Theta2';
A_3 = sigmoid(Z_3);

Theta1_temp = zeros(size(Theta1,1), size(Theta1,2)-1);
Theta2_temp = zeros(size(Theta2,1), size(Theta2,2)-1);

cost = zeros(num_labels,1);
for c = 1:num_labels
	new_y = (y == c);
	cost(c) = (((((-new_y)'*log(A_3))) - ((1 .- new_y )'*log(1 .- A_3)))/m)(c);
endfor


Theta2_temp = (Theta2(:,2:size(Theta2,2)) .^ 2);
Theta1_temp = (Theta1(:,2:size(Theta1,2)) .^ 2);
J = sum(cost) + (lambda/(2*m))*(sum(sum(Theta2_temp)) + sum(sum(Theta1_temp)));

small_delta_3 = zeros(1,num_labels);
small_delta_2 = zeros(1,hidden_layer_size);
Delta_2 = zeros(size(Theta2));
Delta_1 = zeros(size(Theta1));

for t = 1:m

	%% Forward Propagation
	a_1 = X(t,:);
	out_y = zeros(1,num_labels);
	out_y(y(t)) = 1;
	a_1 = [ones(1, 1) a_1];
	z_2 = a_1*Theta1';
	a_2 = sigmoid(z_2);
	a_2 = [ones(1, 1) a_2];
	z_3 = a_2*Theta2';
	a_3 = sigmoid(z_3);
	
	%% Calculate error @ the output
	small_delta_3 = (a_3 .- out_y);
	Delta_2 = Delta_2 .+ (small_delta_3'*a_2);
	small_delta_2 =  ((small_delta_3*(Theta2))(2:end).*sigmoidGradient(z_2));
	Delta_1 = Delta_1 .+ (small_delta_2'*a_1);
endfor

Theta1_grad = (1/m) * (Delta_1 + (lambda*Theta1));	
Theta2_grad = (1/m) * (Delta_2 + (lambda*Theta2));
Theta1_grad(:,1) = (1/m) * (Delta_1)(:,1);
Theta2_grad(:,1) = (1/m) * (Delta_2)(:,1);



% -------------------------------------------------------------

% =========================================================================

% Unroll gradients
grad = [Theta1_grad(:) ; Theta2_grad(:)];

end
