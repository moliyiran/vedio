from multiprocessing import Pool
class a:
    def c(self):
        i = 5
        while i>0:
            print("i"+str(i))
            i -=1;
    def d(self):
        i = 5
        while i>0:
            print("j"+str(i))
            i -=1;
if __name__=='__main__':
    obj = a()
    p = Pool(2)
    p.apply_async(obj.c, args=())
    p.apply_async(obj.d, args=())
    p.close()
    p.join() 
