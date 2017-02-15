import json
import numpy as np
import base64

class _NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        """If input object is an ndarray it will be converted into a dict 
        holding dtype, shape and the data, base64 encoded.
        """
        if isinstance(obj, np.ndarray):
            if obj.flags['C_CONTIGUOUS']:
                obj_data = obj.data
            else:
                cont_obj = np.ascontiguousarray(obj)
                assert(cont_obj.flags['C_CONTIGUOUS'])
                obj_data = cont_obj.data
            data_b64 = base64.b64encode(obj_data)
            return dict(__ndarray__=data_b64,
                        dtype=str(obj.dtype),
                        shape=obj.shape)
        # Let the base class default method raise the TypeError
        return json.JSONEncoder(self, obj)


def _json_numpy_obj_hook(dct):
    """Decodes a previously encoded numpy ndarray with proper shape and dtype.

    :param dct: (dict) json encoded ndarray
    :return: (ndarray) if input was an encoded ndarray
    """
    if isinstance(dct, dict) and '__ndarray__' in dct:
        data = base64.b64decode(dct['__ndarray__'])
        return np.frombuffer(data, dct['dtype']).reshape(dct['shape'])
    return dct
	
def save(data, filename):
	assert type(data) is dict
	# Save
	with open(filename, 'w') as outfile:
		for (key, val) in data.iteritems():
			# Convert np arrays to lists
			if (type(val) is np.ndarray):
				data["[np] " + key] = val.tolist()
				del data[key]
		json.dump(data, outfile, cls=_NumpyEncoder)
    
def load(filename):
	with open(filename, 'r') as infile:
		data = json.load(infile, object_hook=_json_numpy_obj_hook)
    # Convert things to ndarray
		for (key, val) in data.iteritems():
			# Check for [np] tags
			if (key.split(' ', 1)[0] == '[np]'):
				data[key.split(' ', 1)[1]] = np.ndarray(val)
				del data[key]
		return data
