import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.preprocessing  import OneHotEncoder, LabelEncoder,LabelBinarizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
import matplotlib.pyplot as plt
import numpy as np


#to display all rows and cols
#pd.set_option('display.max_columns',10)
#pd.set_option('display.max_rows',None)

#$$$$$$$$$$$$$$$$$$$$$$$$$
#$$$$$$$$$$$$$$$$$$$$$$$$
#import data from csv file
#$$$$$$$$$$$$$$$$$$$$$$$$$
#$$$$$$$$$$$$$$$$$$$$$$$$$

data=pd.read_csv("__data__/bangalore_rentdtls_updt.csv",na_values=["-"])
print(data.head())

'''
#plot the data
data=pd.read_csv("ForPlot_bangalore_rentdtls_updt.csv",na_values=["-"])
loc=data.iloc[:,[0,3,4]]
print(type(loc),loc)
plt.scatter(loc["Locality"], loc["AvgRent"], c=loc["HouseType"])
plt.legend()
plt.xlabel("Locality ->")
plt.ylabel("Avg. Rent ->")
plt.xticks(rotation=45)
plt.title("Average Rent across localities in Bangalore (1BHK, 2BHK, 3BHK)")
plt.tight_layout()
plt.show() 
'''

#column data types and non-null values
data.info()

#summary of numeric columans
#print(data.describe())

# ???????? TRY TO FIND SOLN....handle "L" (for Lakhs in "4.5 L") in MinPrice and MaxPrice columsn ....FOR NOW, DELETE IT MANUALLY
#
#drop rows having "L" (lakh) in either minprice, maxprice or avg rent
#print("---&&&&&&&&&&--")
#print(data.query("'*L*' in MaxPrice"))
#print(data["MaxPrice"].str.contains("L"))
#print("---&&&&&&&&&&--")
#
#

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#-------------------------PRE-PROCESSING--------------------------
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

'''
#rent cols to int
for col in data.select_dtypes("object"):
	print("INSIDE -> rent cols to int")
	#if col in ("MinPrice","MaxPrice","AvgRent"):
	if col in ("MinPrice"):
		print(col, data[col].dtype)
		data[col]=data[col].astype(int)

data.info() #
'''

#handle outliers

#handle values like "8 L" for 800000

#handle nan values...ANY OTHER WAY TO HANDLE NaNs
data=data.dropna()
#data.dropna(inplace=True)
data.info() #
print(data)
print()


#=========================================
#Handle categorical value (INPUT FEATURES)
#=========================================

# NOTE : *** this conversion to be put into NEW module / class and call it ***

ohe=OneHotEncoder()

#fit
ohe.fit(data[["Locality"]])
print("Identified Categories")
print(ohe.categories_)
print()
print("Feature Names")
print(ohe.get_feature_names_out())
print()

#transform into one hot encoding
data_new=ohe.transform(data[["Locality"]]).toarray()
data_newdf=pd.DataFrame(data=data_new,columns=ohe.get_feature_names_out())
print(data_newdf)
print()

df_price=data[["MinPrice","MaxPrice","AvgRent"]]
print(type(df_price), df_price)
df_price=df_price.reset_index(drop=True) # see what happens if you dont use this
print(type(df_price), df_price)

#join input features
print("Input features concatenated")
data_features_final=pd.concat([data_newdf,df_price],axis=1)
#print(data_features_final.head())
print(data_features_final)
print()

#===================================
#scale the feature vector X (inputs)
#===================================
ss=StandardScaler()
data_features_final=pd.DataFrame(data=ss.fit_transform(data_features_final))
print("After Scaling")
print(data_features_final.head())


#============================================
# Handle categorical values (OUTPUT / TARGET)
#============================================


''' 
print("WITHOUT LabelBinarizer")
le=LabelEncoder()
le.fit(data["HouseType"])
print(le.classes_)
data_out=le.transform(data["HouseType"])
#print(data_out[:6])
print(data_out)
print()
'''

print("WITH LabelBinarizer")
lb=LabelBinarizer()
lb.fit(data["HouseType"])
print(lb.classes_)
data_out=lb.transform(data["HouseType"])
print(type(data_out), data_out[:6])
#print(data_out)
print()



#join all the columsn into one (i:e input features + class))
print("Final dataset before training")
#data_final=pd.concat([data_features_final,pd.Series(data_out)],axis=1) # before using LabelBinarizer
data_final=pd.concat([data_features_final,pd.DataFrame(data_out)],axis=1) # after using LabelBinarizer
print(data_final)
#print(data_final.info())
print()


#$$$$$$$$$$$$$$$$$$$$$
#$$$$$$$$$$$$$$$$$$$$$
#-----Define X and y
#$$$$$$$$$$$$$$$$$$$$$
#$$$$$$$$$$$$$$$$$$$$$

X=data_final.iloc[:,:-1]
print(X.head())

y=data_final.iloc[:,-1]
print(y[:5])
print()

#print(data_final.describe())
#print(data_final[0].value_counts())
data_final.to_csv("exported_data_final.csv")

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#--------------train model-----------------
#$$$$$$$$$$$$$$$$$$$$$#$$$$$$$$$$$$$$$$$$$$$
#$$$$$$$$$$$$$$$$$$$$$#$$$$$$$$$$$$$$$$$$$$$

train_x,test_x,train_y,test_y=train_test_split(X,y,test_size=0.2,random_state=2)

print(type(train_x),type(train_y))
#model=LogisticRegression()
model=SVC()
model.fit(train_x,train_y)



#$$$$$$$$$$$$$$$$$$$$$$
#$$$$$$$$$$$$$$$$$$$$$$
#-------predict--------
#$$$$$$$$$$$$$$$$$$$$$$
#$$$$$$$$$$$$$$$$$$$$$$

#print("Test Data")
#print(test_x)
predict_train_y=model.predict(train_x)
predict_test_y=model.predict(test_x)


#$$$$$$$$$$$$$$$$$$$$$$
#$$$$$$$$$$$$$$$$$$$$$$
#------metrics---------
#$$$$$$$$$$$$$$$$$$$$$$
#$$$$$$$$$$$$$$$$$$$$$$

# TRAIN DATA
print("confusion matrix for TRAIN data")
print(confusion_matrix(train_y,predict_train_y))
print()

print("accuracy score for TRAIN data")
print("Accuracy Score : %.2f "%accuracy_score(train_y,predict_train_y))
print()
print()

# TEST DATA
print("confusion matrix for TEST data")
print(confusion_matrix(test_y,predict_test_y))
print()

print("accuracy score for TEST data")
print("Accuracy Score : %.2f "%accuracy_score(test_y,predict_test_y))

#feature scaling (run model WITH / WITHOUT feature scaling)
# 
# ================Logistic Regression =====================
# WITHOUT scaling : train acc - 45 % , test acc - 41 %
# WITH scaling : train acc - 99 % test acc - 41 %
# WITHOUT scaling but WITH labelbinarizer : train acc - 71 % test acc - 67 %
# WITH scaling and WITH labelbinarizer : train acc - 100 % test acc -85 %
# 
# ================ SVC =====================
# WITH scaling and WITH labelbinarizer : train acc - 81 % test acc - 70 %
#
# 

# to do
# ...inverse transofmr test data and see which are new data 
# ...//try to visualize data
# ....modularize code...func to pre-process, train , pass new data (Ex. loc,minrent,max rent) and pre-process and predict

