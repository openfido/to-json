"""OpenFIDO to-json pipeline

This pipeline converts the contents of the input to JSON output

INPUTS

  List of input files to be converted. If input is omitted, input is read to /dev/stdin.

OUTPUTS

  List of JSON output files. If output omitted, output is written to /dev/stdout.

"""
import os, csv, pandas, json
def main(inputs,outputs,options):
	if not inputs:
		inputs = ["/dev/stdin"]
	if outputs:
		if len(outputs) > 1 :
			raise Exception("too many outputs")
	else:
		outputs = ["/dev/stdout"]
	result = []
	for file in inputs:
		if not file:
			raise Exception("missing input")
		data = pandas.read_csv(file,header=None)
		result.append(data)
	result = pandas.DataFrame(pandas.concat(result)).values.tolist()
	with open(outputs[0],"w") as fh:
		json.dump(result,fh,indent=4)
	return result
