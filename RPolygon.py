import os
import copy
import random

class RPolygon:

    def __init__(self,label=-1):
        self.aanXY=[]
        self.polyXY=[]
        self.nLastLineUpdated=-1
        self.dfPolyValue=label
        self.id=random.random()
        # print("RPolygon is created")
     
    def AddSegment(self,x1,y1,x2,y2):
        # print("add segment")
        self.nLastLineUpdated = max(y1, y2);
        #/* -------------------------------------------------------------------- */
        #/*      Is there an existing string ending with this?                   */
        #/* -------------------------------------------------------------------- */

        for iString in range(0,len(self.aanXY)):
            anString = copy.deepcopy(self.aanXY[iString])
            nSSize = len(anString)

            # print("x1,y1,x2,y2:",x1,y1,x2,y2)
            # print("anString[nSSize-2],anString[nSSize-1]",anString[nSSize-2],anString[nSSize-1])
            # print("anString[nSSize-1] == y1  ?",anString[nSSize-1] == y1 )
            # print("anString[nSSize-2] == x1  ?",anString[nSSize-2] == x1 )
            # print("anString[nSSize-2] == x1 and anString[nSSize-1] == y1  ?",anString[nSSize-2] == x1 and anString[nSSize-1] == y1 )

            # print("anString",anString)
            if( anString[nSSize-2] == x1 and anString[nSSize-1] == y1 ):
                # print("enter if 1:(x1,y1)")
                # print("x1,x2",x1,x2)
                # os.system("pause")
                x1,x2=x2,x1
                y1,y2=y2,y1

            if( anString[nSSize - 2] == x2 and anString[nSSize - 1] == y2 ):
                # print("enter if 2:(x2,y2)")
                # We are going to add a segment, but should we just extend an existing segment already going in the right direction ?
                # max(x-x2,y-y2)
                nLastLen = max(abs(anString[nSSize - 4] - anString[nSSize - 2]),abs(anString[nSSize - 3] - anString[nSSize - 1]))

                if( nSSize >= 4 and (anString[nSSize - 4] - anString[nSSize - 2] == (anString[nSSize - 2] - x1) * nLastLen) 
                                and (anString[nSSize - 3] - anString[nSSize - 1] == (anString[nSSize - 1] - y1) * nLastLen) ):
                    self.aanXY[iString].pop()
                    self.aanXY[iString].pop()

                self.aanXY[iString].append( x1 )
                self.aanXY[iString].append( y1 )
                #os.system("pause")

                # print("***********************************************return")
                return
                # print("not return")

        #/* -------------------------------------------------------------------- */
        #/*      Create a new string.                                            */
        #/* -------------------------------------------------------------------- */
        anString=[x1,y1,x2,y2]
        self.aanXY.append(anString)

    def Merge(self,iBaseString,iSrcString,iDirection):
        # print("merge")
        anBase = copy.deepcopy(self.aanXY[iBaseString])
        anString = copy.deepcopy(self.aanXY[iSrcString])
        iStart = 1
        iEnd = -1

        if( iDirection == 1 ):
            iEnd = int((len(anString))/2)
        else:
            iStart = int(len(anString)/2-2)

        # 把anString的值添加到iBaseString后面
        for i in range(iStart,iEnd,iDirection):
            self.aanXY[iBaseString].append( anString[i*2+0] )
            self.aanXY[iBaseString].append( anString[i*2+1] )
        
        # 最后一组数据填充src，可以直接pop缩小规模
        if( iSrcString < (len(self.aanXY)-1) ):
            self.aanXY[iSrcString]=copy.deepcopy(self.aanXY[len(self.aanXY)-1])

        self.aanXY.pop()
        # print(self.aanXY)
        # print("merge pause:")
        # os.system("pause")
        

    def Dump(self):
        print("dump")
        for iString in range(0,len(self.aanXY)):
            anString = self.aanXY[iString]
            print( "  String %d:\n", static_cast<int>(iString) )
            for iVert in range(0,len(anString2),2):
                print( "    (%d,%d)\n", anString[iVert], anString[iVert+1] )

    def Colesce(self):
        """
        # print("colesce")
        #/* -------------------------------------------------------------------- */
        #/*      Iterate over loops starting from the first, trying to merge     */
        #/*      other segments into them.                                       */
        #/* -------------------------------------------------------------------- */    
        # for iBaseString in range(0,len(self.aanXY)):

        for iBaseString in range(0,len(self.aanXY)):
            endflag=True
            
            # print("|| colesce main it:",itr)
            # print("len(self.aanXY)",len(self.aanXY))
            #这里不需要判别iBaseString==1的情况，len.aanxy==1，那么下面for循环就会return
            if iBaseString>=len(self.aanXY):
                return

            while (endflag):
                anBase = copy.deepcopy(self.aanXY[iBaseString])
                bMergeHappened = True     
            #/* -------------------------------------------------------------------- */
            #/*      Keep trying to merge the following strings into our target      */
            #/*      "base" string till we have tried them all once without any      */
            #/*      mergers.                                                        */
            #/* -------------------------------------------------------------------- */
                while( bMergeHappened ):
                    bMergeHappened = False;
            #/* -------------------------------------------------------------------- */
            #/*      Loop over the following strings, trying to find one we can      */
            #/*      merge onto the end of our base string.                          */
            #/* -------------------------------------------------------------------- */
                    for iString in range(iBaseString+1,len(self.aanXY)):
                        if iString>=len(self.aanXY):
                            break

                        anString = self.aanXY[iString]
                        # print("anBase",anBase)
                        # print("anString",anString)
                        if( anBase[len(anBase)-2]==anString[0] and anBase[len(anBase)-1]==anString[1] ):
                            # print("enter 1")
                            self.Merge(iBaseString,iString,1)
                            bMergeHappened = True
                        else :
                            if( anBase[len(anBase)-2]==anString[len(anString)-2] and anBase[len(anBase)-1]==anString[len(anString)-1] ):
                                # print("enter -1")
                                self.Merge( iBaseString,iString,-1)
                                bMergeHappened = True

                # 每次大循环完毕，检查首尾是否已经衔接，如果已经衔接，一个多边形已经封闭
                if(anBase[0]==anBase[len(anBase)-2] and anBase[1]==anBase[len(anBase)-1]):
                    endflag=False
        """
        
        for iBaseString in range(0,len(self.aanXY)):
            if iBaseString>=len(self.aanXY):
                return

            itflag=True

            while itflag:
                # 这个flag的风险在于如果没有闭环就会死循环
                anBase=copy.deepcopy(self.aanXY[iBaseString])

                for iString in range(iBaseString+1,len(self.aanXY)):
                    if iString>=len(self.aanXY):
                        break

                    anString=copy.deepcopy(self.aanXY[iString])

                    if( anBase[len(anBase)-2]==anString[0] and anBase[len(anBase)-1]==anString[1] ):
                        # print("enter 1")
                        self.Merge(iBaseString,iString,1)
                    else :
                        if( anBase[len(anBase)-2]==anString[len(anString)-2] and anBase[len(anBase)-1]==anString[len(anString)-1] ):
                            # print("enter -1")
                            self.Merge( iBaseString,iString,-1)

                    if(self.aanXY[iBaseString][0]==self.aanXY[iBaseString][len(self.aanXY[iBaseString])-2])and(self.aanXY[iBaseString][1]==self.aanXY[iBaseString][len(self.aanXY[iBaseString])-1]):
                        itflag=False
                        break
                        # 闭环完成，跳出小循环，跳出

    def Trans(self):
        # self.polyXY=[[[self.aanXY[i*2],self.aanXY[i*2+1]] for i in range(0,len(self.aanXY)/2-1)]]
        # 转化为pyshp需要的格式
        for iP in range(0,len(self.aanXY)):
            self.polyXY.append([])
            for iQ in range(0,int(len(self.aanXY[iP])/2)):
                # print("len(self.aanXY[iP])",len(self.aanXY[iP]))
                # print("self.aanXY[iP][iQ+1]",self.aanXY[iP][iQ+1])
                # print("polyXY[iP]",self.polyXY[iP])
                # os.system("pause")
                self.polyXY[iP].append([self.aanXY[iP][iQ*2],self.aanXY[iP][iQ*2+1]])

        # print("polyXY",self.polyXY)
        # os.system("pasue")
        # print("aanXY",self.aanXY)