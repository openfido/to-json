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
	import openfido_util as of
	of.setup_io(inputs,outputs)
	format = []
	if "-d" in options or "--dict" in options:
		format.append("dict")
	elif "-l" in options or "--list" in options:
		format.append("list")
	if len(set(format)) > 1:
		raise Exception("only one output format can be specified")
	elif not format:
		format = "dict"
	else:
		format = format[0]
	result = []
	for file in inputs:
		if not file:
			raise Exception("missing input")
		data = of.read_input(file,options)
		result.append(data)
	if format == "list":
		result = pandas.DataFrame(pandas.concat(result)).values.tolist()
	elif format == "dict":
		result = pandas.DataFrame(pandas.concat(result)).to_dict()
	else:
		raise Exception(f"invalid output format specified")
	of.write_output(result,outputs[0],options)
	return {outputs[0]:result}
