import os
import subprocess
import shlex
import time

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
