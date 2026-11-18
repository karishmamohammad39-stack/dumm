import os
import tempfile

def test_rename_open():
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "test.txt")
        with open(path, "w") as f:
            f.write("hello")
        
        # open for reading
        f = open(path, "r")
        
        path_tmp = os.path.join(tmp, "test.tmp")
        with open(path_tmp, "w") as f2:
            f2.write("world")
            
        try:
            os.replace(path_tmp, path)
            print("os.replace succeeded!")
        except Exception as e:
            print(f"os.replace failed: {type(e).__name__} - {e}")
            
        try:
            path_old = path + ".old"
            os.rename(path, path_old)
            print("os.rename out of the way succeeded!")
            os.replace(path_tmp, path)
            print("os.replace after rename succeeded!")
        except Exception as e:
            print(f"rename/replace failed: {type(e).__name__} - {e}")
            
        f.close()

if __name__ == "__main__":
    test_rename_open()
