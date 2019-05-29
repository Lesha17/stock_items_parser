import pandas as pd
import matplotlib.pyplot as plt
import os

output = "output/eval"
validation_file_name = "validate.txt"
train_file_name = "train.txt"
test_file_name = "test.txt"

datasets = ["krepmarket", "exists_ru"]
train_sizes = ["0_0001", "0_001", "0_002", "001", "005", "02", "067"]
first_layers = ["lstm", "cnn"]
second_layers = ["ff_proj", "lstm_proj", "pt_crf", "lstm_crf"]

train_sizes_dict = { "067": 0.67, "02": 0.2, "005": 0.05, "001": 0.01, "0_002": 0.002, "0_001": 0.001, "0_0001": 0.0001 }

def read_evals(callback):
    for first_layer in first_layers:
        for second_layer in second_layers:
            for dataset_name in datasets:
                for train_size in train_sizes:
                    validation_path = "{}/{}_{}/{}/{}/{}".format(output, first_layer, second_layer, dataset_name, train_size, validation_file_name)
                    train_path = "{}/{}_{}/{}/{}/{}".format(output, first_layer, second_layer, dataset_name,
                                                                 train_size, train_file_name)
                    test_path = "{}/{}_{}/{}/{}/{}".format(output, first_layer, second_layer, dataset_name,
                                                                 train_size, test_file_name)
                    if not os.path.isfile(validation_path):
                        print("No such file: {}".format(validation_path))
                        continue
                    metrics_validation = pd.read_json(validation_path, orient="records", typ='series', convert_dates=False)
                    metrics_train = pd.read_json(train_path, orient="records", typ='series',
                                                      convert_dates=False)
                    metrics_test = pd.read_json(test_path, orient="records", typ='series',
                                                      convert_dates=False)

                    callback(first_layer, second_layer, dataset_name, train_size, metrics_train, metrics_test, metrics_validation)

def make_excel_table_of_f1():
    rows_by_train_size = {}
    def consume(first_layer, second_layer, dataset_name, train_size, metrics_train, metrics_test, metrics_validation):
        if train_size not in rows_by_train_size:
            rows_by_train_size[train_size] = {}
        rows = rows_by_train_size[train_size]
        if second_layer not in rows:
            rows[second_layer] = {}
        row = rows[second_layer]
        row["train_size"] = train_size

        train = metrics_train['f1_macro']
        test = metrics_test['f1_macro']
        validation = metrics_validation['f1_macro']
        row["{}_{}".format(first_layer, dataset_name)] = "{:.3f} / {:.3f} / {:.3f}".format(train, test, validation)
        row["second_layer"] = second_layer

    read_evals(consume)

    rows = []
    for train_size, rows_for_train_size in rows_by_train_size.items():
        for second_layer, row in rows_for_train_size.items():
            rows.append((train_size, second_layer, row))
    rows.sort(key = lambda x: (x[0], x[1]))

    df = pd.DataFrame(columns=["train_size", "cnn_exists_ru", "lstm_exists_ru", "cnn_krepmarket", "lstm_krepmarket"])
    for r in rows:
        df = df.append(r[2], ignore_index=True)
    df.to_excel('output/f1_table.xlsx')

def plot(dataset_name):
    x_by_model = {}
    y_by_model = {}
    def consume(first_layer, second_layer, dset_name, train_size, metrics_train, metrics_test, metrics_validation):
        if dset_name != dataset_name:
            return
        model_name = "{}_{}".format(first_layer, second_layer)
        x = train_sizes_dict[train_size]
        y = metrics_validation['f1_macro']

        if model_name not in x_by_model:
            x_by_model[model_name] = []

        if model_name not in y_by_model:
            y_by_model[model_name] = []

        x_by_model[model_name].append(x)
        y_by_model[model_name].append(y)

    read_evals(consume)

    linestyles = ['-', '--', '-.', ':']
    colors = ['k', '#aaffaa', 'r']
    i = 0

    # And plot stuff there
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111)
    for model, x in x_by_model.items():
        print("Plotting for {}".format(model))
        ls = linestyles[i % len(linestyles)]
        c = colors[i // len(colors)]
        y = y_by_model[model]
        ax.semilogx(x, y, label = model, linestyle = ls, color = c, linewidth = 2)
        ax.legend()
        i += 1

    plt.show(block=True)


make_excel_table_of_f1()
plot('exists_ru')
plot('krepmarket')



