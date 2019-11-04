import os

class RasterPolygonEnumT:
    def __init__(self):
        print("_init_ RasterPolygonEnumT")
        self.panPolyIdMap=[]
        self.panPolyValue = []
        self.nNextPolygonId = 0 # 多边形Id个数
        # nPolyAlloc = 0  # alloc个数，py里面不需要考虑
        self.nFinalPolyCount = 0 # 根节点计数值
	# 变量有多余的，debug用

    def MergePolygon(self,nSrcId,nDstIdInit):        
        nDstIdFinal = nDstIdInit
        while (self.panPolyIdMap[nDstIdFinal] != nDstIdFinal):
            nDstIdFinal = self.panPolyIdMap[nDstIdFinal]

        # Map the whole intermediate chain to it.
        nDstIdCur = nDstIdInit
        while (self.panPolyIdMap[nDstIdCur] != nDstIdCur):
            nNextDstId = self.panPolyIdMap[nDstIdCur]
            self.panPolyIdMap[nDstIdCur] = nDstIdFinal
            nDstIdCur = nNextDstId

        # And map the whole source chain to it too (can be done in one pass).
        while (self.panPolyIdMap[nSrcId] != nSrcId):
            nNextSrcId = self.panPolyIdMap[nSrcId]
            self.panPolyIdMap[nSrcId] = nDstIdFinal
            nSrcId = nNextSrcId

        self.panPolyIdMap[nSrcId] = nDstIdFinal

    def NewPolygon(self,nValue):
        nPolyId=self.nNextPolygonId
	
        self.panPolyIdMap.append(nPolyId)
        self.panPolyValue.append(nValue)
        self.nNextPolygonId=self.nNextPolygonId+1

        return nPolyId

    def ProcessLine(self,panLastLineVal,panThisLineVal,panLastLineId,panThisLineId,nXSize,iY):
        if (panLastLineVal[1] == -1):
            for i in range(1,nXSize+1):
                # 跟左边像素属性不一样，新建一个polygon
                # print("debug:","panThisLineVal[i]",panThisLineVal[i],"panThisLineVal[i-1]",panThisLineVal[i-1])
                if (panThisLineVal[i]!=panThisLineVal[i-1]):
                    panThisLineId[i] = self.NewPolygon(panThisLineVal[i])
                    # print("first line new poly")            
                    # print(" panThisLineId[i]", panThisLineId[i])
                else:
                    panThisLineId[i] = panThisLineId[i - 1]

            # print("first line debug:",panThisLineId)
            # os.system("pause")
            return

        # print("** not first line start  **")
        for i in range(1,nXSize+1):
            # print("x坐标:",i)
            # print("Last[i-1]",panLastLineVal[i-1],"Last[i]",panLastLineVal[i],"Last[i+1]",panLastLineVal[i+1])
            # print("This[i-1]",panThisLineVal[i-1],"This[i]",panThisLineVal[i])
            if (panThisLineVal[i] == -1):
                panThisLineId[i] = -1
            else :
                if ( i>1 and panThisLineVal[i]==panThisLineVal[i-1] ):
                    if iY==21 and i==27:
                        print("enter here 1")
                    panThisLineId[i] = panThisLineId[i-1];

                    if ( panLastLineVal[i]==panThisLineVal[i] and self.panPolyIdMap[panLastLineId[i]]!=self.panPolyIdMap[panThisLineId[i]] ):
                        self.MergePolygon(panLastLineId[i], panThisLineId[i])
                        # merge(src,dst)

                    if ( panLastLineVal[i-1]==panThisLineVal[i] and self.panPolyIdMap[panLastLineId[i-1]]!=self.panPolyIdMap[panThisLineId[i]] ):
                        self.MergePolygon(panLastLineId[i - 1], panThisLineId[i])

                    if ( i<nXSize and panLastLineVal[i+1]==panThisLineVal[i] and self.panPolyIdMap[panLastLineId[i+1]]!=self.panPolyIdMap[panThisLineId[i]] ):
                        self.MergePolygon(panLastLineId[i+1], panThisLineId[i])
                        # print("[非首列]左：true + 正上：true")
                else :
                    if ( panLastLineVal[i]==panThisLineVal[i] ):
                        if iY==21 and i==27:
                            print("enter here 2")
                        panThisLineId[i] = panLastLineId[i]
                    else :
                        if (i>1 and panLastLineVal[i-1]==panThisLineVal[i]):
                            if iY==21 and i==27:
                                print("enter here 3")
                            panThisLineId[i] = panLastLineId[i-1]

                            if (i<nXSize and panLastLineVal[i+1]==panThisLineVal[i] and self.panPolyIdMap[panLastLineId[i+1]]!=self.panPolyIdMap[panThisLineId[i]]):
                                self.MergePolygon(panLastLineId[i+1], panThisLineId[i]);
                        else :
                            if ( i<nXSize and panLastLineVal[i+1]==panThisLineVal[i]):
                                if iY==21 and i==27:
                                    print("enter here 4")
                                panThisLineId[i] = panLastLineId[i+1]
                            else:
                                if iY==21 and i==26:
                                    print("enter here 5")
                                    print("panThisLineVal[i]",panThisLineVal[i])
                                panThisLineId[i]=self.NewPolygon(panThisLineVal[i])
				
    def CompleteMerges(self):
        #传播标签
        for iPoly in range(0,self.nNextPolygonId):
	    # Figure out the final id.
            nId = self.panPolyIdMap[iPoly]
            while (nId != self.panPolyIdMap[nId]):
                nId = self.panPolyIdMap[nId]

	    # Then map the whole intermediate chain to it.
            nIdCur = self.panPolyIdMap[iPoly]
            self.panPolyIdMap[iPoly] = nId
            while (nIdCur != self.panPolyIdMap[nIdCur]):
                nNextId = self.panPolyIdMap[nIdCur]
                self.panPolyIdMap[nIdCur] = nId
                nIdCur = nNextId

            # 如果为根节点，continue
            if (self.panPolyIdMap[iPoly] == iPoly):
                self.nFinalPolyCount=self.nFinalPolyCount+1

        
    
 

