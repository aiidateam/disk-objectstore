from .container import Container
import datetime
import tempfile

class WrappedRepository:
    def __init__(self, folder=None, verbose=True):
        """Initialise a new container."""
        if folder is None:
            folder = tempfile.mkdtemp()
            if verbose:
                print("Using random folder '{}' - remember to delete it (e.g. using 'self.clean_up_folder()".format(folder))
        self._container = Container(folder=folder)
        self._container.init_container()

    def clean_up_folder(self):
        """Clean up the folder of the container.
        
        It leaves only empty folders and an empty SQLAlchemy file."""
        self._container.init_container(clear=True)

    def put_objects(self, objlist):
        """Add a list of objects to the container.
        
        :param objlist: a list of bytestreams
        :return: a list of keys for the objects, in the same order as specified in objlist.
        """
        basedate = str(datetime.date.today())
        basetime = str(datetime.datetime.now().time()).replace(':','-')
        basename = 'file-'+basedate+'-'+basetime

        files_dict = {
            basename+str(idx).zfill(6)+'.dat': objcont
            for idx, objcont in enumerate(objlist)}

        self._container.add_files(files_dict)

        return list(files_dict.keys())

    def get_objects(self, keylist):
        """Get a list of objects from the container.
        
        :param objlist: a list of keys to retrieve.
        :return: a list of bytestreams with the content of the keys requested.
        """
        objlist = []
        for keyname in keylist:
            objlist.append( self._container.get_file_content(keyname) )

        return objlist

    def del_objects(self, keylist):
        """Delete an object from the container.
        
        Note: this often performs a fast delete, often 'soft', i.e. the data
        might remain on disk (especially if already packed).

        You will need to repack everything to clean up space.
        """
        raise NotImplementedError

    def get_size(self):
        """Get the total size in bytes of all files in the repository."""
        total_size_packed, total_size_loose = self._container.get_total_size()
        return total_size_loose + total_size_packed

    def pack(self):
        """Pack all loose objects."""
        self.pack_all_loose()

if __name__ == "__main__":

    wrapped_repo = WrappedRepository(verbose=True)

    contents = [b"34234", b"sdfssd"]

    filenames = wrapped_repo.put_objects(contents)
    size_before = wrapped_repo.get_size()
    print("Size before: {}".format(size_before))

    wrapped_repo.pack()
    size_after = wrapped_repo.get_size()
    print("Size after: {}".format(size_after))
    
    data = wrapped_repo.get_objects(filenames)
    assert data == contents

    print("All tests passed (write+read)")
