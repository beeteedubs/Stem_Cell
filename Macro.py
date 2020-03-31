
import csv                      # Jython only has standard Python libraries, no Pandas for dataframes means importing csv
from ij import IJ               # crazy, but can use .jar files, I think must be in same folder as script
import os
from ij.plugin import ChannelSplitter
import sys
"""
IJ.log("Beginning Macro")
test_counter = 0

tiff_path = 'D:/Stem_Cells/All_Tiff_Files'

for file in os.listdir(tiff_path):
    if test_counter > 1:
        break
    IJ.log(file)
    test_counter+=1

THIS WORKS, COMMENTED OUT FOR NOW CUZ SLOW
infile = "D:/A3 Exp/sub exp/GT A3_Stitch.tif"
curr_image = IJ.openImage(infile) # type: imagePlus
curr_image.show()
"""

prolif_counter, iffy_counter, senescent_counter = 1,1,1

length, height = 200, 200
batch_folder = "Batch_1"
radius = 4
lowerThreshold = 30.0
upperThreshold = 255.0
circularity = 0.70
size = 50.00

tiff_path = 'D:/Stem_Cells/All_Tiff_Files'

# returns: c3 type: ImagePlus
def preprocess(filePath, fileName, fileID):
    global radius
    global circularity
    global size
    global lowerThreshold
    global upperThreshold

    curr = IJ.openImage(filePath + '/' + fileName)
    c1, c2, c3 = ChannelSplitter.split(curr) # type:
    IJ.run(c1,"Gaussian Blur...","sigma=%i" %radius)
    IJ.setThreshold(c1, lowerThreshold, upperThreshold)
    #IJ.run("Set Measurements...", "mean center redirect=C2-GT_%s-Stitch.tif decimal=1" %fileID)
    #IJ.run("Set Measurements...", "mean center redirect=C2-GT_A4-Stitch.tif decimal=1")
    IJ.run("Set Measurements...", "mean center redirect =C2-GT_%s-Stitch.tif decimal - 1" %fileID)
    IJ.run(c1, "Analyze Particles...", "size=%i-Infinity circularity=%i-1.00 display exclude include" %(size, circularity))
    return c3

def csvPreprocess(fileID):
    global batch_folder

    IJ.saveAs("Results", "D:/Stem_Cells/Batches/%s/CSV_Results/%s.csv" %(batch_folder, fileID))
    csv_file = open('D:/Stem_Cells/Batches/%s/CSV_Results/%s.csv' %(batch_folder, fileID))
    csv_reader = csv.reader(csv_file)
    next(csv_reader)
    return csv_reader

def cropAndSave(row, channel):
    # for checking bounds and making Regions of Interest (ROI, or aka rectangles)
    # 4.818 comes from converting micron to pixels
    global prolif_counter
    global iffy_counter
    global senescent_counter
    global length
    global height
    global batch_folder

    x_bound = channel.width
    y_bound = channel.height
    topLeft_x = int(float(row[2])*4.818 - (length/2))
    topLeft_y = int(float(row[3])*4.818 - (height/2))
    # checking for out of bounds
    if topLeft_x < 152 or topLeft_y < 152 or topLeft_x + length> x_bound - 152 or topLeft_y + height > y_bound - 152:
        IJ.log("outta bounds")
        return
    else:
        channel.setRoi(topLeft_x,topLeft_y, length, height)
        temp_image = channel.crop() # note: does not render, so saves memory
        #temp_image.show()
        IJ.log("Mean: "+row[1])
        if float(row[1]) < 10:
            IJ.save(temp_image,"D:/Stem_Cells/Batches/%s/Senescent/cell%i.tiff" %(batch_folder, senescent_counter))
            senescent_counter += 1 
            IJ.log("senescent saved")
        elif float(row[1]) > 30:
            IJ.save(temp_image,"D:/Stem_Cells/Batches/%s/Prolif/cell%i.tiff" %(batch_folder, prolif_counter))
            #IJ.save(temp_image,"D:/Stem_Cells/A3_Exp/cell%i.tif" %prolif_counter)
            #IJ.save(temp_image,"D:/Stem_Cells/A3_Exp/sub_exp/cells/test/Proliferative/cell%i.tif" %prolif_counter)
            prolif_counter += 1
            IJ.log("prolif saved")
        else:
            IJ.save(temp_image,"D:/Stem_Cells/Batches/%s/Iffy/cell%i.tif" %(batch_folder, iffy_counter))
            iffy_counter += 1
            IJ.log("iffy saved")
        #temp_image.close()  



#IJ.log("num channels of curr_image: " + str(curr_image.nChannels))
#curr_image.setActiveChannels("011")
#IJ.log("type of curr_image:" + str(type(curr_image)))

#csv_file = open('D:/Stem_Cells/A3_Exp/sub_exp/A5.csv')
#csv_reader = csv.reader(csv_file)



# hardcoded is fine for now 

#next(csv_reader)
#next(csv_reader)

def main():

    for file in os.listdir(tiff_path): # goes through each tiff file 
        fileID = file[3:5] # ex: A3
        channel = preprocess(tiff_path, file, fileID)
        data = csvPreprocess(fileID)

        #for row in data:
        #    cropAndSave(row, channel)
        sys.exit(0)
main()
