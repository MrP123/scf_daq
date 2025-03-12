# SCF DAQ
This project does data acquisition for collecting data from smart composite fabrics (SCF) that have embedded piezoelectric strain sensors based made from PVDF foil.

Currently it is only used for testing how well LDAQ handles data acquisition at high sampling rates of 1 MS/s.

## Installation
1. Clone the repository
2. Create a virtual environment & activate it
```
python -m venv .venv
.venv\Scripts\activate
```
3. Install the required packages using pip
```
pip install -r requirements.txt
```
4. Run the main Jupyter notebook
