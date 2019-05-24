from allennlp.training.metrics import F1Measure


def get_metrics(obj, reset):
    result = {}
    f1_sum = 0
    f1_count = 0
    for name, metric in obj.metrics.items():
        if name.startswith("f1"):
            if name.endswith("NONE_CHAR"):
                continue
            # With only true_negatives it could be 0 and break a metric
            if metric._true_positives + metric._false_positives + metric._false_negatives > 0:
                precision, recall, f1_measure = metric.get_metric(reset=reset)
                f1_sum += f1_measure
                f1_count += 1

                if obj._verbose_metrics:
                    result[name] = f1_measure
        else:
            result[name] = metric.get_metric(reset=reset)
    if f1_count > 0:
        result['f1_macro'] = f1_sum / f1_count

    return result

def add_f1(model):
    for label, index in model.vocab.get_token_to_index_vocabulary('labels').items():
        model.metrics["f1_" + label.replace(' ', '_')] = F1Measure(index)