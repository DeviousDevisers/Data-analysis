
import plotly; plotly.tools.set_credentials_file(username='deviousdevisers', api_key='2893d9w6uc')
import plotly.plotly as py
from plotly.graph_objs import *
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib import pylab
import pylab as pl
import matplotlib.mlab as mlab
from pylab import *
import numpy as np

class CSVReader(object):
    '''Extracts informtion from a csv file.'''

    def __init__(self, fname=None):
        '''Constructor - opens the input file and gets ready to parse it.'''
        self.fname = fname
        if fname == None:
            return
        entry = ''
        self.csv = []
        row = []
        inQuotes = False
        skip = False
        csvIn = open(fname).read()
        for i in range(len(csvIn)):
            if skip:
                skip = False
                continue
            letter = csvIn[i]
            if inQuotes:
                if letter == '"':  # Could be first of a pair, or the closing quote.
                    if csvIn[i+1] == '"':  # Current quote is the first of a pair.
                       entry += '"'
                       skip = True
                    else:  # Current quote is the closing quote.
                        inQuotes = False
                        continue
                else:
                    entry += letter
            else:
                isComma = (letter == ',')
                isNewline = (letter == '\n')
                isQuote = (letter == '"')
                if not (isComma or isNewline or isQuote):
                    entry += letter
                elif isComma:
                    row.append(entry)
                    entry = ''
                elif isNewline:
                    row.append(entry)
                    entry=''
                    if row != []:
                        self.csv.append(row)
                    row = []
                    
                else:
                    inQuotes = True
                
    
        
    
    def __str__(self):
        return 'CSVReader object'
        
    def nCols(self):
        '''
        nCols() -> int
        returns the number of coloumns.
        '''
        return len(self.csv[0])

    def nRows(self):
        '''
        nCols() -> int
        returns the number of rows.
        '''
        if self.hasColumnHeadings():
            return len(self.csv)-1
        return len(self.csv)
        
    
    def row(self, n):
        '''
        makes a list with the elements in a row
        returns the list
        '''
        return self.csv[n]

    def col(self, n):
        '''
         makes a list with the elements in a column and returns it.
         '''
        column = []
        for row in self.csv:
            column.append(row[n])
##        if self.hasColumnHeadings():
##            return column[1:]
##        else:
        return column
            
    
    def uniqueElement(self, heading):
        uniqueElements=[]
        for element in self.values(heading):
            if element not in uniqueElements:
                uniqueElements.append(element)
            
        return uniqueElements
    

    def hasColumnHeadings(self):
        '''
        CR.hasColumnHeadings() -> bool
        Returns True if the top row contains no numeric entries. False otherwise.
           '''
        for entry in self.row(0):
            if entry.isnumeric() :
                return False
        return True           

    def mixedIdList(self):
        schoolIdList = self.values('SchoolId')
        yearIdList = self.values('YearId')
        mergedList = []
        for i in range(len(schoolIdList)):
            mergedId = schoolIdList[i] + '-' + yearIdList[i]
            mergedList.append(mergedId)
        return mergedList

    def values(self, heading):
        '''
        Makes a list with the elements in a column given the heading of the column.'''
        
        return self.col(self.row(0).index(heading))
        
    def value(self, row, col):
        '''
        Returns the element located at row , col.
        '''
        if type(col) == str:
            col = self.row(0).index(col)
        return self.row(row)[col]

    def rowValues(self, heading):
        return self.row(self.col(0).index(heading))
    
    def dataOfId(self, mergedId, mergedList, columnName):
        index = mergedList.index(mergedId)
        return self.value(index, columnName)

