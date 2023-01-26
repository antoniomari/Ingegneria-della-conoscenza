from sklearn import model_selection, tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import precision_recall_fscore_support, \
    mean_absolute_error, mean_squared_error, accuracy_score, max_error
from sklearn.tree import export_graphviz
import pandas as pd

def k_fold(tr_data: pd.DataFrame, n_folds):
    kf = model_selection.KFold(n_splits=n_folds)

    curr_tree = DecisionTreeClassifier(max_depth=5)

    X: pd.DataFrame = tr_data.drop(columns=["NUM_OF_DEAD", "IS_KILLED_A_CHILD", "IS_HOMICIDE"])
    y: pd.Series = tr_data["IS_HOMICIDE"]

    curr_tree.fit(X, y)

    export_graphviz(curr_tree, out_file="tree.dot")
