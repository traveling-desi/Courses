function plotDataPoints(X, idx, K)
%PLOTDATAPOINTS plots data points in X, coloring them so that those with the same
%index assignments in idx have the same color
%   PLOTDATAPOINTS(X, idx, K) plots data points in X, coloring them so that those 
%   with the same index assignments in idx have the same color

% Create palette
palette = hsv(K + 1);
colors = palette(idx, :);

% Plot the data
%scatter(X(:,1), X(:,2), 15, colors);
% work around for scatter bug
pt_size = 15; 
rws = rows(X);
if rws <= 100
	scatter(X(:,1), X(:,2), pt_size, colors);
else
	loops = floor(rws/100);
	for i = 1:loops
		range = (1+(i-1)*100):(i*100);
		scatter(X(range,1), X(range,2), pt_size, colors(range,:));
	endfor
	if rws > loops*100
		range = (1+loops*100):rws;
		scatter(X(range,1), X(range,2), pt_size, colors(range,:));
	endif
endif

end
