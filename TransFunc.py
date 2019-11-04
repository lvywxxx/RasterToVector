import RPolygon
import shapefile as shp
import os

class TransFunc:
    def __init__(self):
        print("_init_TransFunc")

        #/************************************************************************/
        #/*                              AddEdges()                              */
        #/*                                                                      */
        #/*      Examine one pixel and compare to its neighbour above            */
        #/*      (previous) and right.  If they are different polygon ids        */
        #/*      then add the pixel edge to this polygon and the one on the      */
        #/*      other side of the edge.                                         */
        #/************************************************************************/

    # 这个函数逻辑上没问题
    def AddEdges(self,panThisLineId,panLastLineId,panPolyIdMap,panPolyValue,papoPoly,iX,iY):
        nThisId = panThisLineId[iX];
        if( nThisId != -1 ):
            nThisId = panPolyIdMap[nThisId]
        nRightId = panThisLineId[iX+1]
        if( nRightId != -1 ):
            nRightId = panPolyIdMap[nRightId]
        nPreviousId = panLastLineId[iX]
        if( nPreviousId != -1 ):
            nPreviousId = panPolyIdMap[nPreviousId]
        nLeftId=panLastLineId[iX-1]
        if( nLeftId != -1 ):
            nLeftId = panPolyIdMap[nLeftId]

        # 这里就映射到计算机坐标了,从0开始
        iXReal = iX - 1;

        if( nThisId != nPreviousId ):
            #上下不同，添加水平线
            if( nThisId != -1 ):
                if( papoPoly[nThisId].dfPolyValue == -1 ):
                    papoPoly[nThisId] = RPolygon.RPolygon( panPolyValue[nThisId] )
                papoPoly[nThisId].AddSegment( iXReal, iY, iXReal+1, iY )
            
            if( nPreviousId != -1 ):     
                if( papoPoly[nPreviousId].dfPolyValue == -1 ):
                    papoPoly[nPreviousId] = RPolygon.RPolygon(panPolyValue[nPreviousId])
                papoPoly[nPreviousId].AddSegment( iXReal, iY, iXReal+1, iY )

        if( nThisId != nRightId ):
            if( nThisId != -1 ):
                if( papoPoly[nThisId].dfPolyValue == -1 ):
                    papoPoly[nThisId] = RPolygon.RPolygon(panPolyValue[nThisId])
                papoPoly[nThisId].AddSegment( iXReal+1, iY, iXReal+1, iY+1 )

            if( nRightId != -1 ):
                if( papoPoly[nRightId].dfPolyValue == -1 ):
                    papoPoly[nRightId] = RPolygon.RPolygon(panPolyValue[nRightId])
                papoPoly[nRightId].AddSegment( iXReal+1, iY, iXReal+1, iY+1 )

    def Clockwise(self,polyXY):
        print(1)

    def AutoClockwise(self,aanXY):
        if len(aanXY)==1:
            oVec=[aanXY[0][2]-aanXY[0][0],aanXY[0][3]-aanXY[0][1]]
            iVec=[aanXY[0][len(aanXY[0])-4]-aanXY[0][0],aanXY[0][len(aanXY[0])-3]-aanXY[0][1]]
            dirVec=oVec[0]*iVec[1]-oVec[1]*iVec[0]
            if(dirVec<0):
                aanXY[0].reverse()
            return

        bbox=[self.GetBBox(aanXY[iPoly]) for iPoly in range(0,len(aanXY))]
        height=[0 for iPoly in range(0,len(aanXY))]

        for iPoly in range(0,len(aanXY)):
            for iPolyH in range(iPoly+1,len(aanXY)):
                if bbox[iPoly][0]>bbox[iPolyH][0] and bbox[iPoly][1]>bbox[iPolyH][1]:
                    if bbox[iPoly][2]>bbox[iPolyH][2] and bbox[iPoly][3]>bbox[iPolyH][3]:
                        height[iPolyH]= height[iPoly]+1

        for iPoly in range(0,len(aanXY)):
            oVec=[aanXY[iPoly][2]-aanXY[iPoly][0],aanXY[iPoly][3]-aanXY[iPoly][1]]
            iVec=[aanXY[iPoly][len(aanXY[iPoly])-4]-aanXY[iPoly][0],aanXY[iPoly][len(aanXY[iPoly])-3]-aanXY[iPoly][1]]
            dirVec=oVec[0]*iVec[1]-oVec[1]*iVec[0]
            if height[iPoly]==0:
                if dirVec<0:
                    aanXY[iPoly].reverse()
            else:
                if dirVec>0:
                    aanXY[iPoly].reverse()

    def GetBBox(self,anXY):
        xmax=anXY[0]
        xmin=anXY[0]
        ymax=anXY[1]
        ymin=anXY[1]
        for i in range(0,int(len(anXY)/2)):
            if anXY[i*2]>xmax:
                xmax=anXY[i*2]
            if anXY[i*2]<xmin:
                xmin=anXY[i*2]
            if anXY[i*2+1]>ymax:
                ymax=anXY[i*2+1]
            if anXY[i*2+1]<ymin:
                ymin=anXY[i*2+1]
        return[xmin,xmax,ymin,ymax]