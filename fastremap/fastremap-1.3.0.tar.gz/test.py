import fastremap
import numpy as np 
import time

x = np.random.randint(0, 2**16, (512,512,512), dtype=np.uint64)
print('created')
fastremap.renumber(x, in_place=True)

time.sleep(2)


# print(x.dtype)


# x = fastremap.asfortranarray(x)
# print(x)
# print(x.flags)
# print(x.strides)

# print(x.dtype)



# @profile
# def run():
#   x = np.ones( (512,512,512), dtype=np.uint32, order='C')
#   x += 1
#   print(x.strides, x.flags)
#   y = np.asfortranarray(x)
#   print(x.strides, x.flags)

#   print("done.")

# run()