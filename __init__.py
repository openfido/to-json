"""OpenFIDO to-json pipeline

This pipeline converts the contents of the input to JSON output

INPUTS

  List of input files to be converted. If input is omitted, input is read to /dev/stdin.

OUTPUTS

  List of JSON output files. If output omitted, output is written to /dev/stdout.

OPTIONS

  -d|--dict   Output data as a dictionary
  -l|--list   Output data as a list
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
	format = "dict"
	for option in options:
		if option in ["-d","--dict"]:
			format = "dict"
		elif option in ["-l","--list"]:
			format = "list"
		else:
			raise Exception("'{option}' is not a valid JSON format")
	result = []
	for file in inputs:
		if not file:
			raise Exception("missing input")
		data = pandas.read_csv(file,header=None)
		result.append(data)
	if format == "list":
		result = pandas.DataFrame(pandas.concat(result)).values.tolist()
	elif format == "dict":
		result = pandas.DataFrame(pandas.concat(result)).to_dict()
	else:
		raise Exception(f"format '{format}' is not valid")
	with open(outputs[0],"w") as fh:
		json.dump(result,fh,indent=4)
	return result
