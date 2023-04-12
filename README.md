# Glasses Detection via OpenCV

To use, run the program with `python main.py <file-to-process>` (processess a single file and shows pretty pictures)
Alternatively, use `python mass_process <directory-to-process> <output-path>` to process all .png/.jpg files in a directory (and its subdirectories) and save the outputs to a .csv file. 
The program was made to handle near-infrared ocular images, but may work with other formats too. For best results, use 4:3 ratio images, as the program scales them to 320x240 resolution.
