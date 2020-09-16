![WordLS](https://user-images.githubusercontent.com/22931832/88269568-f4ca6e00-ccdc-11ea-9399-650fa66a704f.png)
> It is a word learning system. It is basically designed to learn the reading errors of an OCR engine.     

# WordLS [![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) [![made-with-python](https://img.shields.io/badge/NLP-TOOL-blue)](https://github.com/fkahraman)


Wordls is an abbreviation of the word learning system. So what does it do ?

  - Classification of the word read by OCR
  - The correctness of the classification of the word
  - With the check system, he can realize that he has learned something new.

### Features
----
  - The words given as input are encoded and converted into mathematical vectors.
  - Data is generated from transformed vectors.
  - Learning takes place and the boom system is ready for your order.

A remarkable detail:
  - The data of the background learning are generated as a result of the analysis of the reading errors of the OCR engine. (You can easily change the data production characters in your own project.)

### Tech
----
In terms of performance, SVM, RF, KNN, ANN and Mixed Model(CNN + RNN) techniques have been tested and the two most successful methods have been identified as RF and Mixed Model.

* [Random Forest](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html) - Machine learning method powered by Extremely Random Forests
* [Artificial Neaural Network](https://scikit-learn.org/stable/modules/neural_networks_supervised.html) - Simple and powerfull deep learning teqnique
* [Support Vector Machine](https://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html) - Machine learning method for classification and regression
* [K Nearest Neighborhood](https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html) - Although the knn approach is an unsupervised method, in some cases we can use the cluster function as a classification. Of course, its performance is quite low compared to classification methods.
* [Mixed Model(CNN + RNN)](https://keras.io/api/layers/) - It is a deep learning library where tensorflow works in the background.

### Installation Library
----
Just run setup.exe inside the Installation folder.

```sh
$ cd Installation
$ setup.exe
```

Or manually library installation...

```sh
$ pip install scikit-learn
$ pip install Keras
$ pip install statistics
```

### Usage
----
The `setup_Encoding.py` file must be run first to create the source files and data. It should not be forgotten that this file will pull and process the products in the `words.txt` file.

We are ready to model after the data is created. Select one of the RF or Mixed modeling files and run it.Then the model will be creating in Model folder.

Finally, you will find some example in `predict.py` file.

For those who will use command line...

```sh
$ python setup_Encoding.py
$ python set_Model_RF.py
$ python predict.py
```

### Performance Test
----
In this section, we will look at the duration and success status of functions such as model success, model loading time and model prediction time.

| Process (word quantity: 187)| Status |
| ------ | ------ |
| RF Model Score  | %99.89 |
| Check Model Score  | %99.99 |
| Model Load Time | 0.613 sec |
| Check Model Load Time | 0.002 sec |
| Predict Time (Per Word) | 0.005 sec |


### What is this check or negative system?
----
 - I think the most experienced classification problems are negative classifications.
 - Although the positive classes are limited, the negative class can be unlimited. Producing a negative class can be very expensive in terms of time and resources.
 - As a solution to this situation, a second artificial intelligence model comes into play and makes an inference by examining the relationship between the predicted word and the predicted result class. This inference determines whether the word that comes as an input is in the classes.
 - The source files of the model representing the negative class and the model are available in the repository.

### Todos
----
 - Comment lines will be added
 

### Done
----
- Deep Learning technique uploaded
    
### Other
----
 - The whole system is written in Turkish language so don't forget to re-adapt the character map according to the language you will use.
 - The OCR engine used for analysis in the system is tesseract.
 - For Linux users, the utf-8 plugin may be useful.
 - If you want to produce a group of 100-200 words at the same time during data production, your ram may be insufficient. The minimum ram I recommend is 16 GB

# License [![GPLv3 license](https://img.shields.io/github/license/fkahraman/WordLS)](http://perso.crans.org/besson/LICENSE.html)
----
 - GNU General Public License v3.0
----

**Artificial intelligence at your fingertips!**
**Fatih Kahraman**

