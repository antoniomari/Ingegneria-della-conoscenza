from sklearn import model_selection, tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import precision_recall_fscore_support, \
    mean_absolute_error, mean_squared_error, accuracy_score, max_error
from sklearn.tree import export_graphviz
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.model_selection import learning_curve


def k_fold(tr_data: pd.DataFrame, n_folds=2):
    kf = model_selection.KFold(n_splits=n_folds)

    curr_tree = DecisionTreeClassifier(max_depth=10)

    X: pd.DataFrame = tr_data.drop(columns=["CASE_NUMBER", "NUM_OF_DEAD", "IS_KILLED_A_CHILD",
                                            "IS_HOMICIDE", "VICTIM_RACE", "ARRESTED_RACE", "AVER_AGE"])

    y: pd.Series = tr_data["IS_HOMICIDE"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)
    curr_tree.fit(X_train, y_train)
    pred_test = curr_tree.predict(X_test)

    export_graphviz(curr_tree, out_file="tree.dot")

    print_classifier_scores(true_y=y_test, pred_y=pred_test)

    for criterion in {"gini", "entropy", "log_loss"}:
        rf = RandomForestClassifier(n_estimators=50, criterion=criterion)
        rf.fit(X_train, y_train)
        pred_test = rf.predict(X_test)

        print_classifier_scores(true_y=y_test, pred_y=pred_test)


def print_classifier_scores(true_y, pred_y, beta=1.0):
    (pr, rec, f_sc, su) = precision_recall_fscore_support(y_true=true_y, y_pred=pred_y, beta=beta, average="macro")
    acc = accuracy_score(y_true=true_y, y_pred=pred_y)
    print("Accuracy:\t" + str(acc))
    print("Precision:\t" + str(pr))
    print("Recall:\t\t" + str(rec))
    print("F-measure" + ":\t" + str(f_sc))
    print("(beta " + str(beta) + ")")

k_fold(pd.read_csv("working_dataset.csv"))
