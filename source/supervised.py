from sklearn import model_selection, tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import precision_recall_fscore_support, \
    mean_absolute_error, mean_squared_error, accuracy_score, max_error
from sklearn.tree import export_graphviz
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.model_selection import learning_curve, train_test_split, cross_val_score

from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
import numpy as np
from sklearn.svm import SVC
from sklearn import model_selection
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.base import clone
from sklearn.preprocessing import normalize

def k_fold(X: pd.DataFrame, y: pd.Series, n_folds: int, classifier, verbose=False):

    kf = model_selection.KFold(n_splits=n_folds)
    i_train = 0
    i_test = 0
    j = 1
    max_score = 0
    curr_test_score = 0
    
    """
    if model_type=="tree":
        curr_tree = DecisionTreeClassifier(max_depth=5)
    elif model_type=="grad_boost":
        curr_tree = GradientBoostingClassifier()
    elif model_type=="random_forest":
        curr_tree = RandomForestClassifier(n_estimators=20)
        """
    

    for train_indexes, test_indexes in kf.split(X, y):
        curr_classifier = clone(classifier)
        curr_classifier = curr_classifier.fit(X.iloc[train_indexes], y[train_indexes])
        
        curr_train_score = curr_classifier.score(X.iloc[train_indexes], y[train_indexes])
        curr_test_score = curr_classifier.score(X.iloc[test_indexes], y[test_indexes])

        if verbose:
            print("Fold " + str(j) + "/" + str(n_folds))
            print("--------MODEL " + str(j) + " QUALITY--------")

            print("-------| Training |-----------")

            print_classifier_scores(true_y=y[train_indexes], 
                                pred_y=curr_classifier.predict(X.iloc[train_indexes]), beta=2.0)
        
            print("-------|   Test   |-----------")
            true_y = y[test_indexes]
            pred_y = curr_classifier.predict(X.iloc[test_indexes])
            print_classifier_scores(true_y=true_y, pred_y=pred_y, beta=2.0)


        if curr_test_score > max_score:
            best_classifier = curr_classifier
            max_score = curr_test_score

        j += 1
        i_train += curr_train_score
        i_test += curr_test_score

    mean_train_score = i_train / n_folds
    mean_test_score = i_test / n_folds

    return best_classifier, mean_train_score, mean_test_score

def print_classifier_scores(true_y, pred_y, beta=1.0):
    (pr, rec, f_sc, su) = precision_recall_fscore_support(y_true=true_y, y_pred=pred_y, beta=beta, average="macro")
    acc = accuracy_score(y_true=true_y, y_pred=pred_y)
    print("Accuracy:\t" + str(acc))
    print("Precision:\t" + str(pr))
    print("Recall:\t\t" + str(rec))
    print("F-measure" + ":\t" + str(f_sc))
    print("(beta " + str(beta) + ")")

def my_knn():

    df1 = pd.read_csv("crimes_selected.csv")
    df2 = pd.read_csv("working_dataset.csv")
    df = pd.merge(df1, df2, on="CASE_NUMBER")

    x = pd.DataFrame(normalize(df[["Latitude", "Longitude"]], axis=0))

    y = df["IS_HOMICIDE"]
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.1, random_state=33)
    knn = KNeighborsClassifier()
    k_scores = []

    for k in range(1, 31, 2):
        best_model, train_score, test_score = k_fold(x, y, 10, classifier=KNeighborsClassifier(k),verbose=False)        
        print("For: ", k)
        print("Test: ", str(test_score))
        print("Train: ", str(train_score))

    pass

def my_svm():
    ds_original = pd.read_csv("crimes_selected.csv")
    ds_new = pd.read_csv("working_dataset.csv")

    complete_df: pd.DataFrame = pd.merge(ds_original, ds_new, on="CASE_NUMBER")
    df_for_nb = complete_df.drop(["Location Description","CASE_NUMBER", "Date", "Block", "Latitude", "Longitude", "NUM_CRIMES_DISTRICT", "NUM_CRIMES_BEAT", "NUM_CRIMES_COMM_AREA", "NUM_CRIMES_WARD", "NUM_CRIMES_BLOCK", "NUM_CRIMES_ZIP_CODE", "NUM_CRIMES_STREET_ORG", "AVG_NUM_CHARGES", "AREA_INCOME", "AREA_ASSAULT_HOMICIDE", "AREA_FIREARM", "AREA_POVERTY_HEALTH", "AREA_HIGH_SCHOOL_DIPLOMA", "AREA_UNEMPLOYMENT", "AREA_BIRTH_RATE", "NUM_OF_DEAD", "NUM_OF_VICTIMS", "IS_KILLED_A_CHILD", "MULTIPLE_ARRESTS", "ARRESTED_RACE", "VICTIM_RACE", "AVER_AGE"], axis=1)
    
    X = df_for_nb.drop(["IS_HOMICIDE"], axis=1)
    y = df_for_nb["IS_HOMICIDE"]
    print(df_for_nb.columns)
    best_model, train_score, test_score = k_fold(X, y, 10, verbose=True, classifier=SVC(kernel='sigmoid'))
    print(str(test_score)) # 0.5

#k_fold(pd.read_csv("working_dataset.csv"))