class CSVeditor(object):

    def __init__(self, fname=None):
        if fname == None:
            return
        self.R=CSVReader(fname)
        self.fname=fname

        
    def merger(self,column1, column2):
        fname=self.fname
        newColumn = column1 + '-' + column2
        newFile = open(fname+ 'w')
        firstRow = R.row(0)
        index1 = firstRow.index(column1)
        index2 = firstRow.index(column2)
        for element in firstRow:
            if element != column1 and element != column2:
                newFile.write(element+',')
            elif element == column1:
                newFile.write(newColumn+',')
        newFile.write('\n')
        for row in range(R.nRows()-1):
            try:
                currentRow = R.row(row+1)
                if currentRow == ['']:
                    continue
                lastRow = currentRow
                column1 = currentRow[index1]
                column2 = currentRow[index2]
                newColumn = column1 + '-' + column2
                for element in currentRow:
                    if element != column1 and element != column2:
                        newFile.write(element+',')
                    elif element == column2:
                        newFile.write(newColumn+',')
                newFile.write('\n')
            except:
                print('Error occured. row: {}\ncurrentRow: {}\n'.format(row, currentRow))

        newFile.close()

        
    def IdMatcher(self, fname1, fname2):
        extraIdList = []
        file1 = CSVReader(fname1)
        file2 = CSVReader(fname2)
        schoolIdList1 = file1.values('SchoolId')
        schoolIdList2 = file2.values('SchoolId')
        yearIdList1 = file1.values('YearId')
        yearIdList2 = file2.values('YearId')
        mergedList1 = []
        mergedList2 = []
        for i in range(len(schoolIdList1)):
            mergedId1 = schoolIdList1[i] + '-' + yearIdList1[i]
            mergedList1.append(mergedId1)
        for i in range(len(schoolIdList2)):
            mergedId2 = schoolIdList2[i] + '-' + yearIdList2[i]
            mergedList2.append(mergedId2)
        for j in mergedList1:
            if j not in mergedList2:
                extraIdList.append(file1.fname + '-' + j)
            else:
                mergedList2.remove(j)
        for k in mergedList2:
            extraIdList.append(file2.fname + '-' + k)
        return extraIdList


    def uniqueId(self,fname):
        doubleId = []
        file = CSVReader(fname)
        schoolIdList = file.values('SchoolId')
        yearIdList = file.values('YearId')
        mergedList = []
        for i in range(len(schoolIdList)):
            mergedId = schoolIdList[i] + '-' + yearIdList[i]
            if mergedId not in mergedList:
                mergedList.append(mergedId)
            else:
                doubleId.append(mergedId)
        return doubleId

    


    def merger2(self,listOfColumns,newColumnName):
        ### assuming that column heads in the list are in order.[h0 h1 h2] add operation argument
        fname=self.fname
        newColumn = []
        idx=[]
        ncol=R.nCols()
        firstRow = R.row(0)
        lastHeadingidx=ncol+1- len(listOfColumns)
        for item in listOfColumns:
            idx.append(firstRow.index(item))
        firstCol= idx[0]
        newFile = open(fname, 'w')
        for row in range(R.nRows()):
            total= 0
            a=','
            for item in listOfColumns:
                data=R.value(row, item)    
                if data.isnumeric():
                    total= total + int(data)
            for i in range(R.nCol()):
                if i ==  firstCol:
                    if row == 0:
                        newFile.write(newColumnName + a)
                    else:
                        newFile.write(str(total) + a)
                elif i not in idx:
                    if (i == lastHeadingidx):
                        a='\n'
                    newFile.write(R.row(row)[i]+a)

    
    def commonColumns(self,fname1,fname2):
        final = []
        file1 = CSVReader(fname1)
        file2 = CSVReader(fname2)
        headings1 = file1.row(0)
        headings2 = file2.row(0)
        for i in headings1:
            if i in headings2:
                final.append(i)
        final.remove('SchoolId')
        final.remove('YearId')
        return final

    def extraIds(self,fname):
        file = CSVReader(fname)
        missingIds = []
        schoolIds = file.uniqueElement('SchoolId')[1:]
        yearIds = file.uniqueElement('YearId')[1:]
        schoolIdList = file.values('SchoolId')
        yearIdList = file.values('YearId')
        print(len(schoolIds),len(yearIds), yearIds, len(schoolIds)* len(yearIds))
        mergedList = []
        for i in range(len(schoolIdList)):
            mergedId = schoolIdList[i] + '-' + yearIdList[i]
            mergedList.append(mergedId)
        print (len(mergedList))
        return len(schoolIds)* len(yearIds)-len(mergedList)
        for school in schoolIds:
            for year in yearIds:
                mergedItem = school + '-' + year
                if mergedItem not in mergedList:
                    missingIds.append(mergedItem)
        return len(missingIds)


    def dataCorrectness(self,fname1,fname2):
        listOfColumns = self.commonColumns(fname1,fname2)
        file1 = CSVReader(fname1)
        file2 = CSVReader(fname2)
        mergedIds1 = file1.mixedIdList()
        mergedIds2 = file2.mixedIdList()
        for column in listOfColumns:
            incorrectData = [column]
            for i in mergedIds1:
                if i in mergedIds2:
                    data1 = file1.dataOfId(i,mergedIds1,column)
                    data2 = file2.dataOfId(i,mergedIds2,column)
                    if data1 != data2:
                        incorrectData.append({fname1+'-'+i+'-'+data1,fname2+'-'+i+'-'+data2})
            print(incorrectData)       


    def allCorrectness(self):
        self.dataCorrectness('SchoolDetailedInfo.csv','WorkingNonTeachingStaff.csv')
        print('pappu')
        self.dataCorrectness('WorkingTeachingStaff.csv','WorkingNonTeachingStaff.csv')


