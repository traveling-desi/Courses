%% Initialization
clear ; close all; clc

%temp = dlmread("train.csv",",");
%y = temp(:,1);
%X = temp(:,2:size(temp,2));
%save("train.mat", "X", "y");

%load('ex4weights.mat');
%Theta1_new = zeros(size(Theta1,1),785);
%Theta1_new(:,1:401) = Theta1;
%Theta1_new(:,402:785) = Theta1(:,1:384);
%Theta1 = Theta1_new;
%% Unroll parameters 
%nn_params = [Theta1(:) ; Theta2(:)];

% Weight regularization parameter (we set this to 0 here).
%lambda = 1;

%J = nnCostFunction(nn_params, input_layer_size, hidden_layer_size, ...
%                   num_labels, X_train, y_train, lambda);




%%%%%%%%%%%%%%%
%%% Start of Code
%%%%


%% Initialization
clear ; close all; clc

load("train.mat");
y = y(2:size(y,1));
X = X(2:size(X,1),1:size(X,2));
y(y(:) == 0) = 10;

%%  -- sel = randperm(size(X, 1));
%%  -- train_size = 0.6*size(X,1);
%%  -- sel_train = sel(1:train_size);
%%  -- sel_cv = sel(train_size+1:size(X,1));
%%  -- X_train = X(sel_train,:);
%%  -- X_cv = X(sel_cv,:);
%%  -- y_train = y(sel_train,:);
%%  -- y_cv = y(sel_cv,:);

%%  -- sel_disp = sel(1:100);
%%  -- displayData(X(sel_disp, :));

%%  --%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%  --%%%%	Code for NN without Principal Component Analysis
%%  --%%%%
%%  --%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%  -- %% Setup the parameters you will use for this exercise
%%  -- input_layer_size  = 784;  % 28x28 Input Images of Digits
%%  -- hidden_layer_size = 100;   % 100 hidden units
%%  -- num_labels = 10;          % 10 labels, from 1 to 10   
%%  --                           % (note that we have mapped "0" to label 10)
%%  -- 
%%  -- 
%%  -- 
%%  -- initial_Theta1 = randInitializeWeights(input_layer_size, hidden_layer_size);
%%  -- initial_Theta2 = randInitializeWeights(hidden_layer_size, num_labels);
%%  -- % Unroll parameters
%%  -- initial_nn_params = [initial_Theta1(:) ; initial_Theta2(:)];
%%  -- 
%%  -- 
%%  -- %  After you have completed the assignment, change the MaxIter to a larger
%%  -- %  value to see how more training helps.
%%  -- options = optimset('MaxIter', 10);
%%  -- 
%%  -- 
%%  -- %  You should also try different values of lambda
%%  -- lambda_mat = [0.01, 0.03, 0.1, 0.3, 1, 3, 10];
%%  -- 
%%  -- accuracy_mat = zeros(size(lambda_mat));


%%  --
%%  --
%%  --for i =1:size(lambda_mat,2)
%%  --	lambda = lambda_mat(i)
%%  --
%%  --	% Create "short hand" for the cost function to be minimized
%%  --	costFunction = @(p) nnCostFunction(p, ...
%%  --        	                           input_layer_size, ...
%%  --                	                   hidden_layer_size, ...
%%  --                        	           num_labels, X_train, y_train, lambda);
%%  --
%%  --	% Now, costFunction is a function that takes in only one argument (the
%%  --	% neural network parameters)
%%  --	[nn_params, cost] = fmincg(costFunction, initial_nn_params, options);
%%  --
%%  --	% Obtain Theta1 and Theta2 back from nn_params
%%  --	Theta1 = reshape(nn_params(1:hidden_layer_size * (input_layer_size + 1)), ...
%%  --        	         hidden_layer_size, (input_layer_size + 1));
%%  --
%%  --	Theta2 = reshape(nn_params((1 + (hidden_layer_size * (input_layer_size + 1))):end), ...
%%  --        	         num_labels, (hidden_layer_size + 1));
%%  --
%%  --	pred = predict(Theta1, Theta2, X_cv);
%%  --	accuracy_mat(i) = mean(double(pred == y_cv));
%%  --endfor
%%  --
%%  --[max_accuracy, optim_itr] = max(accuracy_mat);
%%  --
%%  --lambda = lambda_mat(optim_itr);
%%  --
%%  --% Create "short hand" for the cost function to be minimized
%%  --costFunction = @(p) nnCostFunction(p, ...
%%  --       	                           input_layer_size, ...
%%  --               	                   hidden_layer_size, ...
%%  --                       	           num_labels, X_train, y_train, lambda);
%%  --
%%  --
%%  --% Now, costFunction is a function that takes in only one argument (the
%%  --% neural network parameters)
%%  --[nn_params, cost] = fmincg(costFunction, initial_nn_params, options);
%%  --
%%  --% Obtain Theta1 and Theta2 back from nn_params
%%  --Theta1 = reshape(nn_params(1:hidden_layer_size * (input_layer_size + 1)), ...
%%  --                 hidden_layer_size, (input_layer_size + 1));
%%  --
%%  --Theta2 = reshape(nn_params((1 + (hidden_layer_size * (input_layer_size + 1))):end), ...
%%  --                 num_labels, (hidden_layer_size + 1));
%%  --
%%  --
%%  --
%%  --%%% Testing
%%  --
%%  --load("test.mat");
%%  --X = X(2:size(X,1),1:size(X,2));
%%  --pred = predict(Theta1, Theta2, X);
%%  --pred(pred(:) == 10) = 0;
%%  --dlmwrite("pred.csv", pred, ",");

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%	Code for NN with Principal Component Analysis
%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%% Running PCA
[U, S] = pca(X);
S_vec = sum(S);

