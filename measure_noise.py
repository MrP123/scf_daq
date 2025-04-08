import LDAQ
import numpy as np
import numpy.typing as npt
import matplotlib.pyplot as plt

def configure_task(num_channels: int = 6, chassis_name: str = "cDAQ2", module_slots: list[str] = ["Mod3", "Mod4"]):
    input_task_name = "ni_input_task"
    acquisition_name = input_task_name + "_acq"
    fs = 1_000_000

    ni_task = LDAQ.national_instruments.NITask(input_task_name, sample_rate=fs)

    device_names = [chassis_name + mod for mod in module_slots]
    device_ids = [ni_task.device_list.index(device_name) for device_name in device_names]

    num_channels_available = 0
    for id in device_ids:
        num_channels_available += len(ni_task.system.devices[id].ai_physical_chans)
    num_channels_per_device = num_channels_available / len(device_ids)

    # check if there are enough devices for the amount of channels
    assert num_channels <= num_channels_available, f"Not enough channels available on the selected devices. Desired: {num_channels}, Available: {num_channels_available}"

    for i in range(0, num_channels):
        current_device_id = device_ids[int(np.floor(i / num_channels_per_device))]
        channel_ind = int(i % num_channels_per_device)

        ni_task.add_channel(channel_name=f"ch{i+1}", device_ind=current_device_id, channel_ind=channel_ind, scale=1.0, units="V", min_val=-10.0, max_val=10.0)

    return ni_task, acquisition_name

def evaluate_noise(data, num_channels: int = 6):
    raw_data = data["data"]

    def rms(data):
        return np.sqrt(np.mean(data**2))

    rms_values = np.empty((num_channels,))
    mean_values = np.empty((num_channels,))
    max_values = np.empty((num_channels,))
    
    for i in range(0, num_channels):
        current_data = raw_data[:, data["channel_names"].index(f"ch{i+1}")]
        rms_values[i] = rms(current_data)
        mean_values[i] = np.mean(current_data)
        max_values[i] = np.max(np.abs(current_data))
    
        print(f"RMS of channel ch{i+1}: {rms_values[i]:.5f} V = {rms_values[i]*1e3:.2f} mV / mean: {mean_values[i]*1e3:.2f}")
    
    print(f"Mean RMS value is:  {np.mean(rms_values):.5f} V = {np.mean(rms_values)*1e3:.2f} mV")
    print(f"Max value for all data is: {np.max(max_values):.5f} V = {np.max(max_values)*1e3:.2f} mV")
    
    max_idx = np.argmax(rms_values)
    print(f"Estimated max noise amplitude is: {(3.3*rms_values[max_idx] + mean_values[max_idx])*1e3:.2f} mV") #Amplitude is smaller than 3.3 sigma for 99.9% of all samples would require mean to be 0


if __name__ == "__main__":
    num_channels = 6

    print(f"Configuring task...")
    ni_task, acquisition_name = configure_task(num_channels=num_channels)

    # Run acquisition
    print(f"Running acquisition...")
    acq_ni = LDAQ.national_instruments.NIAcquisition(task_name=ni_task, acquisition_name=acquisition_name)
    ldaq = LDAQ.Core(acquisitions=acq_ni)
    ldaq.run(5.0, autostart=True, verbose=0)

    # Get data & evaluate
    measurement = ldaq.get_measurement_dict()
    data = measurement[acquisition_name]

    print(f"Evaluating noise data...")
    evaluate_noise(data, num_channels=num_channels)
