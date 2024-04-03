import json
import pandas as pd
from neural_networks import CustomNN
from clearml import Task, InputModel, OutputModel, Dataset


PROJECT_NAME = "ProjectX"


def train_model(task, dataset, params):
    dataset_metadata = dataset.get_metadata()
    dataset_path = dataset.get_local_copy()
    data = pd.read_csv(dataset_path + "/dataset.csv")
    with open(dataset_path + "/labels.json", "r") as f:
        labels = json.load(f)
    if 'Models/input_model_id' in params:
        input_model = InputModel(params['Models/input_model_id'])
        if input_model.labels != labels:
            raise AssertionError("Label enumeration does not match")
        config = input_model.config_dict
        config['input_model_id'] = params['Models/input_model_id']
        network = CustomNN.from_file(input_model.get_weights())
    else:
        config = {
            'input_size':   dataset_metadata['input_size'],
            'output_size':  dataset_metadata['output_size'],
            'hidden_size':  params['Models/hidden_layer_size'],
            'hidden_count': params['Models/hidden_layer_count'],
            'random_seed':  params['Models/seed']
        }
        network = CustomNN(**config)
    network.train(
        training_data=data[10:],
        testing_data=data[:10],
        iterations=params['Args/iterations'],
        learning_rate=params['Args/learning_rate'],
        batch_size=params['Args/batch_size'],
        seed=params['Args/seed'],
        logger=task.get_logger()
    )
    network.save_to_file("weights.json")
    output_model = OutputModel(
        task=task,
        name=params['Models/output_model_name'],
        framework="CustomNN",
        label_enumeration=labels,
        config_dict=config
    )
    output_model.update_weights()
    output_model.wait_for_uploads()


def run_task():
    task_id = input("Введите ID эксперимента: ")
    task = Task.get_task(task_id=task_id)
    task.mark_started()
    params = task.get_parameters()
    dataset = Dataset.get(dataset_id=params['Datasets/dataset_id'])
    return task, dataset, params


def new_task():
    task_name = input("Введите название эксперимента: ")
    task = Task.init(project_name=PROJECT_NAME, task_name=task_name)
    dataset_id = input("Введите ID датасета: ")
    dataset = Dataset.get(dataset_id=dataset_id)
    input_model_id = input("Введите ID входной модели (0 - создать новую): ")
    if input_model_id == "0":
        print("Введите параметры модели")
        model_params = {
            'Models/hidden_layer_size':     int(input("\tРазмер скрытых слоёв: ")),
            'Models/hidden_layer_count':    int(input("\tКол-во скрытых слоёв: ")),
            'Models/seed':                  int(input("\tСемя: "))
        }
    else:
        model_params = {
            'Models/input_model_id': input_model_id
        }
        task.set_input_model(model_id=input_model_id)
    output_model_name = input("Введите название выходной модели: ")
    print("Введите параметры")
    params = {
        'Args/iterations':          int(input("\tИтерации: ")),
        'Args/learning_rate':       float(input("\tСкорость обучения: ")),
        'Args/batch_size':          int(input("\tРазмер частей: ")),
        'Args/seed':                int(input("\tСемя: ")),
        'Datasets/dataset_id':      dataset_id,
        'Models/output_model_name': output_model_name
    }
    params.update(model_params)
    task.set_parameters(params)
    return task, dataset, params


def main():
    inp = input("Введите 1, чтобы создать эксперимент, 2 - выполнить существующий эксперимент: ")
    if inp == "1": task, dataset, params = new_task()
    elif inp == "2": task, dataset, params = run_task()
    else: raise ValueError("Invalid input")
    train_model(task, dataset, params)
    task.close()


if __name__ == "__main__":
    main()
