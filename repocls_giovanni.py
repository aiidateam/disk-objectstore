import files_db
import files_db.add_file
import datetime

class repocls_giovanni:
    
    def __init__(self):
        from files_db.models import get_session
        from files_db.common import DB_FILE

        self._session = get_session(DB_FILE)

    def put_objects(self, objlist):
        basedate = str(datetime.date.today())
        basetime = str(datetime.datetime.now().time()).replace(':','-')
        basename = 'file-'+basedate+'-'+basetime

        files_dict = {basename+str(idx).zfill(6)+'.dat': objcont for idx, objcont in enumerate(objlist)}

        files_db.add_file.add_files(self._session, files_dict)

        return list(files_dict.keys())

    def get_objects(self, keylist):
        objlist = []
        for keyname in keylist:
            objlist.append( files_db.add_file.get_file_content(self._session, keyname) )

        return objlist

    def del_objects(self, keylist):
        # This is very easy to implement, just drop from the DB, but we
        # need to think if we want to do it at the lowest level, it's
        # annoying for concurrency reasons
        raise NotImplementedError

    def get_size(self):
        total_size_packed, total_size_loose = files_db.add_file.get_total_size(self._session)
        return total_size_loose + total_size_packed

    def pack(self):
        files_db.add_file.pack_all_loose(self._session)

if __name__ == "__main__":

    impl = repocls_giovanni()

    contents = [b"34234", b"sdfssd"]

    filenames = impl.put_objects(contents)
    size_before = impl.get_size()
    print("Size before: {}".format(size_before))

    impl.pack()
    size_after = impl.get_size()
    print("Size after: {}".format(size_after))
    
    data = impl.get_objects(filenames)
    assert data == contents

    print("All tests passed (write+read)")
