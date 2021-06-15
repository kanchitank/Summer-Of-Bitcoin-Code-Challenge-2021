import pandas as pd  # importing the packages
from csv import reader
import matplotlib.pyplot as plt
import copy

mempool_list = []  # declaring an empty list -> mempool_list

with open('mempool.csv', 'r') as obj:  # opening the csv file in reader mode
    next(obj)  # skipping the first row
    csv_reader = reader(obj)
    for row in csv_reader:
        row[1] = int(row[1])  # changing string datatype to int
        row[2] = int(row[2])  # changing string datatype to int
        row[3] = [x for x in row[3].split(';')]  # splitting the parent_txids into a sublist
        mempool_list.append(row)  # appending the rows to the empty list -> mempool_list

'''
/*This code is used for visualizing the trends in Fee and Weight after sorting the data on Fee (descending) using a line chart*/ 
df = pd.read_csv("mempool.csv")  #read csv file using pandas library
sorted_df = df.sort_values(by=["fee"], ascending=False)  #sort the dataset on Fee column (descending)
x = sorted_df['fee']  #X-axis points
y = sorted_df['weight']  #Y-axis points 
plt.figure(figsize=(20,8))  
plt.title('Fee vs Weight')
plt.xlabel('Fee')
plt.ylabel('Weight')
plt.plot(x, y)  # Plot the chart
plt.show()   
'''

score = []  # declaring an empty list -> score

for i in range(len(mempool_list)):
    X = mempool_list[i][1] - mempool_list[i][2]  # difference between Fee and Weight of a transaction
    score.append(X)  # appending the score to the score list

score_1 = score.copy()  # creating a copy of score list
score_1.sort(reverse=True)  # sorting the list (descending)

mempool_list_1 = []  # declaring another list

for i in range(len(score)):
    for j in range(len(score)):
        if score_1[i] == score[j]:  # checking for the scores in the reverse sorted list which are equal to the score in the unsorted list
            if mempool_list[j] not in mempool_list_1:  # checking for duplicates
                mempool_list_1.append(mempool_list[j])  # appending the scores

mempool_list = mempool_list_1


def find_parent(item):  # function to find the parent txid if present in the first column
    for k in range(len(mempool_list)):
        if mempool_list[k][0] == item:
            return k


sum_weight = 0  # declaring variables
sum_fee = 0
index = []
final_block = []

for i in range(len(mempool_list)):
    while sum_weight <= 4000000:  # while loop will run till the sum_weight equals 4000000
        if mempool_list[i][3][0] == '':  # if there are no parent txids in a particular transaction, this loop will run
            if (sum_weight + mempool_list[i][2]) <= 4000000:  # checking if the sum of "sum_weight" and weight of the transaction is less than or equal to 4000000
                sum_weight = sum_weight + mempool_list[i][2]  # adding the transaction weight to the sum_weight variable
                sum_fee = sum_fee + mempool_list[i][1]  # adding the transaction fee to the sum_fee variable
                index.append(i)  # appending the index of the transaction to the index list
                final_block.append(mempool_list[i][0])  # appending the txid to the block
        else:  # if there are parent txids in a particular transaction, this loop will run
            sum_weight_p = sum_weight  # declaring variable sum_weight_p which stores the value of sum_weight
            sum_fee_p = sum_fee  # declaring variable sum_fee_p which stores the value of sum_fee
            idx = []  # declaring a list -> idx (for storing indices)

            for item in mempool_list[i][3]:
                indexx = find_parent(
                    item)  # finding the location of the parent txid in the first column using the function "find_parent"
                sum_weight_p = sum_weight_p + mempool_list[indexx][2]  # adding the transaction weight of the parent txid to the sum_weight_p variable
                sum_fee_p = sum_fee_p + mempool_list[indexx][1]  # adding the transaction fee of the parent txid to the sum_fee_p variable
                idx.append(indexx)  # appending the index of the parent transaction to the idx list

            sum_weight_c = sum_weight_p + mempool_list[i][2]  # adding the transaction weight of the existing txid to the sum_weight_p variable and assigning it to sum_weight_c
            sum_fee_p = sum_fee_p + mempool_list[i][1]  # updating the sum_fee_p variable by adding the transaction fee of the existing txid to it
            idx.append(i)  # appending the index of the existing transaction to the idx list

            if sum_weight_c <= 4000000:  # checking if the sum_weight_c variable is less than or equal to 4000000
                sum_weight = sum_weight_c  # transfering sum_weight_c value to sum_weight
                sum_fee = sum_fee_p  # transfering sum_fee_p value to sum_fee
                for item in idx:
                    final_block.append(mempool_list[item][0])  # appending the txid to the block

        break  # breaking the loop once the sum_weight reaches 4000000 value

print("Sum of weights:", sum_weight)  # printing the output
print("\nMaximum fees:", sum_fee)
print("\nLength of the block:", len(final_block))
print("\nFinal block of txids:")
print(final_block)

with open("block.txt", 'w') as output:  # exporting the output txids to "block.txt" file
    for row in final_block:
        output.write(str(row) + '\n')