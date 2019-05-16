library(plot3D)

args = commandArgs(trailingOnly = TRUE)

trace = read.csv(paste0(args[1], ".tsv"), sep = "\t")

png(filename = paste0(args[1], ".png"), width = 1280, height = 960, pointsize = 24)

scatter3D(trace$x, trace$y, trace$z, colvar = trace$log_density, xlim = c(0, 30), ylim = c(0, 30), zlim = c(0, 30), clim = c(-25, 0), clab = "log density", ticktype = "detailed")

dev.off()