##    def uniqueId(self,*filelist):
##        final=[]
##        headings1=[]
##        csvs=[]
##        for i in filelist:
##            print(i)
##            self.openFile(i)
##            headings=R.row(0)
##            headings1.append(headings)
##            csvs.append(R.csv)
##        for j in range(len(headings1)-1):
##            for element in headings1[0]:
##                if element in headings1[j+1]:
##                    final.append(element)
##        for heading in final:
##            R.csv=csvs[0]
##            print(len(R.csv))
##            R.values(heading)
##            colvalues=R.colList
##            for csv in range(len(csvs)-1):
##                R.csv=csvs[csv+1]
##                print(len(R.csv))
##                R.values(heading)
##                if colvalues != R.colList:
##                    return False
##        return True
            
##           
##            listoflists.append(headings)
##        rowlen=0
##        for colslist in listoflists:
##            if rowlen==0:
##                rowlen=len(colslist)
##            else:
##                if len(colslist)!=rowlen:
##                    
##                                
##            newFile.write(total)
##            newColumn.append(total)
##            try:
##                currentRow = R.row(row+1)
##                if currentRow == ['']:
##                    continue
###                R.lastRow = currentRow
##                column1 = currentRow[index1]
##                column2 = currentRow[index2]
##                newColumn = column1 + '-' + column2
##                for element in currentRow:
##                    if element != column1 and element != column2:
##                        newFile.write(element+',')
##                    elif element == column2:
##                        newFile.write(newColumn+',')
##                newFile.write('\n')
##            except:
##                print('Error occured. row: {}\ncurrentRow: {}\n'.format(row, currentRow))
##        newFile.close()
##        
##    def openFile(self):
##        fname=self.fname
##        if 'edited' not in fname:
##            fname=self.fname.replace('.csv','')+'edited.csv'
##        csv=open(self.fnew).read()
##        R.csv=csv.split('\n')
##        self.fname = fname
        
        
class CSVStatistics(object):

    def __init__(self, fname=None):
        self.R=CSVReader(fname)
        self.fname=fname
        

    
    def colFill(self,heading):
        '''
       returns number of filled items in a column
        '''
        count=0
        if type(heading)== int:
            column = R.col(heading)
        elif type(heading)==str:
            column = R.values(heading)
        for element in column:
            element.strip()
            if element != '':
                count+=1
        return count
                

    def colFillPercentage(self,heading):
        '''Returns the percentage of filled entries in a column'''
        validCount = self.colFill(heading)
        countPercentage = validCount*100/self.R.nRows()
        return countPercentage

##    def colUsefulness(self, heading):
##        countPercentage=self.percentageCounter(heading)
##        if countPercentage< 25:
##            return 'countPercentage = ' + str(countPercentage) + ';sparse data'
##        elif countPercentage > 75:
##            return 'countPercentage = ' + str(countPercentage) + ';sufficient data'
##        else:
##            return 'countPercentage = ' + str(countPercentage) + ';data might be insufficient'
##        

    def usefulCols(self):
        '''
        Returns a list of percentages of filled entries for each column
        Shows what percentage of each column has useful data.
        '''
        if self.R.hasColumnHeadings():
            start = 1
        else:
            start = 0
        usefulColumns = [0] * R.nCols()
        for row in R.csv[start:]:
            for i in range(len(row)):
                entry = row[i]
                if entry != '':
                    usefulColumns[i] += 1
        for i in range(len(usefulColumns)):
            usefulColumns[i] *= 100 / R.nRows()
        return usefulColumns
            
