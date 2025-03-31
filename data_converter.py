from typing import Any, Dict


def measurement_dict_to_sep005(meas_dict: Dict[str, Dict[str, Any]]):
    #https://github.com/sdypy/sdypy/blob/main/docs/seps/sep-0005.rst

    signals = []

    for acq_name, data in meas_dict.items():
        if acq_name == "comment":
            continue

        signal = {
            "name": acq_name,    #TODO: Think about if the acquisition name is actually a good name for the resulting signal data
            "data": data["data"],
            "time": data["time"],
            "fs": data["sample_rate"],
            "channel_name": data["channel_names"],
            "unit_str": ""       #TODO: Check if it is somehow possible to retrieve the unit that was associated with the channel of the LDAQ NITask
        }

        #LDAQ always stores a time signal
        n_samples = signal["time"].shape[0]
        n_channels = 1

        #multiple channels specified
        if isinstance(signal["channel_name"], list):
            n_channels = len(signal["channel_name"])

        #if data has more than 1 channel it is a 2D np.array
        if(len(signal["data"].shape)) == 2:
            data_shape = signal["data"].shape

            #TODO: Investigate the following 
            #The official documentation (https://github.com/sdypy/sdypy/blob/main/docs/seps/sep-0005.rst) actually states (n_channels, n_samples) as correct order
            #This differs from the implementation in the assertin tool https://github.com/sdypy/sdypy-sep005-compliance
            #This implementation follows the assertion tool
            if data_shape == (n_samples, n_channels):
                #correct order
                pass
            elif data_shape == (n_channels, n_samples):
                signal["data"] = signal["data"].T
            else:
                raise AssertionError("data is in wrong shape, does not match time (n_samples) and channel_name (n_channels)")
        else:
            assert signal["data"].shape[0] == n_samples, "data does not have same size as time"

        signals.append(signal)
    
    #SEP005 allows either a dict or a list of dicts. Return the more convenient form
    if len(signals) == 1:
        return signals[0]
    else:
        return signals


if __name__ == "__main__":
    import LDAQ
    from sdypy_sep005.sep005 import assert_sep005

    loaded_data = LDAQ.utils.load_measurement("20250320_135546_impact_sample_1.pkl", directory="data")
    data = measurement_dict_to_sep005(loaded_data)
    assert_sep005(data)
    print(data)
