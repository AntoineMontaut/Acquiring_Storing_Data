'''Unit4 Lesson6'''

from sklearn import datasets
import pandas as pd
import matplotlib.pyplot as plt

iris = datasets.load_iris()
# print(iris['target_names'])
# print(iris['data'][:5, :])
# print(iris.keys())
# print(iris['feature_names'])
# print(iris['DESCR'])

df = pd.DataFrame(iris['data'], columns=['sepal_len', 'sepal_wid', 'petal_len', 'petal_wid'])
df['target'] = iris['target']
df['iris'] = df.target.map(lambda x: iris['target_names'][x])
# print(df.head())
# print(df.tail())
print(df.info())

def plot_data():
    
    fig = plt.figure('Iris', figsize=(12,6))
    plt.subplot(1, 2, 1)
    plt.scatter(df[df.iris=='setosa'].sepal_len, df[df.iris=='setosa'].sepal_wid, c='b', label='Setosa')
    plt.scatter(df[df.iris=='versicolor'].sepal_len, df[df.iris=='versicolor'].sepal_wid, c='r', label='Versicolor')
    plt.scatter(df[df.iris=='virginica'].sepal_len, df[df.iris=='virginica'].sepal_wid, c='g', label='Virginica')
    plt.legend(loc='upper right')
    plt.xlabel('Sepal Length (cm)')
    plt.ylabel('Sepal Width (cm)')
    
    plt.subplot(1, 2, 2)
    plt.scatter(df[df.iris=='setosa'].sepal_len, df[df.iris=='setosa'].sepal_wid, c='b', label='Setosa')
    plt.scatter(df[df.iris=='versicolor'].sepal_len, df[df.iris=='versicolor'].sepal_wid, c='r', label='Versicolor')
    plt.legend(loc='upper right')
    plt.xlabel('Sepal Length (cm)')
    plt.ylabel('Sepal Width (cm)')
    
    
    
    # plt.scatter(iris.data[:100, 1], iris.data[:100, 2], c=iris.target[:100])
    # plt.xlabel(iris.feature_names[1])
    # plt.ylabel(iris.feature_names[2])

    plt.show()
    
# plot_data()

