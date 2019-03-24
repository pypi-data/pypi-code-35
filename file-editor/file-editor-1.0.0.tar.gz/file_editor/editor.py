from PIL import Image
import sys
import os
import fnmatch
from pdf2image import convert_from_path

def image(inputfile,outputfileformat):
	"""Convertor input file to different file formats
	   firstArgument = input file path
	   secondArgument = ouput file format """
	if inputfile.endswith(".pdf"):
		pages = convert_from_path(inputfile,200)
		for page in pages:
			output = createSeqFile("fileEditor",outputfileformat)
			page.save(output)
	else:
		im = Image.open(inputfile).convert("RGB")
		output = createSeqFile("fileEditor",outputfileformat)
		im.save(output)


def createSeqFile(basename, ext, dir=None, digits=3):
	if dir is None:
		dir = os.getcwd()

	m = 0
	for f in seqFiles(dir, recurse=False, abs_paths=False, return_folders=False, pattern='*', path=None):
		r, e = os.path.splitext(f)
		if r.startswith(basename) and ext == e:
			try:
				i = int(r[len(basename):])
			except ValueError:
				continue
			else:
				m = max(m, i)
	return os.path.join(dir, "%s%0*d%s" % (basename, digits, m+1, ext))
   	
def seqFiles(root, recurse=True, abs_paths=False, return_folders=False, pattern='*', path=None):
    if path is None:
        path = root

    try:
        names = os.listdir(root)
    except os.error:
        return

    pattern = pattern or '*'
    pat_list = pattern.split(';')

    for name in names:
        fullname = os.path.normpath(os.path.join(root, name))

        for pat in pat_list:
            if fnmatch.fnmatch(name, pat):
                if return_folders or not os.path.isdir(fullname):
                    if abs_paths:
                        yield fullname
                    else:
                        try:
                            yield os.path.basename(fullname)
                        except ValueError:
                            yield fullname


        if recurse and os.path.isdir(fullname): 
            for f in seqFiles(fullname, recurse, abs_paths, return_folders, pattern, path):
                yield f
    	
		
