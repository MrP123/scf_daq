# Data Acquisition in Smart Composite Fabrics (SCFs) with PVDF Strain Sensors
This project is used to handle data acquisition from smart composite fabrics (SCF) that have embedded piezoelectric strain sensors fabricated from PVDF foil and Cu/Ni electrode tapes. The main test being carried out are drop weight impact tests lossely following [ASTM D7136](https://store.astm.org/d7136_d7136m-20.html).

Development and tests were carried out in the System Design with Advanced Composites Lab at Chung-Ang-University, Seoul.
This repository is supposed for data perparation for the neural network based evaluation methods developed in https://github.com/MrP123/scf_nn

The current test specimen is a 3D printed flat plate of size 300 mm x 120 mm with continuous carbon fibers in a [0/90] direction. The specimen contains 6 strain sensors in a 3x2 array.

## Installation
1. Clone the repository
2. Create a virtual environment & activate it
```sh
python -m venv .venv
.venv\Scripts\activate
```
3. Install the required packages using pip
```sh
pip install -r requirements.txt
```
4. If the NI-DAQmx drivers are not yet installed (or need updates) run
```sh
python -m nidaqmx installdriver
```
5. Run the `main` Jupyter notebook

## Usage
This repo contains a multitude of different files that are mainly used independently in the process of data acquisition and data preparation for the project.

- `main.ipynb`: Main Jupyter notebook used for collecting data. Sets up the DAQ and parts can be rerun for consecutive acquisitions.
- `extract_peak_times.ipynb`: Takes collected raw data from `main.ipynb` and extracts peaks for each channel for further processing using ANNs for impact localization.
- `planning_calcs.ipynb`: Used for calculating impact heights from desired energy.
- `measure_noise.py`: Used in the evaluation of the expected noise floor of each measurement. Also helpful when selecting trigger levels.
- `data_converter.py`: Helper module containing functions to transform the collected data into a uniform format.
- `plotting_utils.py`: Helper module with wrapper for the raw data that features helpful plotting functions


## Literature references
- [1] J. Yu, J. Liu, Z. Peng, L. Gan, and S. Wan, “Localization of impact on CFRP structure based on fiber Bragg gratings and CNN-LSTM-Attention,” Optical Fiber Technology, vol. 87, p. 103943, Oct. 2024, doi: 10.1016/j.yofte.2024.103943.
- [2] K.-C. Jung and S.-H. Chang, “Advanced deep learning model-based impact characterization method for composite laminates,” Composites Science and Technology, vol. 207, p. 108713, May 2021, doi: 10.1016/j.compscitech.2021.108713.
- [3] K.-C. Jung, M.-G. Han, and S.-H. Chang, “Impact characterisation of draped composite structures made of plain-weave carbon/epoxy prepregs utilising smart grid fabric consisting of ferroelectric ribbon sensors,” Composite Structures, vol. 238, p. 111940, Apr. 2020, doi: 10.1016/j.compstruct.2020.111940.