##     def uniqueId(self,*filelist):
##        final=[]
##        headings1=[]
##        csvs=[]
##        for i in filelist:
##            print(i)
##            self.openFile(i)
##            headings=R.row(0)
##            headings1.append(headings)
##            csvs.append(R.csv)
##        for j in range(len(headings1)-1):
##            for element in headings1[0]:
##                if element in headings1[j+1]:
##                    final.append(element)

    def categoryCounter(self):
        if self.R.hasColumnHeadings():
            start = 1
        else:
            start = 0
        usefulColumns = [0] * self.R.nCols()
        for row in self.R.csv[start:]:
            for i in range(len(row)):
                entry = row[i]
                if entry != '':
                    usefulColumns[i] += 1
        nRows = self.R.nRows()
        for i in range(len(usefulColumns)):
            usefulColumns[i] *= nRows
        return usefulColumns


    def columnBarChart(self, filename, xaxis, yaxis):
        '''
        Generates a bar chart to show the usefulness of each column in terms of percentage of filled entries.
        '''
        data = Data([
        Bar(
        x=self.R.row(0),
        y=self.categoryCounter())
        ])
        layout = Layout(
            title=' Percentage of filled entries in each column in' + str(self.fname),
            xaxis=XAxis(
                title=xaxis,
                titlefont=Font(
                    family='Courier New, monospace'
                )
            ),
            yaxis=YAxis(
                title=yaxis,
                titlefont=Font(
                    family='Courier New, monospace'
                )
            )
        )
        fig = Figure(data=data, layout=layout)
        plot_url = py.plot(fig, filename=filename)

    def schoolsCategoryCounter(self, numberORpercentage):
        '''
        returns a lsit od length 10. Each index of the list represents a percentage category.
        For example, index 0 represents the percentage of rows with  0 % to 10 % of filled entries
        idenx 1 represents the percentage of rows with 10 to 20 % of filled entries. 
        '''
        count = 0
        if self.R.hasColumnHeadings():
            start = 1
        else:
            start = 0
        usefulRows = [0] * 10
        for row in self.R.csv[start:]:
            for entry in row:
                if entry != '':
                    count+=1
            category = self.percentageCategorizer(count)
            usefulRows[category] += 1
            count = 0
        usefulRowsPercentage = []
        nRows = self.R.nRows()-1
        for item in usefulRows:
            itemPercentage = item*100/nRows
            usefulRowsPercentage.append(itemPercentage)
        if numberORpercentage == 'number':
            return usefulRows
        elif numberORpercentage == 'percentage':
            return usefulRowsPercentage


    def schoolsInCategory(self, percentageCategory, number1=0, number2=-1):
        '''
        Given a percentage category in units of 10, returns the school
        '''
        count = 0
        rownum=1
        schools=[[],[],[],[],[],[],[],[],[], []]
        for row in R.csv[1:]:
            schoolId=self.R.value(rownum, 'SchoolId')
            year=self.R.value(rownum, 'Year')
            for entry in row:
                if entry != '':
                    count+=1
            category = self.percentageCategorizer(count)
            schools[category].append((schoolId,year))
            count=0
            rownum+=1
        SchoolsInCategory= schools[percentagecategory/10]
        if number2!= -1:
            SchoolsNeeded=schools[category/10][number1:number2+1]
        else:
            SchoolsNeeded=schools[category/10][number1:]
            
        if len(SchoolsNeeded) <= len((SchoolsInCategory)):
                return SchoolsNeeded
        else:
            print('insufficient data in category')
            
    def CategoryProgression(self, IdReq):
        schools=self.schoolsInCategory()
        years={}
        for year in self.R.values('Year'):
            if year not in years:
                years[year]=[]
        for category in schools:
            for school in category:
                year=school[1]
                Id=school[0]
                years[year].append(Id)    

    def rowBarChart(self, filename, xaxis, yaxis):
        data = Data([
        Bar(
        x=['(0-10)%', '(10-20)%', '(20-30)%', '(30-40)%', '(40-50)%', '(50-60)%', '(60-70)%', '(70-80)%', '(80-90)%', '(90-100)%'],
        y=self.schoolsCategoryCounter('percentage'))
        ])
        layout = Layout(
            title=' Percentage of filled entries in each row in' + str(self.fname),
            xaxis=XAxis(
                title=xaxis,
                titlefont=Font(
                    family='Courier New, monospace'
                )
            ),
            yaxis=YAxis(
                title=yaxis,
                titlefont=Font(
                    family='Courier New, monospace'
                )
            )
        )
        fig = Figure(data=data, layout=layout)
        plot_url = py.plot(fig, filename=filename)
        

    def percentageCategorizer(self, count):
        noCols = self.R.nCols()
        return count*10//noCols

    
    def rowFill(self,rownumber):
        '''
       returns number of filled items in a row
        '''
        count=0
        for element in self.R.row(rownumber):
            element.strip()
            if element != '':
                count+=1
        return count

    def rowPercentageCounter(self,rownumber):
        validCount = self.rowFill(rownumber)
        countPercentage = (validCount*100)//self.R.nCols()
        return countPercentage

    def rowUsefulness(self,rownumber):
        countPercentage=self.rowPercentageCounter(rownumber)
        if countPercentage< 25:
            return 'countPercentage = ' + str(countPercentage) + ';sparse data'
        elif countPercentage > 75:
            return 'countPercentage = ' + str(countPercentage) + ';sufficient data'
        else:
            return 'countPercentage = ' + str(countPercentage) + ';data might be insufficient'
        

    def rowCategory(self):
        self.RowList ={}
        for i in range(self.R.nRows()-1):
            self.RowList[i+1]=self.rowUsefulness(i+1)


