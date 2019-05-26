from allennlp.training.metrics import F1Measure

def get_metrics(obj, reset):
    f1_sum = 0
    f1_count = 0
    for f1 in obj.f1_metrics:
        if f1._true_positives + f1._false_positives + f1._false_negatives > 0:
            precision, recall, f1_measure = f1.get_metric()
            f1_sum += f1_measure
            f1_count += 1

    metrics = super(obj.__class__, obj).get_metrics(reset=reset)
    result = {}

    for name, metric_value in metrics.items():
        if name in obj.f1_metric_names:
            if obj._verbose_metrics:
                result[name] = f1_measure
        else:
            result[name] = metric_value

    if f1_count > 0:
        result['f1_macro'] = f1_sum / f1_count

    return result

def add_f1(model):
    model.f1_metrics = []
    model.f1_metric_names = []
    for label, index in model.vocab.get_token_to_index_vocabulary('labels').items():
        if not label.endswith("NONE_CHAR"):
            f1 = F1Measure(index)
            metric_name = "f1_" + label.replace(' ', '_')
            model.metrics[metric_name] = f1
            model.f1_metrics.append(f1)
            model.f1_metric_names.append(metric_name)
    model.f1_metric_names = set(model.f1_metric_names)
