from collections import Counter
from linear_algebra import distance
from stats import mean
import math
import random
import matplotlib.pyplot as plt


def majority_vote(labels):
    """assumes that labels are ordered from nearest to farthest"""
    vote_counts = Counter(labels)
    winner, winner_count = vote_counts.most_common(1)[0]
    num_winners = len([count
                       for count in vote_counts.values()
                       if count == winner_count])

    if num_winners == 1:
        return winner                     # unique winner, so return it
    else:
        return majority_vote(labels[:-1])  # try again without the farthest


def knn_scikit(k, labeled_points, new_point):
    from sklearn.neighbors import KNeighborsClassifier
    kn_clf = KNeighborsClassifier(n_neighbors=k)
    X = [[city[0][0], city[0][1]] for city in labeled_points]
    y = [city[1] for city in labeled_points]
    kn_clf.fit(X, y)
    y_pred = kn_clf.predict([[new_point[0], new_point[1]]])
    return y_pred


def knn_classify(k, labeled_points, new_point):
    """each labeled point should be a pair (point, label)"""

    # order the labeled points from nearest to farthest
    by_distance = sorted(labeled_points,
                         key=lambda point_label: distance(point_label[0], new_point))

    # find the labels for the k closest
    k_nearest_labels = [label for _, label in by_distance[:k]]

    # and let them vote
    return majority_vote(k_nearest_labels)


def predict_preferred_language_by_city(k_values, cities):
    """
    TODO
    predicts a preferred programming language for each city using above knn_classify() and
    counts if predicted language matches the actual language.
    Finally, print number of correct for each k value using this:
    print(k, "neighbor[s]:", num_correct, "correct out of", len(cities))
    """
    num_correct = 0
    print("Classification: ")
    for k in k_values:
        num_correct = 0
        for i in range(len(cities)):
            cities_list = cities.copy()
            del cities_list[i]
            pred = knn_classify(k, cities_list, cities[i][0])
            # pred = knn_scikit(k, cities_list, cities[i][0])
            if(pred == cities[i][1]):
                num_correct += 1
        print(k, "neighbor[s]:", num_correct, "correct out of", len(cities))

    print("Classification using scikit: ")
    for k in k_values:
        num_correct = 0
        for i in range(len(cities)):
            cities_list = cities.copy()
            del cities_list[i]
            pred = knn_scikit(k, cities_list, cities[i][0])
            if(pred == cities[i][1]):
                num_correct += 1
        print(k, "neighbor[s]:", num_correct, "correct out of", len(cities))


if __name__ == "__main__":
    k_values = [1, 3, 5, 7]
    # TODO
    # Import cities from data.py and pass it into predict_preferred_language_by_city(x, y).
    from data import cities as cities
    predict_preferred_language_by_city(k_values, cities)