t = sum(S_vec);

h = zeros(size(S_vec,2),1);
for i = 1:size(S_vec,2)
	temp = zeros(size(S_vec,1),i);
	temp = S_vec(1:i);
	h_val = sum(temp)/t;
	h(i,1) = h_val;
	if h_val >= 0.99
		break;
	endif
endfor

K = find(h,1,"last");
Z = projectData(X, U, K);

sel = randperm(size(Z, 1));
train_size = 0.6*size(Z,1);
sel_train = sel(1:train_size);
sel_cv = sel(train_size+1:size(Z,1));
Z_train = Z(sel_train,:);
Z_cv = Z(sel_cv,:);
y_train = y(sel_train,:);
y_cv = y(sel_cv,:);


%% Setup the parameters you will use for this exercise
input_layer_size  = K;  % PCA dimensions
hidden_layer_size = 100;   % 100 hidden units
num_labels = 10;          % 10 labels, from 1 to 10   

initial_Theta1 = randInitializeWeights(input_layer_size, hidden_layer_size);
initial_Theta2 = randInitializeWeights(hidden_layer_size, num_labels);
% Unroll parameters
initial_nn_params = [initial_Theta1(:) ; initial_Theta2(:)];


%  After you have completed the assignment, change the MaxIter to a larger
%  value to see how more training helps.
options = optimset('MaxIter', 100);


%  You should also try different values of lambda
lambda_mat = [0.01, 0.03, 0.1, 0.3, 1, 3, 10];

accuracy_mat = zeros(size(lambda_mat));

for i =1:size(lambda_mat,2)
	lambda = lambda_mat(i);

	% Create "short hand" for the cost function to be minimized
	costFunction = @(p) nnCostFunction(p, ...
        	                           input_layer_size, ...
                	                   hidden_layer_size, ...
                        	           num_labels, Z_train, y_train, lambda);

	% Now, costFunction is a function that takes in only one argument (the
	% neural network parameters)
	[nn_params, cost] = fmincg(costFunction, initial_nn_params, options);

	% Obtain Theta1 and Theta2 back from nn_params
	Theta1 = reshape(nn_params(1:hidden_layer_size * (input_layer_size + 1)), ...
        	         hidden_layer_size, (input_layer_size + 1));

	Theta2 = reshape(nn_params((1 + (hidden_layer_size * (input_layer_size + 1))):end), ...
        	         num_labels, (hidden_layer_size + 1));

	pred = predict(Theta1, Theta2, Z_cv);
	accuracy_mat(i) = mean(double(pred == y_cv));
endfor

[max_accuracy, optim_itr] = max(accuracy_mat);

lambda = lambda_mat(optim_itr);

% Create "short hand" for the cost function to be minimized
costFunction = @(p) nnCostFunction(p, ...
       	                           input_layer_size, ...
               	                   hidden_layer_size, ...
                       	           num_labels, Z_train, y_train, lambda);


% Now, costFunction is a function that takes in only one argument (the
% neural network parameters)
[nn_params, cost] = fmincg(costFunction, initial_nn_params, options);

% Obtain Theta1 and Theta2 back from nn_params
Theta1 = reshape(nn_params(1:hidden_layer_size * (input_layer_size + 1)), ...
                 hidden_layer_size, (input_layer_size + 1));

Theta2 = reshape(nn_params((1 + (hidden_layer_size * (input_layer_size + 1))):end), ...
                 num_labels, (hidden_layer_size + 1));



%%% Testing

load("test.mat");
X = X(2:size(X,1),1:size(X,2));
Z_test = projectData(X, U, K);
pred = predict(Theta1, Theta2, Z_test);
pred(pred(:) == 10) = 0;
dlmwrite("pred.csv", pred, ",");

