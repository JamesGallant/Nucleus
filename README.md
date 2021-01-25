# Nucleus
Computer vision project using Facebook's detectron2 API in a PyQt5 interface. The idea is to create a GUI to interact with detectron2, this works on linux

# Install the dependencies

Install python > 3.6 and pytorch from their [website](https://pytorch.org/) choose the version that works for you. For gpu support you need cuda
```
# cuda
sudo apt install nvidia-cuda-toolkit
pip install qdarkstyle
pip install torch==1.7.1+cpu torchvision==0.8.2+cpu torchaudio==0.7.2 -f https://download.pytorch.org/whl/torch_stable.html
python -m pip install 'git+https://github.com/facebookresearch/detectron2.git'
sudo apt-get install python3-pyqt5 
```

# Running the GUI
once everything is called you can run it in like so:

```
git clone https://github.com/JamesGallant/Nucleus.git

cd Nucleus
python3 main.py

```

# Current state
We can do inference from existing models. Add the ability to train models as well as a choice of models.

