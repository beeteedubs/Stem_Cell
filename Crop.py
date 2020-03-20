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
"""
    

"""
THIS WORKS, COMMENTED OUT FOR NOW CUZ SLOW
infile = "D:/A3 Exp/sub exp/GT A3_Stitch.tif"
curr_image = IJ.openImage(infile) # type: imagePlus
curr_image.show()
"""
prolif_counter, iffy_counter, senescent_counter = 1,1,1
curr = IJ.openImage("D:/Stem_Cells/All_Tiff_Files/GT_A5-Stitch.tif")
IJ.log(str(type(curr)))
c1, c2, c3 = ChannelSplitter.split(curr)
length, height = 200, 200
batch_folder = "Batch_1"
#.show()
#IJ.log("num channels of curr_image: " + str(curr_image.nChannels))
#curr_image.setActiveChannels("011")
#IJ.log("type of curr_image:" + str(type(curr_image)))

# ///How open only if not alreayd open///

IJ.log("opened\n")

csv_file = open('D:/Stem_Cells/A3_Exp/sub_exp/A5.csv')
csv_reader = csv.reader(csv_file)



# hardcoded is fine for now 

line_count = 0

next(csv_reader)
next(csv_reader)

IJ.log("\n Reading .csv \n")
def cropAndSave(name, row):
    # for checking bounds and making Regions of Interest (ROI, or aka rectangles)
    # 4.818 comes from converting micron to pixels
    global prolif_counter
    global iffy_counter
    global senescent_counter
    global curr
    global length
    global height
    global batch_folder
    # checking for out of bounds
    if float(row[4]) < 152.0 or float(row[5]) < 152.0 or float(row[4]) + float(row[6])> 27000 or float(row[5]) + float(row[7]) > 27000:
        IJ.log("outta bounds")
        return
    else:
        topLeft_x = int(float(row[2])*4.818 - (length/2))
        topLeft_y = int(float(row[3])*4.818 - (height/2))
        c3.setRoi(topLeft_x,topLeft_y, length, height)
        temp_image = c3.crop() # note: does not render, so saves memory
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
        
for row in csv_reader:
    
    cropAndSave("A5", row)

     


