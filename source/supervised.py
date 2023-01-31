from sklearn import model_selection, tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import precision_recall_fscore_support, \
    mean_absolute_error, mean_squared_error, accuracy_score, max_error
from sklearn.tree import export_graphviz
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.model_selection import learning_curve, train_test_split, cross_val_score
from sklearn.naive_bayes import CategoricalNB
from sklearn.preprocessing import LabelEncoder
from sklearn import model_selection
from sklearn.base import clone
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import AdaBoostClassifier
import numpy as np
from sklearn.svm import SVC
from sklearn import model_selection
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.base import clone
from sklearn.preprocessing import normalize
import matplotlib.pyplot as plt


# for average -> "macro" or "micro"
def print_classifier_scores(true_y, pred_y, beta=1.0, average="micro"):
    acc, pr, rec, f_sc = calc_classifier_scores(true_y, pred_y, beta=beta, average=average)
    print("Accuracy:\t" + str(acc))
    print("Precision:\t" + str(pr))
    print("Recall:\t\t" + str(rec))
    print("F-measure" + ":\t" + str(f_sc))
    print("(beta " + str(beta) + ")")


def calc_classifier_scores(true_y, pred_y, beta=1.0, average="micro"):
    (pr, rec, f_sc, su) = precision_recall_fscore_support(y_true=true_y, y_pred=pred_y, beta=beta, average=average)
    acc = accuracy_score(y_true=true_y, y_pred=pred_y)
    return acc, pr, rec, f_sc


def k_fold(X: pd.DataFrame, y: pd.Series, n_folds: int, classifier, verbose=False):
    kf = model_selection.KFold(n_splits=n_folds, shuffle=True)
    i_train = 0  # accuracy accumulator for training
    i_test = 0  # accuracy accumulator for test
    j = 1  # counter
    max_score = 0
    curr_test_score = 0

    test_p_acc = 0  # precision accumulator for test
    test_r_acc = 0  # recall accumulator for test
    test_f_acc = 0  # f measure accumulator for test

    for train_indexes, test_indexes in kf.split(X, y):
        curr_classifier = clone(classifier)
        curr_classifier = curr_classifier.fit(X.iloc[train_indexes], y[train_indexes])

        # score == acc
        curr_train_score = curr_classifier.score(X.iloc[train_indexes], y[train_indexes])
        curr_test_score = curr_classifier.score(X.iloc[test_indexes], y[test_indexes])

        true_y = y[test_indexes]
        pred_y = curr_classifier.predict(X.iloc[test_indexes])

        acc, curr_test_p, curr_test_r, curr_test_f = calc_classifier_scores(true_y=true_y, pred_y=pred_y)

        if verbose:
            print("Fold " + str(j) + "/" + str(n_folds))
            print("--------MODEL " + str(j) + " QUALITY--------")

            print("-------| Training |-----------")

            print_classifier_scores(true_y=y[train_indexes],
                                    pred_y=curr_classifier.predict(X.iloc[train_indexes]))

            print("-------|   Test   |-----------")
            print_classifier_scores(true_y=true_y, pred_y=pred_y)

        if curr_test_score > max_score:
            best_classifier = curr_classifier
            max_score = curr_test_score

        j += 1
        i_train += curr_train_score
        i_test += curr_test_score

        test_p_acc += curr_test_p
        test_r_acc += curr_test_r
        test_f_acc += curr_test_f

    mean_train_score = i_train / n_folds
    mean_test_score = i_test / n_folds
    mean_p_score = test_p_acc / n_folds
    mean_r_score = test_r_acc / n_folds
    mean_f_score = test_f_acc / n_folds

    return best_classifier, mean_train_score, mean_test_score, mean_p_score, mean_r_score, mean_f_score


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
        best_model, train_score, test_score, test_prec, test_rec, test_f = k_fold(x, y, 10, classifier=KNeighborsClassifier(k),verbose=False)
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
    best_model, train_score, test_score, test_prec, test_rec, test_f = k_fold(X, y, 10, verbose=True, classifier=SVC(kernel='sigmoid'))
    print(str(test_score)) # 0.5


