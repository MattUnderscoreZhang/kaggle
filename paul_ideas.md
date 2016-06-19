Ideas
====
1. clean up feature set
  * bruteforce combinotoric search for best feature set
  * principal component analysis
2. streamline basic model testing
  * use scipy.optimize to find optimal model parameters
  * standarize test scores (accuracy, log-loss and ?)
3. elimate obvious cases from training data
  * if neuter\_status == "Unknown", then Adoption probability = 0
  * 

Overview of Workflow
====

[Feature Selection][2]
----
1. chi squared test
2. information gain
3. correlation coefficient scores
4. principal component analysis/multiple correspondence [analysis][1]
5. [Ridge regression][3], LASSO

Feature Scaling or Data Resampling
----

Classifier Selection
----
1. Logistic Regression (logit)
2. Decision Tree -> Random Forest
3. Neural Network (ex. Restricted Boltzmann machine -> logit pipeline) 

[1]: http://web.missouri.edu/~kolenikovs/talks/Gustavo-Stas-PCA-generic.pdf
[2]: http://machinelearningmastery.com/an-introduction-to-feature-selection/
[3]: http://www.ncss.com/wp-content/themes/ncss/pdf/Procedures/NCSS/Ridge_Regression.pdf
