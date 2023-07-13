import os
import subprocess
import shlex
import time
import json
import tensorrt as trt
#import pycuda.autoinit
#import pycuda.driver as cuda

def run_object_detection(path, experiment, test_video, min_conf):
    weights = f"{path}/runs/train/{experiment}/weights/best.pt"
    command = f"python detect.py --source {test_video} --conf {min_conf}  --weights {weights}"
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

    while True:
        output = process.stdout.readline().decode().strip()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output)

    if process.poll() is None:
        process.kill()

def run_train_yolo(batch: int, epochs: int, data: str, weights: str, hyp: str = None):
    command = f"python train.py --img 640 --batch {batch} --epochs {epochs} --data {data} --weights {weights}"
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    if hyp is not None:
        command += f" --hyp {hyp}"

    subprocess.run(command, shell=True)



def run_object_detection_warn(path, experiment, test_video, min_conf):
    """
    Aca hay qeue ampliar la funcionalidad de alertas (MIN ACCURACY, WARNING TIMER, etc.)
    """
    weights = f"{path}{experiment}/weights/best.pt"
    command = f"python detect.py --source {test_video} --conf {min_conf}  --weights {weights}"
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

    detection_timer = 0
    detection_interval = 60

    while True:
        output = process.stdout.readline().decode().strip()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output)
            if ("Handgun" in output or "Knife" in output) and detection_timer == 0:
                print("Gun or blade detected.")
                #aca agregar la funcion de MANDAR MSG DE TEXTO

                detection_timer = time.time()

        if detection_timer != 0 and time.time() - detection_timer >= detection_interval:
            detection_timer = 0

    if process.poll() is None:
        process.kill()



def export_yolov5(weights_file, onnx_file, img_size=416, dynamic=False, simplify=True):
    """
    Exports YOLOv5 model to ONNX format using the provided parameters.
    """
    command = f"python export.py --weights {weights_file} --include onnx --imgsz {img_size}"
    if dynamic:
        command += " --dynamic"
    if simplify:
        command += " --simplify"
    command += f" --output {onnx_file}"
    subprocess.run(command, shell=True)


def run_train_yolo_sparse(batch: int, epochs: int, data: str, weights: str, hyp: str = None):
    command = f"python train.py --img 640 --batch {batch} --epochs {epochs} --data {data} --weights {weights}"
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    if hyp is not None:
        command += f" --hyp {hyp}"

    subprocess.run(command, shell=True)


def train_model_magic(data_file, cfg_file, weights, hyp_file, recipe, recipe_args=None, patience=0):
    """
    Trains YOLOv5 using NeuralMagic with the provided parameters.

    Args:
        data_file (str): Path to the data file (custom_data.yaml).
        cfg_file (str): Path to the configuration file (models_v5.0/yolov5s.yaml).
        weights (str): Path to the pre-trained weights or a NeuralMagic recipe.
        hyp_file (str): Path to the hyperparameters file (data/hyps/hyp.finetune.yaml).
        recipe (str): NeuralMagic recipe for fine-tuning the model.
        recipe_args (str or dict): Additional arguments for the NeuralMagic recipe (default: None)."""

    command = f"python train.py --data {data_file} --cfg {cfg_file} --weights {weights} --hyp {hyp_file} --recipe {recipe}"
    if recipe_args:
        if isinstance(recipe_args, dict):
            recipe_args = json.dumps(recipe_args)
        command += f" --recipe-args '{recipe_args}'"
    if patience >= 0:
        command += f" --patience {patience}"
    subprocess.run(command, shell=True)

#train_model_magic(
#    data_file="custom_data.yaml",
#    cfg_file="models_v5.0/yolov5s.yaml",
#    weights="zoo:cv/detection/yolov5-s/pytorch/ultralytics/coco/pruned_quant-aggressive_94?recipe_type=transfer",
#    hyp_file="data/hyps/hyp.finetune.yaml",
#    recipe="zoo:cv/detection/yolov5-s/pytorch/ultralytics/coco/pruned_quant-aggressive_94"
#)

def build_engine(model_file, max_ws=512*1024*1024, fp16=False):
    """with this function we take an ONNX file and convert it to engine, which allows us to use it on tensorRT (optimized for GPU)"""
    print("building engine")
    TRT_LOGGER = trt.Logger(trt.Logger.WARNING)
    builder = trt.Builder(TRT_LOGGER)

    if fp16:
        builder.set_flag(trt.BuilderFlag.FP16)

    config = builder.create_builder_config()
    config.max_workspace_size = max_ws

    #explicit_batch = 1 << int(trt.NetworkDefinitionCreationFlag.EXPLICIT_BATCH)
    explicit_batch = 1 << (int)(trt.NetworkDefinitionCreationFlag.EXPLICIT_BATCH)
    builder.create_network(explicit_batch)
    network = builder.create_network(explicit_batch)
    with trt.OnnxParser(network, TRT_LOGGER) as parser:
        with open(model_file, 'rb') as model:
            parsed = parser.parse(model.read())
            print("network.num_layers", network.num_layers)
            #last_layer = network.get_layer(network.num_layers - 1)
            #network.mark_output(last_layer.get_output(0))
            engine = builder.build_engine(network, config=config)
            return engine

def build_engine_with_trtexec():
    model_path = "best_cam-sim.onnx"
    engine_path = "/notebooks/engine.plan"
    command = ['trtexec', '--onnx={}'.format(model_path), '--saveEngine={}'.format(engine_path),'--explicitBatch','--minShapes=input:1x3x1920x1080','--optShapes=input:4x3x1920x1080','--maxShapes=input:4x3x1920x1080', '--shapes=input:4x3x1920x1080']

    result = subprocess.run(command, stdout=subprocess.PIPE, text=True)

    # Check the command returncode. It is command exit code which indicates the
    # status code - if 0, the command was successful; if non-zero then not
    print(result.returncode)

    # Output the command result to stdout
    print(result.stdout)

#build_engine_with_trtexec()

#engine = build_engine("best_cam-sim.onnx")
