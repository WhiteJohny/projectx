import json
import os
import warnings
import pandas as pd
from clearml import Task, InputModel, OutputModel, Dataset
from src.model.neural_networks import CustomNN


PROJECT_NAME = "ProjectX"


# убирает предупреждения о больших числах в вычислениях от NumPy
warnings.filterwarnings("ignore", "overflow encountered in exp", RuntimeWarning)


def train_model(task, dataset, params):
    dataset_metadata = dataset.get_metadata()
    dataset_path = dataset.get_local_copy()
    data = pd.read_csv(dataset_path + "/dataset.csv")
    if 'Models/input_model_id' in params:
        input_model = InputModel(params['Models/input_model_id'])
        labels = input_model.labels
        config = input_model.config_dict
        config['input_model_id'] = params['Models/input_model_id']
        network = CustomNN.from_file(input_model.get_weights())
    else:
        with open(dataset_path + "/labels.json", "r") as f:
            labels = json.load(f)
        config = {
            'input_size':   int(dataset_metadata['input_size']),
            'output_size':  int(dataset_metadata['output_size']),
            'hidden_size':  int(params['Models/hidden_layer_size']),
            'hidden_count': int(params['Models/hidden_layer_count']),
            'random_seed':  int(params['Models/seed'])
        }
        network = CustomNN(**config)
    network.train(
        training_data=data[10:],
        testing_data=data[:10],
        iterations=int(params['Args/iterations']),
        learning_rate=float(params['Args/learning_rate']),
        batch_size=int(params['Args/batch_size']),
        seed=int(params['Args/seed']),
        logger=task.get_logger()
    )
    network.save_to_file("model.json")
    output_model = OutputModel(
        task=task,
        name=params['Models/output_model_name'],
        framework="CustomNN",
        label_enumeration=labels,
        config_dict=config
    )
    output_model.update_weights(
        weights_filename="model.json",
        async_enable=False,
        upload_uri="https://files.clear.ml"
    )
    os.remove("model.json")


def run_task():
    task_id = input("Введите ID эксперимента: ")
    task = Task.get_task(task_id=task_id)
    task.mark_started()
    params = task.get_parameters()
    dataset = Dataset.get(dataset_id=params['Datasets/dataset_id'])
    train_model(task, dataset, params)
    task.mark_completed()


def new_task():
    task_name = input("Введите название эксперимента: ")
    task = Task.init(project_name=PROJECT_NAME, task_name=task_name)
    dataset_id = input("Введите ID датасета: ")
    dataset = Dataset.get(dataset_id=dataset_id, alias="dataset_id")
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
    train_model(task, dataset, params)
    task.close()


def main():
    inp = input("Введите 1, чтобы создать эксперимент, 2 - выполнить существующий эксперимент: ")
    if inp == "1": new_task()
    elif inp == "2": run_task()
    else: raise ValueError("Invalid input")


if __name__ == "__main__":
    main()
