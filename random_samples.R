library(plot3D)
library(mvtnorm)

major_cov_matrix = matrix(c(
  9.0, 0.0, 0.0,
  0.0, 9.0, 0.0,
  0.0, 0.0, 9.0), nrow = 3)

minor_cov_matrix = matrix(c(
  1.0 / 9.0, 0.0, 0.0,
  0.0, 1.0 / 9.0, 0.0,
  0.0, 0.0, 1.0 / 9.0), nrow = 3)

major_means = c(12.0, 12.0, 12.0)
minor_means = c(25.0, 25.0, 25.0)

major_samples = rmvnorm(500, mean = major_means, sigma = major_cov_matrix)
minor_samples = rmvnorm(500, mean = minor_means, sigma = minor_cov_matrix)

major_samples_df = data.frame(major_samples)
minor_samples_df = data.frame(minor_samples)

colnames(major_samples_df) = c("x", "y", "z")
colnames(minor_samples_df) = c("x", "y", "z")

major_samples_df$component = "major"
minor_samples_df$component = "minor"

mixture_samples_df = rbind(major_samples_df, minor_samples_df)

sample_densities = dmvnorm(rbind(major_samples, minor_samples), mean = major_means, sigma = major_cov_matrix) * 0.5 +
          dmvnorm(rbind(major_samples, minor_samples), mean = minor_means, sigma = minor_cov_matrix) * 0.5

mixture_samples_df$log_density = log(sample_densities)

png(filename = "random_samples.png", width = 1280, height = 960, pointsize = 24)

scatter3D(mixture_samples_df$x, mixture_samples_df$y, mixture_samples_df$z, colvar = mixture_samples_df$log_density, xlim = c(0, 30), ylim = c(0, 30), zlim = c(0, 30), clab = "log density", ticktype = "detailed")

dev.off()
