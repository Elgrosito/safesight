from matplotlib import pyplot as plt

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
