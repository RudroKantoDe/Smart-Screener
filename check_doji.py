def doji (dj):
    val=1/100*dj[3]
    val1=0.5/100*dj[3]
    if dj[0]<dj[3]:
        if dj[3]-dj[0]<=val:
            if abs((dj[2]-dj[3])-(dj[0]-dj[1]))<=val1:
                return 1
                    
    if dj[0]>dj[3]:
        if dj[0]-dj[3]<=val:
            if abs((dj[2]-dj[0])-(dj[3]-dj[1]))<=val1:
                return 2
    return 0
                    
    
