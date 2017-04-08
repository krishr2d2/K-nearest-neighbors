Program a3.py :
	- uncomment the first 3 lines that loads the training data and performs 3 fold cross-validation on the datatraining.txt
	- those 3 lines generate the file error_matrix.txt for KNN and error_matrix_mknn.txt for Modified-KNN for values of k ranging from 1 to 10.
	- then parse the 'error_matrix.txt' or 'error_matrix_mknn.txt' and figure out the optimal_k for which the mean error is minimum
	- now perform the KNN or modified-KNN procedure with that optimal_k and print out the accuracy

Program plots_and_results.py :
	- This program plots a graph of k values(1-10) Vs. Cross-validation error.
	- The same program could be used for both error_matrix.txt and error_matrix_mknn.txt.
 	
