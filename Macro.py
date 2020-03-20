
import csv                      # Jython only has standard Python libraries, no Pandas for dataframes means importing csv
from ij import IJ               # crazy, but can use .jar files, I think must be in same folder as script
import os
from java.awt import Color, Dimension
from ij.process import LUT
from ij.process import ImageProcessor
from ij.plugin import ChannelSplitter

IJ.log("Beginning Macro")

# ------------------Variables------------------

# counters for labeling images/testing purposes
test_counter, prolif_counter, iffy_counter, senescent_counter = 0, 1, 1, 1
# pixel dimesions:
length, height = 200, 200
# batch folder
batch_folder = "Batch_1"
# preprocessing 
circularity = 0.70
size = 50.00
radius = 4

tiff_path = 'D:/Stem_Cells/All_Tiff_Files'
#----------------------------------------------

for file in os.listdir(tiff_path):

    # names .csv and specifies which file for instructions like "Set Measurements"
    fileName = file[3:5]
    IJ.log("File: " + fileName)            
    if test_counter > 0:
        break

    # opens and renders image
    curr = IJ.openImage(tiff_path + '/' + file) # type: CompositeImage
    x_bound = curr.width
    y_bound = curr.height
    IJ.log("opened")
    
    # ensures Gray LUT
    lut = LUT.createLutFromColor(Color.white) 
    lut.max = 255 
    curr.setChannelLut(lut,3)

    # Preprocessing
    c1, c2, c3 = ChannelSplitter.split(curr)
    c3.show()
    IJ.run(c1,"Gaussian Blur...","sigma=%i" %radius)
    IJ.setThreshold(c1, 30.0, 255.0)
    IJ.run("Set Measurements...", "mean center redirect =C2-GT_%s_Stitch.tif decimal - 1" %fileName)
    IJ.run(c1, "Analyze Particles...", "size=%i-Infinity circularity=%i-1.00 display exclude include" %(size, circularity))

    # CSV part
    IJ.saveAs("Results", "D:/Stem_Cells/Batches/%s/CSV_Results/%s.csv" %(batch_folder, fileName))
    csv_file = open('D:/Stem_Cells/Batches/%s/CSV_Results/%s.csv' %(batch_folder,fileName))
    csv_reader = csv.reader(csv_file)
    next(csv_reader)

    IJ.log("\n Reading .csv \n")
    for row in csv_reader:
        
        # for checking bounds and making Regions of Interest (ROI, or aka rectangles)
        # 4.818 comes from converting micron to pixels
        topLeft_x = float(row[2])*4.818 - (length/2)
        topLeft_y = float(row[3])*4.818 - (height/2)

        # checking for out of bounds
        if topLeft_x < 152.0 or topLeft_y < 152.0 or topLeft_x + length> x_bound-152 or topLeft_y + height > y_bound -152: 
            IJ.log("outta bounds")
            continue
        else:
            IJ.selectWindow("C3-GT_%s-Stitch.tif" %fileName)
            IJ.makeRectangle(topLeft_x,topLeft_y, length, height)
            temp_image = curr.crop() # note: does not render, so saves memory
            #temp_image.show()
            IJ.log("Mean: "+row[1])
            if float(row[1]) < 10:
                IJ.save(temp_image,"D:/Stem_Cells/Batches/%s/Senescent/cell%i.tiff" %(batch_folder, senescent_counter))
                senescent_counter += 1 
                IJ.log("senescent saved")
            elif float(row[1]) > 30:
                IJ.save(temp_image,"D:/Stem_Cells/Batches/%s/Prolif/cell%i.tif" %(batch_folder,prolif_counter))
                prolif_counter += 1
                IJ.log("prolif saved")
            else:
                IJ.save(temp_image,"D:/Stem_Cells/Batches/%s/Iffy/cell%i.tif" %(batch_folder, iffy_counter))
                iffy_counter += 1
                IJ.log("iffy saved")
            #temp_image.close()       
    c3.close()
    test_counter += 1
IJ.log("done")
