import random
import math

class data_object:
    def __init__(self,Temp,Humid,Light,CO2,Occ):
        self.Temperature = Temp
        self.Humidity = Humid
        self.Light = Light
        self.Co2 = CO2
        self.Occupancy =  Occ

def partition(l,n):
    div = len(l) / float(n)
    return [ l[int(round(div * i)): int(round(div * (i+1)))] for i in xrange(n)]

def load_data(file_path):
    f = open(file_path,'r')
    l = []
    for line in f:
        k = line.split(',')
        if k[0] == '"date"':
            continue
        else:
            temp = data_object(float(k[2]),float(k[3]),float(k[4]),float(k[5]),int(k[7].replace('\n','')))
            l.append(temp)  
    f.close()
    return l

def cross_validate(l,classifier):
######################## end of data loading ####################################
    if (classifier == 'knn'):
        f2 = open('error_matrix.txt','w')
    elif (classifier == 'modified_knn'):
        f2 = open('error_matrix_mknn.txt','w')

    random.shuffle(l)
    cross_folds = partition(l,3)
    error_mat = []
    for i in range(3) : 
	print 'Current fold : '+str(i)
    	valid = cross_folds[i]
    	train = []
    	for j in filter(lambda x:x != i,range(3)):
            train += cross_folds[j]
    	error = []
    	for k in range(1,11):
            miss_count = 0
            for point in valid :
            	dst = [[calculate_distance(point,po),po.Occupancy] for po in train]
            	dst.sort(key=lambda x:x[0])
                if (classifier == 'knn'):
            	    if (point.Occupancy != calc_class(dst,k)):
                        miss_count += 1
                elif (classifier == 'modified_knn'):
                    if (point.Occupancy != calc_class_mknn(dst,k)):
                        miss_count += 1
            error.append(float(miss_count)/float(len(valid)))
        error_mat.append(error)
	
    for i in error_mat:
        print i
        f2.write(str(i))

    f2.close()

def test_the_data(k,l_train,l_test,classifier):
    # print the accuracy of the classifier for k neighbors...
    hit_count = 0.0
    for point in l_test:
        dst = [[calculate_distance(point,po),po.Occupancy] for po in l_train]
        dst.sort(key=lambda x:x[0])
        if (classifier == 'knn'):
            if (point.Occupancy == calc_class(dst,k)):
                hit_count += 1.0
        elif (classifier == 'modified_knn'):
            if (point.Occupancy == calc_class_mknn(dst,k)):
                hit_count += 1.0

    print "Accuracy : ",(hit_count / float(len(l_test)))*100

def calc_class(dst,k): # majority based classification in normal knn...
    count = 0;
    for i in range(k):
        if dst[i][1] == 1:
            count += 1            
    if count > k-count :
        return 1
    else :
        return 0

def calc_class_mknn(dst,k): #weight based classification in modified knn...
    wt_1 = 0
    wt_2 = 0
    weight = 0
    for i in range(k):
        if (dst[k-1][0] == dst[0][0]):
            weight = 1
        else :
            weight =  (dst[k-1][0] - dst[i][0])/(dst[k-1][0] - dst[0][0]) # weights for every neighbor...
        if (dst[i][1] == 1):
            wt_1 += weight
        else:
            wt_2 += weight

    if wt_1 > wt_2 :
        return 1
    else :
        return 0


def calculate_distance(l1,l2):
    # return Euclidean distance between the vectors...
    return math.sqrt(pow(l1.Temperature-l2.Temperature, 2) + pow(l1.Humidity-l2.Humidity, 2) + pow(l1.Light-l2.Light, 2) + pow(l1.Co2-l2.Co2, 2))

################################################# main function ##############################################
#the below 3 lines are used for 3-fold-crossvalidation and determining the optimal k...
#l=load_data('datatraining.txt')    #load data into a list of objects
#cross_validate(l,'knn')            #cross-validate using normal knn (generates 'error_matrix.txt')
#cross_validate(l,'modified_knn')   #cross_validate using modified knn (generates 'error_matrix_mknn.txt')

#err = open('error_matrix_mknn.txt','r') #comment out for normal knn and uncomment the below line...
err = open('error_matrix.txt','r')
l = err.readline()
l = l.split('][')
l = [i.replace('[','') for i in l]
l = [i.replace(']','') for i in l]
l = [i.replace('\n','') for i in l]
err.close()
l = [i.split(',') for i in l]
for i in range(len(l)):
    l[i] = [float(p) for p in l[i]]
    #print l[i]
mean_error = map(lambda x,y,z:(x+y+z)/3.0,l[0],l[1],l[2])
optimal_k = mean_error.index(min(mean_error))+1

print 'Optimal k :',optimal_k

l_train=load_data('datatraining.txt')
l_test=load_data('datatest.txt')
l_test2 = load_data('datatest2.txt')

print '\nTesting using KNN classifier...'
print '''For test-data in "datatest.txt" '''
test_the_data(optimal_k,l_train,l_test,'knn')
print '''For test-data in "datatest2.txt" '''
test_the_data(optimal_k,l_train,l_test2,'knn')

print '\nTesting using Modified KNN classifier...'
print '''For test-data in "datatest.txt" '''
test_the_data(optimal_k,l_train,l_test,'modified_knn')
print '''For test-data in "datatest2.txt" '''
test_the_data(optimal_k,l_train,l_test2,'modified_knn')
