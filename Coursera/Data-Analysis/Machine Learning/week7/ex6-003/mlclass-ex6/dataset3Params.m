function [C, sigma] = dataset3Params(X, y, Xval, yval)
%EX6PARAMS returns your choice of C and sigma for Part 3 of the exercise
%where you select the optimal (C, sigma) learning parameters to use for SVM
%with RBF kernel
%   [C, sigma] = EX6PARAMS(X, y, Xval, yval) returns your choice of C and 
%   sigma. You should complete this function to return the optimal C and 
%   sigma based on a cross-validation set.
%

% You need to return the following variables correctly.
C = 1;
sigma = 0.1;

% ====================== YOUR CODE HERE ======================
% Instructions: Fill in this function to return the optimal C and sigma
%               learning parameters found using the cross validation set.
%               You can use svmPredict to predict the labels on the cross
%               validation set. For example, 
%                   predictions = svmPredict(model, Xval);
%               will return the predictions on the cross validation set.
%
%  Note: You can compute the prediction error using 
%        mean(double(predictions ~= yval))
%

%C_optim = 1;
%sigma_optim = 0.3;
%C_mat = [0.01, 0.03, 0.1, 0.3, 1, 3, 10, 30]
%sigma_mat = [0.01, 0.03, 0.1, 0.3, 1, 3, 10, 30]
%error_min = 9999999
%for i = 1:8
%	C = C_mat(i);
%	for j = 1:8
%		disp("now in iteration : "), disp(i*j);
%		disp("\n");
%		sigma = sigma_mat(j);
%		model= svmTrain(X, y, C, @(x1, x2) gaussianKernel(x1, x2, sigma));
%                predictions = svmPredict(model, Xval);
%		new_error = mean(double(predictions ~= yval));
%		if (error_min > new_error)
%			error_min = new_error;
%			C_optim = C;
%			sigma_optim =sigma;
%		endif
%	endfor
%endfor
%
%C = C_optim;
%sigma = sigma_optim;
%model= svmTrain(X, y, C, @(x1, x2) gaussianKernel(x1, x2, sigma));
%visualizeBoundary(X, y, model);




% =========================================================================

end
