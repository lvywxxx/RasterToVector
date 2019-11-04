import os

class RasterPolygonEnumT:
    def __init__(self):
        print("_init_ RasterPolygonEnumT")
        self.panPolyIdMap=[]
        self.panPolyValue = []
        self.nNextPolygonId = 0 # 多边形Id个数
        # nPolyAlloc = 0  # alloc个数，py里面不需要考虑
        self.nFinalPolyCount = 0 # 根节点计数值

    def MergePolygon(self,nSrcId,nDstIdInit):        
        # 独立生长的两个polygon，某一点处发现邻接，merge
        # Figure out the final dest id.
        # 从DstInit开始向后传播，找到根节点
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
        # nPolyId是第几个，nPolyVal是属性值
        nPolyId=self.nNextPolygonId
        #if (self.nNextPolygonId >= self.nPolyAlloc):
            #self.nPolyAlloc = nPolyAlloc * 2 + 20;
            #panPolyIdMap = static_cast<int*>(realloc(panPolyIdMap, nPolyAlloc * sizeof(int)))
            #panPolyValue = static_cast<DataType*>(realloc(panPolyValue, nPolyAlloc * sizeof(DataType)))
        # self.nPolyAlloc=self.nPolyAlloc+1
        self.panPolyIdMap.append(nPolyId)
        self.panPolyValue.append(nValue)
        self.nNextPolygonId=self.nNextPolygonId+1
        #self.panPolyIdMap[nPolyId] = nPolyId
        #self.panPolyValue[nPolyId] = nValue
        return nPolyId

#*********************************************************************************************************************************

    def ProcessLine(self,panLastLineVal,panThisLineVal,panLastLineId,panThisLineId,nXSize,iY):
        # -------------------------------------------------------------------- */
	    #   Special case for the first line.                                */
	    # -------------------------------------------------------------------- */
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

	    #/* -------------------------------------------------------------------- */
	    #/*      Process each pixel comparing to the previous pixel, and to      */
	    #/*      the last line.                                                  */
	    #/* -------------------------------------------------------------------- */
        # 约束强一点总没错
        # print("** not first line start  **")
        for i in range(1,nXSize+1):
            # print("x坐标:",i)
            # print("Last[i-1]",panLastLineVal[i-1],"Last[i]",panLastLineVal[i],"Last[i+1]",panLastLineVal[i+1])
            # print("This[i-1]",panThisLineVal[i-1],"This[i]",panThisLineVal[i])
            if (panThisLineVal[i] == -1):
                panThisLineId[i] = -1
            else :
                if ( i>1 and panThisLineVal[i]==panThisLineVal[i-1] ):
			        # 非首列，并且等于左边像素的情况，本分支8领域全部考虑了
                    # print("[非首列] 左：true")

                    if iY==21 and i==27:
                        print("enter here 1")
                    panThisLineId[i] = panThisLineId[i-1];

			        # 在map中传播_val：左上、正上、右上
                    if ( panLastLineVal[i]==panThisLineVal[i] and self.panPolyIdMap[panLastLineId[i]]!=self.panPolyIdMap[panThisLineId[i]] ):
                        # print("[非首列]左：true + 正上：true")
                        self.MergePolygon(panLastLineId[i], panThisLineId[i])
                        # merge(src,dst)

                    if ( panLastLineVal[i-1]==panThisLineVal[i] and self.panPolyIdMap[panLastLineId[i-1]]!=self.panPolyIdMap[panThisLineId[i]] ):
                        self.MergePolygon(panLastLineId[i - 1], panThisLineId[i])
                        # print("[非首列]左：true + 左上：true")

                    if ( i<nXSize and panLastLineVal[i+1]==panThisLineVal[i] and self.panPolyIdMap[panLastLineId[i+1]]!=self.panPolyIdMap[panThisLineId[i]] ):
                        self.MergePolygon(panLastLineId[i+1], panThisLineId[i])
                        # print("[非首列]左：true + 正上：true")
                else :
                    if ( panLastLineVal[i]==panThisLineVal[i] ):
                        if iY==21 and i==27:
                            print("enter here 2")
                        # 如果和左边像素不等，或者是第一列 -> 跟 正上 比较
			            # 向下一行传播
                        # 需要+左上、右上
                        # print(" 左：false -- 正上：true")
                        # if iY==23:
                            # print("enter here")
                            # print("panThisLineId[i]",panThisLineId[i],"panLastLineId[i]",panLastLineId[i])
                            # os.system("pause")
                        panThisLineId[i] = panLastLineId[i]
                    else :
                        # 左、正上 都不相等
                        if (i>1 and panLastLineVal[i-1]==panThisLineVal[i]):
                            if iY==21 and i==27:
                                print("enter here 3")
                            # 非首列，和左上相等
                            # print(" 左、正上：false -- 左上：true")
                            panThisLineId[i] = panLastLineId[i-1]

                            if (i<nXSize and panLastLineVal[i+1]==panThisLineVal[i] and self.panPolyIdMap[panLastLineId[i+1]]!=self.panPolyIdMap[panThisLineId[i]]):
                                # print(" 左、正上：false -- 左上：true + 右上：true")
                                self.MergePolygon(panLastLineId[i+1], panThisLineId[i]);
                        else :
                            # 首列 或者 跟 左、左上、正上 均不相等，考虑右上
                            if ( i<nXSize and panLastLineVal[i+1]==panThisLineVal[i]):
                                if iY==21 and i==27:
                                    print("enter here 4")
                                # print(" 左、左上、正上：false -- 右上：true")
                                panThisLineId[i] = panLastLineId[i+1]
                            else:
			                    # 8邻域都不相等，新的poly
                                if iY==21 and i==26:
                                    print("enter here 5")
                                    print("panThisLineVal[i]",panThisLineVal[i])
                                panThisLineId[i]=self.NewPolygon(panThisLineVal[i])
                                # print("panThisLineId[i]",panThisLineId[i])
                                # os.system("pause")
                                # print("8邻域像素都不相同：NewPoly")

            # print("==it over=="+str(i),"==")
        # print("debug:not first line")
        # os.system("pause")

    def CompleteMerges(self):
        #传播标签
        for iPoly in range(0,self.nNextPolygonId):
		    # Figure out the final id.
            # 第一次正向传播，得到根节点
            nId = self.panPolyIdMap[iPoly]
            while (nId != self.panPolyIdMap[nId]):
                nId = self.panPolyIdMap[nId]

		    # Then map the whole intermediate chain to it.
            # 第二次正向传播，所有节点写入根值
            nIdCur = self.panPolyIdMap[iPoly]
            self.panPolyIdMap[iPoly] = nId
            while (nIdCur != self.panPolyIdMap[nIdCur]):
                nNextId = self.panPolyIdMap[nIdCur]
                self.panPolyIdMap[nIdCur] = nId
                nIdCur = nNextId

            # 如果为根节点，continue
            if (self.panPolyIdMap[iPoly] == iPoly):
                self.nFinalPolyCount=self.nFinalPolyCount+1

        
    
 

