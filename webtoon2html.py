#!/usr/bin/env python3
'''
The goal of this script is to make an html file of the manga pages to be read
'''
import pathlib
import cv2
def main():
    '''
    If in the structure of Manga_Name/Chapter_Name;
    create html file to read the pages here
    '''
    p = pathlib.Path('.')
    path          = str(pathlib.Path.cwd())
    path_fields   = path.split('/')
    chaptername   = path_fields[len(path_fields)-1]
    manganame     = path_fields[len(path_fields)-2]
    fname = manganame + "_" + chaptername + ".html"
    
    # replaces spaces with underscores
    fname = fname.replace(' ','_')
    
    # replace question marks with nothing
    fname = fname.replace('?','')

    # replace pound signs with nothing
    fname = fname.replace('#','')

    # replace colon with underscore
    fname = fname.replace(':','_')
    
    # get list of all jpgs here
    jpgs_here = []
    for file in [str(x) for x in p.iterdir() if x.is_file()]:
        if file.lower().endswith('jpg') or file.lower().endswith('jpeg'):
            jpgs_here.append(file)
            
    # convert all of these jpgs into pngs
    for jpg in jpgs_here:
        image = cv2.imread(jpg)
        # delete the original file
        pathlib.Path(jpg).unlink()
        # create new png
        cv2.imwrite(pathlib.PurePath(jpg).stem + ".png", image)
        
    # get list of all pngs and PNGs here
    pngs_here = []
    for file in [str(x) for x in p.iterdir() if x.is_file()]:
        if file.lower().endswith('png') or file.lower().endswith('PNG'):
            pngs_here.append(file)
    pngs_here = sorted(pngs_here)
            
    # write out html file
    with open(fname,'w') as fname:
        fname.write("<html>\n")
        fname.write("<body bgcolor=\"#000000\">\n")
        fname.write("<div id=\"container\">\n")
        fname.write("    <div id=\"floated-imgs\">\n")
        for png in pngs_here:
            s = "        <center><img src=\""
            s = s + png
            s = s + "\"></center>" + '\n'
            fname.write(s)
        fname.write("    </div>\n")
        fname.write("</div>\n")
        fname.write("</body>\n")
        fname.write("<style>\n")
        fname.write("   #img{\n")
        fname.write("      float: center;\n")
        fname.write("   }\n")
        fname.write("   #img img{\n")
        fname.write("      display: block;\n")
        fname.write("   }\n")
        fname.write("</style>\n")
        fname.write("</html>\n")

if __name__ == "__main__":
    main()
