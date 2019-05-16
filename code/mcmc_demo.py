import csv
import numpy
import scipy.special
import scipy.stats
import sys

def log_density(coordinates, components, log_weights):
	n_components = len(components)
	log_densities = numpy.zeros(n_components)

	for i in range(n_components):
		log_densities[i] = components[i].logpdf(coordinates) + log_weights[i]

	log_density = scipy.special.logsumexp(log_densities)

	return log_density

def proposal(coordinates, scale):
	n_coordinates = len(coordinates)
	i = numpy.random.randint(n_coordinates)

	delta = numpy.random.normal() * scale

	proposed_coordinates = numpy.copy(coordinates)
	proposed_coordinates[i] += delta

	return proposed_coordinates

def proposal2(coordinates, scale):
	n_coordinates = len(coordinates)
	n_to_change = numpy.random.randint(n_coordinates) + 1
	i_to_change = numpy.random.choice(n_coordinates, size = n_to_change, replace = False)

	delta = numpy.random.normal() * scale * 2.0

	proposed_coordinates = numpy.copy(coordinates)

	for i in i_to_change:
		proposed_coordinates[i] += delta

	return proposed_coordinates

if len(sys.argv) > 2:
	use_proposal2 = sys.argv[1] == "2"
	trace_filename = sys.argv[2]
else:
	use_proposal2 = False
	trace_filename = sys.argv[1]

trace_file = open(trace_filename, "w")
trace_writer = csv.writer(trace_file, dialect = csv.excel_tab)
trace_header = ["iteration", "log_density", "x", "y", "z"]
trace_writer.writerow(trace_header)

n_samples = 1000
sample_frequency = 100
n_iterations = n_samples * sample_frequency

proposal_scale = 3.0

major_component = scipy.stats.multivariate_normal(mean = [12.0] * 3, cov = ((9.0, 0.0, 0.0), (0.0, 9.0, 0.0), (0.0, 0.0, 9.0)))
minor_component = scipy.stats.multivariate_normal(mean = [25.0] * 3, cov = ((1.0 / 9.0, 0.0, 0.0), (0.0, 1.0 / 9.0, 0.0), (0.0, 0.0, 1.0 / 9.0)))

components = (major_component, minor_component)
log_weights = (numpy.log(0.5), numpy.log(0.5))

current_coordinates = 22.0 + numpy.random.random(3) * 6
current_log_density = log_density(current_coordinates, components, log_weights)

for iteration in range(n_iterations):
	if iteration % sample_frequency == 0:
		trace_row = [iteration, current_log_density] + list(current_coordinates)
		trace_writer.writerow(trace_row)

	if use_proposal2:
		proposed_coordinates = proposal2(current_coordinates, proposal_scale)
	else:
		proposed_coordinates = proposal(current_coordinates, proposal_scale)

	proposed_log_density = log_density(proposed_coordinates, components, log_weights)
	acceptance_probability = numpy.exp(proposed_log_density - current_log_density)

	if acceptance_probability > numpy.random.random():
		current_coordinates = proposed_coordinates
		current_log_density = proposed_log_density

trace_row = [n_iterations, current_log_density] + list(current_coordinates)
trace_writer.writerow(trace_row)

trace_file.close()