def plot_target_imbalance(y_0, y_1):
    # Plotting the Imbalance
    x = ['Non-Homicide (0)', 'Homicide (1)']
    y = [len(y_0), len(y_1)]

    plt.bar(x, y, color=['green', 'blue', 'red'], width=0.5)
    plt.xlabel('Crime Type')
    plt.ylabel('Count of Crimes')
    plt.title("TARGET FEATURE")
    plt.savefig("../charts/class_imbalance.png", dpi=400)
    plt.clf()

    percentage_of_homicides = len(y_1) / (len(y_0) + len(y_1))
    print(f"Percentage of HOMICIDE: {percentage_of_homicides} %")


def plot_value_counts(feature: pd.Series, title: str):

    value_counts = feature.value_counts()

    plt.bar(value_counts.index, value_counts.array, color=['green', 'blue', 'red'], width=0.5)
    plt.ylabel('Count')
    plt.title(title)
    plt.savefig(f"../charts/{title}_distribution.png", dpi=400)
    plt.clf()


def supervised_main():
    ds_original = pd.read_csv("crimes_selected.csv")
    shoot_original = pd.read_csv("shoot_selected.csv")
    # DROP NULL VALUES ON AVER_AGE
    ds_new = pd.read_csv("working_dataset.csv").dropna(subset=["AVER_AGE"]).reset_index().drop(["index"], axis=1)

    for f in ds_new.columns:
        print(f)

    # Print original incident feature value frequencies
    plot_value_counts(shoot_original["INCIDENT"], "INCIDENT")

    # Print feature imbalance
    plot_target_imbalance(ds_new[ds_new['IS_HOMICIDE'] == 0], ds_new[ds_new['IS_HOMICIDE'] == 1])

    # extract info for trees
    X: pd.DataFrame = ds_new.drop(columns=["CASE_NUMBER", "NUM_OF_DEAD", "IS_KILLED_A_CHILD",
                                           "IS_HOMICIDE", "VICTIM_RACE", "ARRESTED_RACE", "VICTIM_SEX"])
    y: pd.Series = ds_new["IS_HOMICIDE"]

    #tree_training(X, y)  # result -> the best criterion is entropy
    #random_forest_training(X, y)
    #random_forest_training_depth(X, y)
    #ada_boost_training(X, y)
    #gradient_boosting_training(X, y)

    # save_best_models_trees(X, y)

    # prepare data for Naive Bayes
    X_nb, y_nb = prepare_dataset_for_nb(ds_original, ds_new)
    # nb_categorical_training(X_nb, y_nb)
    # nb_with_dropping_column(X_nb, y_nb)

    # hill_climbing_feature_addition(pd.DataFrame(X_nb["Location Description"]), X_nb, y)

    df_final = pd.read_csv("working_dataset_final.csv").dropna(subset=["AVER_AGE"]).reset_index().drop(["index"], axis=1)
    X_final = df_final.drop(columns=["CASE_NUMBER", "NUM_OF_DEAD", "IS_KILLED_A_CHILD",
                                       "IS_HOMICIDE", "VICTIM_RACE", "ARRESTED_RACE", "VICTIM_SEX"], axis=1)
    y_final = df_final["IS_HOMICIDE"]

    tree_training(X_final, y_final, directory="final/")
    random_forest_training(X_final, y_final, directory="final/")
    random_forest_training_depth(X_final, y_final, directory="final/")
    ada_boost_training(X_final, y_final, directory="final/")
    gradient_boosting_training(X_final, y_final, directory="final/")



