# cellCounterForLaturbornetal
 Cell counter to work on images from aging repository
 
Download images and crop to homongous cell fields of approximately the same size (Though response values will be normalized)

Put those images in a folder- Set that directory in line 36 and 37

Set line 36 to locaiton of: DonorInformation filtered by availability of ISH.xls

Set cell Threshold at line 44

Run code Dependencies: Skimage, PIL, numpy, matplotlib, os Scipy, xlrd

outcome: An outfile with counts, diagnosis, PID and areas