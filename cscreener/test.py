import h5py

fs = h5py.File("cscreener\ms_73.mat")

# fs["ms"].visititems(lambda n, o: print(n, o))
print(list(fs["ms"].keys()))
