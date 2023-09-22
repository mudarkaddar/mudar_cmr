# Input data for processing
import numpy as np
import requests

def mbart_summary(input_data, colab_api_url, p_num_beams, p_max_length_input, p_max_length_output, p_repetition_penalty, p_temperature):
   
    payload = {
        'input_data': input_data,
        'p_num_beams': p_num_beams,
        'p_max_length_input': p_max_length_input,
        'p_max_length_output': p_max_length_output,
        'p_repetition_penalty': p_repetition_penalty,
        'p_temperature': p_temperature
    }
    # Send the POST request with the JSON payload
    response = requests.post(colab_api_url, json=payload)
    # Extract the result from the response
    result = response.json().get('result')
    return result
def mbart_summary_list(input_data_list, colab_api_url, p_num_beams, p_max_length_input, p_max_length_output, p_repetition_penalty, p_temperature):
   
    mbart_summary_all = np.vectorize(mbart_summary)

    result_list = mbart_summary_all(input_data_list, colab_api_url, p_num_beams, p_max_length_input, p_max_length_output, p_repetition_penalty, p_temperature)
    return {'message': result_list}