class Stage1Analyzer(object):

    def __init__(self,fname):
        
        self.R = CSVReader(fname)
        self.fname = fname 

    def generateTable(self,headingList=['Average Enrollment', 'Total Enrollment', 'Number of Schools'],name='stable.csv', categoryReq='TotalEnrollment', rowHeading='District', colHeading='Year'):
        table=open(name, 'w')
        cols=self.R.uniqueElement(colHeading)
        length=len(cols)
        for heading in headingList:
            table.write(',' + heading + ','*(length-1))
        table.write('\n')
        rows=self.R.uniqueElement(rowHeading)
        rows.remove('Not Specified')
        table.write(rowHeading + '-' + colHeading)
        for heading in cols[1:-1]:
               table.write(','+ heading)* len(headingList)
        table.write(','+ cols[-1]+'\n')
        rowLen = len(cols)
        noSchools =[]
        enrollList = []
        for rowcategory in rows[1:]:
               table.write(rowcategory)
               for heading in cols[1:]:
                   ## heading is the year, ie, 2011-12
                   schoolIds=self.columnMatch(rowHeading, rowcategory, colHeading, heading, categoryReq)
                   noSchools.append(len(schoolIds))
                   sumEnroll=0
                   for enrollment in schoolIds:
                       if enrollment != '':
                           sumEnroll+=int(enrollment)
                   enrollList.append(sumEnroll)
                   average= sumEnroll//len(schoolIds)
                   table.write(','+str(average))
               for enroll in enrollList:
                   table.write(','+str(enroll))
               for length in noSchools:
                   table.write(','+str(length))
               table.write('\n')
        table.close()
        return name
                   

    def columnMatch(self, category1,category1Val, category2, category2Val, categoryReq):
        categoryReqVals=[]
        values1=self.R.values(category1)
        values2=self.R.values(category2)
        for row in range(self.R.nRows()) :
               if values1[row] == category1Val:
                   if values2[row] == category2Val:
                       match=self.R.value(row, categoryReq)
                       categoryReqVals.append(match)
        return categoryReqVals
            
    def districtLinePlot(self):
        name=self.generateTable()
        table=open(name, 'r')
        reader=CSVReader(name)
        x=reader.csv[1][1:6]
        xaxis=[]
        for i in x:
            i=int(i[-2:])
            xaxis.append(i)
        ma=[]
        mb=[]
        mc=[]
        for row in reader.csv[2:]:
            district=row[0]
            y=row[1:6]
            y1=[]
            for i in y:
                i=int(i)
                y1.append(i)
            y=row[6:11]
            y2=[]
            for i in y:
                i=int(i)
                y2.append(i)
            y=row[11:16]
            y3=[]
            for i in y:
                i=int(i)
                y3.append(i)
            (m1,b1) = polyfit(xaxis,y1,1)
            (m2,b2) = polyfit(xaxis,y2,1)
            (m3,b3) = polyfit(xaxis,y3,1)
            ma.append((m1, district))
            mb.append((m2, district))
            mc.append((m3, district))
            yp1 = polyval([m1,b1],xaxis)
            yp2 = polyval([m2,b2],xaxis)
            yp3 = polyval([m3,b3],xaxis)
            plot(xaxis,yp1)
##            plot(xaxis,yp2)
##            plot(xaxis,yp3)
            scatter(xaxis,y1)
##            scatter(xaxis,y2)
##            scatter(xaxis,y3)
            grid(True)
            xlabel('Year')
            ylabel('Average Enrollment')
            title('Average Enrollment for ' + district)