def save_best_models_trees(X, y):

    # INITIAL TREE BASED
    best_tree, train_sc, test_sc, \
    test_prec, test_rec, test_f = k_fold(X, y, 10,
                                         classifier=DecisionTreeClassifier(max_depth=5, criterion="entropy"))


    print(" ------| Feature importance - Tree |------")
    for feature, importance in zip(X.columns, best_tree.feature_importances_):
        print(f"\t{feature}: {importance}")


    # RANDOM FOREST
    best_forest, train_sc, test_sc, \
    test_prec, test_rec, test_f = k_fold(X, y, 10,
                                         classifier=RandomForestClassifier(max_depth=5, criterion="entropy"))

    print(" ------| Feature importance - Forest |------")
    for feature, importance in zip(X.columns, best_forest.feature_importances_):
        print(f"\t{feature}: {importance}")

    # ADA BOOST
    best_ada, train_sc, test_sc, \
    test_prec, test_rec, test_f = k_fold(X, y, 10,
                                         classifier=AdaBoostClassifier(n_estimators=20))

    print(" ------| Feature importance - AdaBoost |------")
    for feature, importance in zip(X.columns, best_ada.feature_importances_):
        print(f"\t{feature}: {importance}")

    # GRADIENT
    best_grad, train_sc, test_sc, \
    test_prec, test_rec, test_f = k_fold(X, y, 10,
                                         classifier=GradientBoostingClassifier(n_estimators=15))

    print(" ------| Feature importance - GradientBoosting |------")
    for feature, importance in zip(X.columns, best_grad.feature_importances_):
        print(f"\t{feature}: {importance}")



def prepare_dataset_for_nb(ds_original: pd.DataFrame, ds_new: pd.DataFrame):
    complete_df: pd.DataFrame = pd.merge(ds_original, ds_new, on="CASE_NUMBER")

    encoder = LabelEncoder()
    encoder_beat = LabelEncoder()
    encoder_sex = LabelEncoder()
    encoder_race = LabelEncoder()
    encoder_age = LabelEncoder()

    df_for_nb = complete_df.drop(
        ["CASE_NUMBER", "Date", "Block", "Latitude", "Longitude", "NUM_CRIMES_DISTRICT", "NUM_CRIMES_BEAT",
         "NUM_CRIMES_COMM_AREA", "NUM_CRIMES_WARD", "NUM_CRIMES_BLOCK", "NUM_CRIMES_ZIP_CODE", "NUM_CRIMES_STREET_ORG",
         "AVG_NUM_CHARGES", "AREA_INCOME", "AREA_ASSAULT_HOMICIDE", "AREA_FIREARM", "AREA_POVERTY_HEALTH",
         "AREA_HIGH_SCHOOL_DIPLOMA", "AREA_UNEMPLOYMENT", "AREA_BIRTH_RATE", "NUM_OF_DEAD", "NUM_OF_VICTIMS",
         "IS_KILLED_A_CHILD", "MULTIPLE_ARRESTS"], axis=1)
    df_for_nb["AVER_AGE"] = df_for_nb["AVER_AGE"].apply(lambda x: x - (x % 10))

    df_for_nb["Location Description"] = encoder.fit_transform(df_for_nb["Location Description"])
    df_for_nb["Beat"] = encoder_beat.fit_transform(df_for_nb["Beat"])
    df_for_nb["VICTIM_SEX"] = encoder_sex.fit_transform(df_for_nb["VICTIM_SEX"])

    df_for_nb["VICTIM_RACE"] = encoder_race.fit_transform(df_for_nb["VICTIM_RACE"])
    df_for_nb["ARRESTED_RACE"] = encoder_race.transform(df_for_nb["ARRESTED_RACE"])
    df_for_nb["AVER_AGE"] = encoder_age.fit_transform(df_for_nb["AVER_AGE"])

    # start counting from 0 for naive bayes
    df_for_nb["NUM_OF_ARREST"] = df_for_nb["NUM_OF_ARREST"] - 1

    X = df_for_nb.drop(["IS_HOMICIDE"], axis=1)
    y = df_for_nb["IS_HOMICIDE"]

    #for column in X.columns:
    #    print(f"Column - {column} - n. values {X.nunique()[column]}")

    return X, y


