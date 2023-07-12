from matplotlib import pyplot as plt
import cv2
import glob
import matplotlib.pyplot as plt
import os
import subprocess


def visualizacion_resultados(history):
  epochs = [i for i in range(20)]
  fig, ax = plt.subplots(1,2)
  train_acc = history.history["accuracy"]
  train_loss = history.history["loss"]
  val_acc = history.history["val_accuracy"]
  val_loss = history.history["val_loss"]
  fig.set_size_inches(16,9)

  ax[0].plot(epochs, train_acc, "go-",label = "Accuracy training")
  ax[0].plot(epochs, val_acc, "ro-",label = "Validation accuracy")
  ax[0].set_title("Training and validation accuracy")
  ax[0].legend()
  ax[0].set_xlabel("Epochs")
  ax[0].set_ylabel("Accuracy")

  ax[1].plot(epochs, train_loss, "go-",label = "Training loss")
  ax[1].plot(epochs, val_loss, "ro-",label = "Validation loss")
  ax[1].set_title("Training and validation loss")
  ax[1].legend()
  ax[1].set_xlabel("Epochs")
  ax[1].set_ylabel("Loss")

  plt.show()


class Visualization:
    @classmethod
    def show_valid_results(cls, RES_DIR):
        EXP_PATH = f"runs/train/{RES_DIR}"
        validation_pred_images = glob.glob(f"{EXP_PATH}/*_pred.jpg")
        print(validation_pred_images)
        for pred_image in validation_pred_images:
            image = cv2.imread(pred_image)
            plt.figure(figsize=(19, 16))
            plt.imshow(image[:, :, ::-1])
            plt.axis('off')
            plt.show()

    @classmethod
    def inference(cls, RES_DIR, data_path):
        infer_dir_count = len(glob.glob('runs/detect/*'))
        print(f"Current number of inference detection directories: {infer_dir_count}")
        INFER_DIR = f"inference_{infer_dir_count+1}"
        print(INFER_DIR)
        # Inference on images.
        detect_script = os.path.join(os.getcwd(), "detect.py")
        command = [
            "!python",
            detect_script,
            "--weights",
            f"runs/train/{RES_DIR}/weights/best.pt",
            "--source",
            data_path,
            "--name",
            INFER_DIR
        ]
        subprocess.run(command)
        return INFER_DIR

    @classmethod
    def visualize(cls, INFER_DIR):
        INFER_PATH = f"runs/detect/{INFER_DIR}"
        infer_images = glob.glob(f"{INFER_PATH}/*.jpg")
        print(infer_images)
        for pred_image in infer_images:
            image = cv2.imread(pred_image)
            plt.figure(figsize=(19, 16))
            plt.imshow(image[:, :, ::-1])
            plt.axis('off')
            plt.show()
