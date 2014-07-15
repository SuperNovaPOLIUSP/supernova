import os           # package for basic OS operations
import shutil       # package for high level file operations

class FileError(Exception):
    """
     Exception reporting an error in the execution of a File operation.

    :version:
    :author:
    """
    pass

class File (object):
  
    """
     Class that abstracts a file in the file system, providing some tools to keep and
     manipulate a file.
  
    :version:
    :author:
    """
  
    """ ATTRIBUTES
  
     The absolute path to the directory which contains the file in the file system.
  
    directoryPath  (public)
  
     The file name (must not have spaces).
  
    fileName  (public)
  
     Object that represents the actual file that the File object is modeling. 
     Should be used only if necessary.
  
    realFile  (public)
  
    """
  
    def __init__(self, directoryPath, fileName):
        """
         Constructor method.
  
        @param string directoryPath : The absolute path to the directory which contains the file in the file system.
        @param string fileName : The file name (must not have spaces).
        @return  :
        @author
        """
        if not isinstance(directoryPath, str):
            raise FileError("Invalid directoryPath parameter: must be a string.")
        else:        
            if not os.path.exists(directoryPath):
                # tries to create directory if it does not exist
                try:
                    os.mkdir(directoryPath)
                except:
                    raise FileError("Invalid directoryPath parameter: access denied.")
            else:
                # attempts to access the directory
                try:
                    os.chdir(directoryPath)
                except:
                    raise FileError("Invalid directoryPath parameter: access denied.")
  
        if not isinstance(fileName, str):
            raise FileError("Invalid fileName parameter: must be a string.")
        elif fileName == "":
            raise FileError("Invalid fileName parameter: must not be an empty string.")
  
  
        self.directoryPath = directoryPath
        self.fileName = fileName
        self.realFile = None
  
    def deleteFile(self, deleteDirectory = False):
        """
         Deletes the existing file from the file system.
  
        @param bool deleteDirectory : Boolean that specifies if the directory that contains the file should also be deleted.
        @return  :
        @author
        """
        try:
            os.remove(self.getAbsolutePath())
        except:
            raise FileError("Impossible to delete file: file does not exist.")
  
        if deleteDirectory:
            shutil.rmtree(self.directoryPath)
  
    def moveToDirectory(self, directoryPath):
        """
         Moves the file to the specified directory. If the directory does not exist, it
         is created in order to move the file.
  
        @param string directoryPath : Path to the directory, in the file system, to where the file should be moved.
        @return  :
        @author
        """
        if not isinstance(directoryPath, str):
            raise FileError("Invalid directoryPath parameter: must be a string.")
        else:        
            if not os.path.exists(directoryPath):
                # tries to create directory if it does not exist
                try:
                    os.mkdir(directoryPath)
                except:
                    raise FileError("Invalid directoryPath parameter: access denied.")
  
        if os.path.exists(os.path.join(directoryPath, self.fileName)):
            raise FileError("Invalid directoryPath parameter: there is already a file with this name in the directory of destination.")
  
        #os.rename(self.getAbsolutePath(), os.path.join(directoryPath, self.fileName))
        try:
            os.rename(self.getAbsolutePath(), os.path.join(directoryPath, self.fileName))
        except:
            raise FileError("Invalid directoryPath parameter: error ocurred while moving file.")
  
        self.directoryPath = directoryPath
  
    def getAbsolutePath(self):
        """
         Returns the name of the file's absolute path.
  
        @return string :
        @author
        """
        return os.path.join(self.directoryPath, self.fileName)
  
    def workWithFile(self):
        """
         Changes the current directory to the file's directory in order to allow working
         with it.
  
        @return  :
        @author
        """
        os.chdir(self.directoryPath)

