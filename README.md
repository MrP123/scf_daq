# SCF DAQ
This project does data acquisition for collecting data from smart composite fabrics (SCF) that have embedded piezoelectric strain sensors fabricated from PVDF foil and Cu/Ni electrode tapes.

Currently it is only used for testing how well LDAQ handles data acquisition at high sampling rates of 1 MS/s. The tests are carried out on a SCF structure with four embedded sensors, meaning four channels are sampled simultaneously.

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
5. Run the main Jupyter notebook