# tree for each criterion -> depth in [3, 25]
def tree_training(X: pd.DataFrame, y: pd.Series, directory=""):
    for crit in {"gini", "entropy", "log_loss"}:
        print(f"Criterion: {crit}")

        mean_train_score = []
        mean_test_score = []
        mean_test_p = []
        mean_test_r = []
        mean_test_f = []

        for i in range(3, 26):
            best_tree, train_sc, test_sc, test_prec, test_rec, test_f = k_fold(X, y, 10,
                                                    classifier=DecisionTreeClassifier(max_depth=i, criterion=crit))
            mean_train_score.append(train_sc)
            mean_test_score.append(test_sc)
            mean_test_p.append(test_prec)
            mean_test_r.append(test_rec)
            mean_test_f.append(test_f)

        save_plot_scores([i for i in range(3, 26)], mean_train_score, mean_test_score, "Tree Depth", imgname=f"{directory}tree_{crit}")
        print(f"Media test acc: {np.average(mean_test_score)}")
        print(f"Media test prec: {np.average(mean_test_p)}")
        print(f"Media test rec: {np.average(mean_test_r)}")
        print(f"Media test f-measure: {np.average(mean_test_f)}")


def nb_categorical_training(X: pd.DataFrame, y: pd.Series):
    best_nb, train_sc, test_sc, test_prec, test_rec, test_f = k_fold(
        X, y, 10, CategoricalNB(min_categories=X.nunique()), verbose=True)

    print(f"Media test acc: {test_sc}")
    print(f"Media test prec: {np.average(test_prec)}")
    print(f"Media test rec: {np.average(test_rec)}")
    print(f"Media test f-measure: {np.average(test_f)}")


def nb_with_dropping_column(X: pd.DataFrame, y: pd.Series):

    for column in X.columns:

        print(f"---------| Dropping {column} |-------")
        X_reduced = X.drop([column], axis=1)
        best_nb, train_sc, test_sc, test_prec, test_rec, test_f = k_fold(
                    X_reduced, y, 10, CategoricalNB(min_categories=X_reduced.nunique()))

        print("Score train: " + str(train_sc))
        print("Score test: " + str(test_sc))


def hill_climbing_feature_addition(X_start: pd.DataFrame, X_complete: pd.DataFrame, y: pd.Series, n_folds=10):
    best_nb, train_sc, test_sc, test_prec, test_rec, test_f = k_fold(
                    X_start, y, n_folds, CategoricalNB(min_categories=X_start.nunique()))
    print(f"Initial Scores: \n\tTR: {train_sc} \n\tTE: {test_sc}")

    while len(X_complete.columns) > len(X_start.columns):
        column_scores = {}
        for column in X_complete.columns:
            if column not in X_start.columns:
                X_augmented = X_start.assign(columns=X_complete[column])
                best_nb, train_sc, test_sc, test_prec, test_rec, test_f = k_fold(
                                X_augmented, y, 10, CategoricalNB(min_categories=X_augmented.nunique()))
                column_scores[column] = (train_sc, test_sc)

        best_feature = max(column_scores, key=lambda x: column_scores[x][1])
        X_start[best_feature] = X_complete[best_feature]
        print(f"---------| Adding {best_feature} |-------")
        best_nb, train_sc, test_sc, test_prec, test_rec, test_f = k_fold(
            X_start, y, 10, CategoricalNB(min_categories=X_start.nunique()))
        print("Score train: " + str(train_sc))
        print("Score test: " + str(test_sc))


# num of classifiers 5, 10, 15, ..., 150
def random_forest_training(X: pd.DataFrame, y: pd.Series, directory=""):

    print(f"Random Forest - Criterion: entropy")

    mean_train_score = []
    mean_test_score = []
    mean_test_p = []
    mean_test_r = []
    mean_test_f = []

    for i in range(5, 151, 5):
        best_forest, train_sc, test_sc, test_prec, test_rec, test_f = k_fold(
                    X, y, 10, classifier=RandomForestClassifier(n_estimators=i, criterion="entropy"))
        mean_train_score.append(train_sc)
        mean_test_score.append(test_sc)
        mean_test_p.append(test_prec)
        mean_test_r.append(test_rec)
        mean_test_f.append(test_f)

    save_plot_scores([i for i in range(5, 151, 5)], mean_train_score, mean_test_score, "Num of trees", imgname=f"{directory}forest_num_class")
    print(f"Media test acc: {np.average(mean_test_score)}")
    print(f"Media test prec: {np.average(mean_test_p)}")
    print(f"Media test rec: {np.average(mean_test_r)}")
    print(f"Media test f-measure: {np.average(mean_test_f)}")


