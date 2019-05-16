# Assessing MCMC convergence

## Introduction

Consider the following MCMC traces showing the log probability density from two
independent chains, both sampling from the same probability distribution:

![alt text](example_traces.png "MCMC traces with high and low probability densities.")

Which chain has converged? It seems intuitive that the chain with the higher
log probability density has converged and is sampling from the stationary
distribution, whereas the chain with the lower posterior density has failed to
do so. After all, there is roughly 5.5 log units between the means of the two
chains, meaning that the probability density being sampled by the turquoise
chain is roughly 250 times greater than what is being sampled by the gold
chain!

However I will show that in fact neither chain has converged.

## Probability distributions

In this case, we are sampling from a three-dimensional probability
distribution which is a 50/50 mixture of two circular-symmetric multivariate
Gaussians. The mean and standard deviation of each coordinate for the first
(broad) Gaussian are 12 and 3 respectively, and for the second (narrow)
Gaussian are 25 and 1/3.

Because the Gaussians are placed some distance apart, this creates two modes
which share roughly equally the probability mass of the mixture. If the
probability distribution happens to be a posterior distribution, this means
that we are 50% certain that the truth lies within the broader mode, and 50%
certain that it lies within the narrower mode.

![alt text](random_samples.png "The bimodal mixture distribution.")

