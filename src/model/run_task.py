import json
import os
import warnings
import pandas as pd
from clearml import Task, InputModel, OutputModel, Dataset
from sklearn.exceptions import DataConversionWarning
from src.model.neural_networks import FRAMEWORKS
from src.model.nlp import processing_dataset


PROJECT_NAME = "ProjectX"


# убирает предупреждения
warnings.filterwarnings("ignore", "overflow encountered in exp", RuntimeWarning)
warnings.filterwarnings("ignore", "A column-vector y was passed when a 1d array was expected", DataConversionWarning)


def train_model(task, dataset, params):
    dataset_metadata = dataset.get_metadata()
    dataset_path = dataset.get_local_copy()
    data = pd.read_csv(dataset_path + "/dataset.csv")
    if 'Models/input_model_id' in params:
        input_model = InputModel(params['Models/input_model_id'])
        labels = input_model.labels
        config = input_model.config_dict
        config['input_model_id'] = params['Models/input_model_id']
        framework_name = input_model.framework
        try:
            framework = FRAMEWORKS[framework_name]
        except KeyError:
            raise NotImplementedError(f"{framework_name} framework not implemented")
        network = framework.from_file(input_model.get_weights())
    else:
        with open(dataset_path + "/labels.json", "r") as f:
            labels = json.load(f)
        framework_name = params['Models/framework']
        try:
            framework = FRAMEWORKS[framework_name]
        except KeyError:
            raise NotImplementedError(f"{framework_name} framework not implemented")
        config = {
            'input_size':   int(dataset_metadata['input_size']),
            'output_size':  int(dataset_metadata['output_size']),
            'hidden_size':  int(params['Models/hidden_layer_size']),
            'hidden_count': int(params['Models/hidden_layer_count']),
            'random_seed':  int(params['Models/seed'])
        }
        network = framework(**config)
    network.train(
        training_data=data[10:],
        testing_data=data[:10],
        iterations=int(params['Args/iterations']),
        learning_rate=float(params['Args/learning_rate']),
        batch_size=int(params['Args/batch_size']),
        seed=int(params['Args/seed']),
        logger=task.get_logger()
    )
    filename = "model" + framework.FILE_EXTENSION
    network.save_to_file(filename)
    output_model = OutputModel(
        task=task,
        name=params['Models/output_model_name'],
        framework=framework_name,
        label_enumeration=labels,
        config_dict=config
    )
    output_model.update_weights(
        weights_filename=filename,
        async_enable=False,
        upload_uri="https://files.clear.ml"
    )
    os.remove(filename)


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
        print("Доступные фреймворки")
        for frame in FRAMEWORKS: print("\t" + frame)
        framework_name = input("Введите фреймворк модели: ")
        if framework_name not in FRAMEWORKS:
            raise ValueError("invalid framework")
        print("Введите параметры модели")
        model_params = {
            'Models/framework':             framework_name,
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
    inp = input("""Меню
\t1 - создать эксперимент
\t2 - выполнить существующий эксперимент
\t3 - обработать датасет
Выберите пункт из меню: """)
    if inp == "1": new_task()
    elif inp == "2": run_task()
    elif inp == "3": processing_dataset(
        input("Введите ID необработанного датасета: "),
        int(input("Введите размер, до которого обрезать вектора входных данных в датасете: "))
    )
    else: raise ValueError("Invalid input")


if __name__ == "__main__":
    main()
