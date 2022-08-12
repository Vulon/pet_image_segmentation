import dataclasses
from dataclasses import dataclass

import yaml


@dataclass
class DatasetConfig:
    coco_categories_map: dict
    coco_train_annotations_url: str
    coco_archive_train_filename: str
    coco_archive_val_filename: str
    raw_files_folder: str
    dataset_files_folder : str

    train_fracture: float
    val_fracture: float
    test_fracture: float

    image_size: int

    
@dataclass
class ModelConfig:
    pretrained_name: str

@dataclass
class TrainingConfig:
    downloaded_datasets_folder: str
    train_mode: str
    container_data_folder: str

    eval_steps: int
    train_batch_size: int
    val_batch_size: int
    epochs: int
    learning_rate: float
    weight_decay: float
    save_steps: int
    fp16: bool
    gradient_accumulation_steps: int
    eval_accumulation_steps: int
    logging_strategy: str
    tensorboard_logs_directory: str
    trainer_checkpoint: str

@dataclass
class AugmentationsConfig:
    rotate_angle: int
    mask_size: int

@dataclass
class BaseConfig:
    random_seed: int
    dataset: DatasetConfig
    model: ModelConfig
    training: TrainingConfig
    augmentations: AugmentationsConfig


def __dataclass_from_dict(klass, d):
    try:
        fieldtypes = {f.name: f.type for f in dataclasses.fields(klass)}
        return klass(**{f: __dataclass_from_dict(fieldtypes[f], d[f]) for f in d})
    except:
        return d  # Not a dataclass field



def get_config_from_dvc() -> BaseConfig:
    import dvc.api

    params = dvc.api.params_show()
    config = __dataclass_from_dict(BaseConfig, params)
    return config


def get_config_from_yaml(yaml_path: str) -> BaseConfig:
    with open(yaml_path, "r") as file:
        yaml_dict = yaml.safe_load(file)
        config = __dataclass_from_dict(BaseConfig, yaml_dict)
        return config