##            show()
        return [ma, mb, mc]
                
    
                   
    def districtDataPercentage(self,district,yearId):
        schools = self.columnMatch('District', district, 'YearId', yearId, 'SchoolId')
        print (len(schools))
        stats = CSVStatistics(self.fname)
        schoolList=self.R.values('SchoolId')
        yearList=self.R.values('YearId')
        totalFilled = 0
        for school in schools:
            yearStart = yearList.index(yearId)
            rowNumber = schoolList[yearStart:].index(school) + yearStart
            filledItems = stats.rowFill(rowNumber)
            totalFilled = totalFilled + filledItems
        averageFilled = totalFilled / len(schools)
        return averageFilled
    

    def districtWiseBarCharts(self,xaxis='',yaxis='Average Percentage Of Filled Items In Each District'):
        districts = self.R.uniqueElement('District')[1:]
        districts.remove('Not Specified')
        yearIds = self.R.uniqueElement('YearId')[1:]
        print (districts,yearIds)
        for year in yearIds:
            filledColumns = []
            columnPercentages = []
            nColumns = self.R.nCols()
            for district in districts:
                filledColumns.append(self.districtDataPercentage(district,year))
            for item in filledColumns:
                itemPercentage = item*100/nColumns
                columnPercentages.append(itemPercentage)
            data = Data([
            Bar(
            x=districts,
            y=columnPercentages)
            ])
            layout = Layout(
                title = 'Percentage of filled entries in each row of each district in the year 20' + str(int(year)-1) + '-' + year,
                xaxis=XAxis(
                    title=xaxis,
                    titlefont=Font(
                        family='Courier New, monospace'
                    )
                ),
                yaxis=YAxis(
                    title=yaxis,
                    titlefont=Font(
                        family='Courier New, monospace'
                    )
                )
            )
            fig = Figure(data=data, layout=layout)
            plot_url = py.plot(fig, filename='District Wise Bar Chart for the year 20' + str(int(year)-1) + '-' + year)
                


    def overallSpatialBar(self,colHeading):
        districts = self.R.uniqueElement(colHeading)[1:]
        if 'Not Specified' in districts:
            districts.remove('Not Specified')
        length = len(districts)
        districtCounter = [0] * length
        fillingCounter = [0] * length
        averageCounter = [0] * length
        newDistricts = []
        stats = CSVStatistics(self.fname)
        for i in range(len(self.R.csv)):
            districtName = self.R.value(i,colHeading)
            if districtName in districts:
                index = districts.index(districtName)
                districtCounter[index] += 1
                fillingCounter[index] += stats.rowFill(i)
        for i in range(len(fillingCounter)):
            averageCounter[i] = fillingCounter[i] / districtCounter[i]
        nCols = self.R.nCols()
        for i in range(len(averageCounter)):
            averageCounter[i] = averageCounter[i] * 100 /nCols
        sortedCounter = sorted(averageCounter)
        for i in sortedCounter:
            index = averageCounter.index(i)
            newDistricts.append(districts[index])
        data = Data([
        Bar(
        x=newDistricts,
        y=sortedCounter)
        ])
        layout = Layout(
            title = 'Overall Percentage Of Filled Entries In Each ' + colHeading ,
            xaxis=XAxis(
                title='',
                titlefont=Font(
                    family='Courier New, monospace'
                )
            ),
            yaxis=YAxis(
                title='Average Percentage Of Filled Items In Each ' + colHeading,
                titlefont=Font(
                    family='Courier New, monospace'
                )
            )
        )
        fig = Figure(data=data, layout=layout)
        plot_url = py.plot(fig, filename=colHeading + ' Wise Bar Chart For Filled Entries')
            
    def bara(self):
        bar = ['CircleOffice','UnionCouncil']
        for i in bar:
            self.overallSpatialBar(i)

    def districtSlopePlot(self, xaxis='', yaxis='slope'):
        m=self.districtLinePlot()
        avgEnrl=m[0]
        avgEnrl.sort()
        ttlEnrl=m[1].sort()
        noSchools=m[2].sort()
        x=[]
        y=[]
        for i in avgEnrl:
            slope=i[0]
            district=i[1]
            x.append(district)
            y.append(slope)

        fig = pl.figure()
        ax = pl.subplot(111)
        width=0.8
        ax.bar(range(len(x)), y)
        ax.set_xticks(np.arange(len(x)) + width/2)
        ax.set_xticklabels(x, rotation=58)
        ax.set_title('Average Enrollment Rate for Districts')
        ax.set_xlabel('District')
        ax.set_ylabel('Average Enrollment Rate')
        for item in (ax.get_xticklabels()):
            item.set_fontsize(8.5)
        show()
            



                        


    


    


    
            
            



    


    
            
            