def random_forest_training_depth(X: pd.DataFrame, y: pd.Series, directory=""):
    print(f"Random Forest - Criterion: entropy - Varying estimators' depth")

    mean_train_score = []
    mean_test_score = []
    mean_test_p = []
    mean_test_r = []
    mean_test_f = []

    for i in range(3, 26):
        best_forest, train_sc, test_sc, test_prec, test_rec, test_f = k_fold(
            X, y, 10, classifier=RandomForestClassifier(max_depth=i, criterion="entropy"))
        mean_train_score.append(train_sc)
        mean_test_score.append(test_sc)
        mean_test_p.append(test_prec)
        mean_test_r.append(test_rec)
        mean_test_f.append(test_f)

    save_plot_scores([i for i in range(3, 26)], mean_train_score, mean_test_score, "Trees' Depth",
                     imgname=f"{directory}forest_depth")
    print(f"Media test acc: {np.average(mean_test_score)}")
    print(f"Media test prec: {np.average(mean_test_p)}")
    print(f"Media test rec: {np.average(mean_test_r)}")
    print(f"Media test f-measure: {np.average(mean_test_f)}")


def ada_boost_training(X: pd.DataFrame, y: pd.Series, directory=""):
    mean_train_score = []
    mean_test_score = []
    mean_test_p = []
    mean_test_r = []
    mean_test_f = []
    print("AdaBoost")
    for i in range(5, 151, 5):
        best_ada_boost, train_sc, test_sc, test_prec, test_rec, test_f = k_fold(
            X, y, 10, classifier=AdaBoostClassifier(n_estimators=i))
        mean_train_score.append(train_sc)
        mean_test_score.append(test_sc)
        mean_test_p.append(test_prec)
        mean_test_r.append(test_rec)
        mean_test_f.append(test_f)

    save_plot_scores([i for i in range(5, 151, 5)], mean_train_score, mean_test_score, "Num of trees",
                     imgname=f"{directory}ada_boost")

    print(f"Media test acc: {np.average(mean_test_score)}")
    print(f"Media test prec: {np.average(mean_test_p)}")
    print(f"Media test rec: {np.average(mean_test_r)}")
    print(f"Media test f-measure: {np.average(mean_test_f)}")


def gradient_boosting_training(X: pd.DataFrame, y: pd.Series, directory=""):
    for loss in {"exponential", "log_loss"}:
        mean_train_score = []
        mean_test_score = []
        mean_test_p = []
        mean_test_r = []
        mean_test_f = []
        print(f"Gradient Boosting Classifier - Loss: {loss}")
        for i in range(5, 151, 5):
            best_grad_boost, train_sc, test_sc, test_prec, test_rec, test_f = k_fold(
                        X, y, 10, classifier=GradientBoostingClassifier(n_estimators=i, loss=loss))
            mean_train_score.append(train_sc)
            mean_test_score.append(test_sc)
            mean_test_p.append(test_prec)
            mean_test_r.append(test_rec)
            mean_test_f.append(test_f)

        save_plot_scores([i for i in range(5, 151, 5)], mean_train_score, mean_test_score, "Num of trees",
                         imgname=f"{directory}grad_boost_{loss}")

        print(f"Media test acc: {np.average(mean_test_score)}")
        print(f"Media test prec: {np.average(mean_test_p)}")
        print(f"Media test rec: {np.average(mean_test_r)}")
        print(f"Media test f-measure: {np.average(mean_test_f)}")


def save_plot_scores(x_values, train_scores, test_scores, to_print, imgname):
    fig, ax = plt.subplots()

    ax.plot(x_values, train_scores)
    ax.plot(x_values, test_scores)

    plt.xlabel(to_print)
    plt.ylabel('Scores')
    plt.ylim(0, 1)
    plt.title("Training and test scores")
    plt.savefig(f"../charts/{imgname}.png", dpi=400)
    plt.clf()


supervised_main()
