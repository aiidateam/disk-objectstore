from .container import Container
import tempfile

class WrappedRepository:
    def __init__(self, folder=None, verbose=True, clear=False):
        """Initialise a new container."""
        if folder is None:
            folder = tempfile.mkdtemp()
            if verbose:
                print("Using random folder '{}' - remember to delete it (e.g. using 'self.clean_up_folder()".format(folder))
        self._container = Container(folder=folder)
        if clear:
            self._container.init_container(clear=clear)
        if not self._container.is_initialised:
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
        keys = []

        for content in objlist:
            keys.append(self._container.add_object(content))

        return keys

    def get_objects(self, keylist):
        """Get a list of objects from the container.
        
        :param objlist: a list of keys to retrieve.
        :return: a list of bytestreams with the content of the keys requested.
        """
        content = self._container.get_object_contents(keylist)
        return [content[key] for key in keylist]

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
        self._container.pack_all_loose()
