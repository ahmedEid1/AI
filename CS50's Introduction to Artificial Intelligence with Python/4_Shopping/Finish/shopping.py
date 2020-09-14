import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():
    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    evidence = []
    labels = []

    with open(filename, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        line_count = -1
        for row in csv_reader:
            if line_count == -1:
                line_count += 1
            else:
                new_row = row.copy()
                # 1
                for word in ['Administrative', 'Informational', 'ProductRelated', 'OperatingSystems', 'Browser'
                    , 'Region', 'TrafficType']:
                    new_row[word] = int(new_row[word])
                # 2
                for word in ['Administrative_Duration', 'Informational_Duration', 'ProductRelated_Duration',
                             'BounceRates', 'ExitRates', 'PageValues', 'SpecialDay']:
                    new_row[word] = float(new_row[word])
                # 3
                month_dict = {"Jan": 0,
                              "Feb": 1,
                              "Mar": 2,
                              "Apr": 3,
                              "May": 4,
                              "June": 5,
                              "Jul": 6,
                              "Aug": 7,
                              "Sep": 8,
                              "Oct": 9,
                              "Nov": 10,
                              "Dec": 11
                              }
                new_row['Month'] = month_dict[new_row['Month']]
                # 4
                if new_row['VisitorType'] == "Returning_Visitor":
                    new_row['VisitorType'] = 1
                else:
                    new_row['VisitorType'] = 0
                # 5
                if new_row['Weekend']:
                    new_row['Weekend'] = 1
                else:
                    new_row['Weekend'] = 0
                # 6
                if new_row['Revenue'] == "TRUE":
                    new_row['Revenue'] = 1
                else:
                    new_row['Revenue'] = 0
                # adding to the lists
                labels.append(new_row['Revenue'])
                customer = []
                for column in ['Administrative', 'Administrative_Duration', 'Informational', 'Informational_Duration',
                               'ProductRelated', 'ProductRelated_Duration', 'BounceRates', 'ExitRates', 'PageValues',
                               'SpecialDay', 'Month', 'OperatingSystems', 'Browser', 'Region', 'TrafficType',
                               'VisitorType'
                    , 'Weekend']:
                    customer.append(new_row[column])
                evidence.append(customer)

                line_count += 1

    return evidence, labels


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)

    x_training = [customer for customer in evidence]
    y_training = [label for label in labels]
    model.fit(x_training, y_training)

    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    sensitivity = 0
    specificity = 0
    total_positive = 0
    positive = 0
    total_negative = 0
    negative = 0

    for actual, predict in zip(labels, predictions):
        if actual == 1:
            total_positive += 1
            if predict == 1:
                positive += 1
        if actual == 0:
            total_negative += 1
            if predict == 0:
                negative += 1
    if total_negative == 0:
        specificity = 0
    else:
        specificity = negative / total_negative
    if total_positive == 0:
        sensitivity = 0
    else:
        sensitivity = positive / total_positive

    return sensitivity, specificity


if __name__ == "__main__":
    main()
