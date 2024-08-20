from vtk import *
print('\nInput pressure value: ')
pressure = int(input()) #The value for which we want the isocontour

reader = vtkXMLImageDataReader()
reader.SetFileName('Data/Isabel_2D.vti')
reader.Update()
data = reader.GetOutput()

num_cells = data.GetNumberOfCells() #62001

n_pts = data.GetNumberOfPoints()

dataArr = data.GetPointData().GetArray('Pressure')

pdata = vtkPolyData()
cells = vtkCellArray()
points = vtkPoints()

#In the folloing loop, i am scanning through the sides of cells in counterclockwise manner.
#Whenever i find a point lying on a side, i set temp_pid1, temp_pid2, temp_val1, temp_val2 for the corresponding vertices.
#Similarly when i find the second point, i set temp_pid3, temp_pid4, temp_val3, temp_val4 for the corresponding vertices.
#I am also storing a variable 'case' for checking which 2 sides have the isoline intersection. eg. case 11 means first and second side.
#This can be understood better by having a look inside the condition code

for i in range(num_cells-1):

    cell = data.GetCell(i)
    pid1 = cell.GetPointId(0)
    pid2 = cell.GetPointId(1)
    pid3 = cell.GetPointId(3)
    pid4 = cell.GetPointId(2)

    val1 = dataArr.GetTuple1(pid1)
    val2 = dataArr.GetTuple1(pid2)
    val3 = dataArr.GetTuple1(pid3)
    val4 = dataArr.GetTuple1(pid4)
    
    if (pressure>=val1 and pressure<val2):
        temp_pid1 = pid1
        temp_pid2 = pid2
        temp_val1 = val1
        temp_val2 = val2
        if (pressure>=val3):
            temp_pid3 = pid2
            temp_pid4 = pid3
            temp_val3 = val2
            temp_val4 = val3
            case = 11
        elif (pressure>=val4):
            temp_pid3 = pid3
            temp_pid4 = pid4
            temp_val3 = val3
            temp_val4 = val4
            case = 12
        else:
            temp_pid3 = pid4
            temp_pid4 = pid1
            temp_val3 = val4
            temp_val4 = val1
            case = 13
    elif (pressure<val1 and pressure>=val2):
        temp_pid1 = pid1
        temp_pid2 = pid2
        temp_val1 = val1
        temp_val2 = val2
        if (pressure<val3):
            temp_pid3 = pid2
            temp_pid4 = pid3
            temp_val3 = val2
            temp_val4 = val3
            case = 11
        elif (pressure<val4):
            temp_pid3 = pid3
            temp_pid4 = pid4
            temp_val3 = val3
            temp_val4 = val4
            case = 12
        else:
            temp_pid3 = pid4
            temp_pid4 = pid1
            temp_val3 = val4
            temp_val4 = val1
            case = 13
    elif (pressure>=val2 and pressure<val3):
        temp_pid1 = pid2
        temp_pid2 = pid3
        temp_val1 = val2
        temp_val2 = val3
        if (pressure>=val4):
            temp_pid3 = pid3
            temp_pid4 = pid4
            temp_val3 = val3
            temp_val4 = val4
            case = 21
        elif (pressure>=val1):
            temp_pid3 = pid4
            temp_pid4 = pid1
            temp_val3 = val4
            temp_val4 = val1
            case = 22
        else:
            temp_pid3 = pid1
            temp_pid4 = pid2
            temp_val3 = val1
            temp_val4 = val2
            case = 23
    elif (pressure<val2 and pressure>=val3):
        temp_pid1 = pid2
        temp_pid2 = pid3
        temp_val1 = val2
        temp_val2 = val3
        if (pressure<val4):
            temp_pid3 = pid3
            temp_pid4 = pid4
            temp_val3 = val3
            temp_val4 = val4
            case = 21
        elif (pressure<val1):
            temp_pid3 = pid4
            temp_pid4 = pid1
            temp_val3 = val4
            temp_val4 = val1
            case = 22
        else:
            temp_pid3 = pid1
            temp_pid4 = pid2
            temp_val3 = val1
            temp_val4 = val2
            case = 23
    elif (pressure>=val3 and pressure<val4):
        temp_pid1 = pid3
        temp_pid2 = pid4
        temp_val1 = val3
        temp_val2 = val4
        if (pressure>=val1):
            temp_pid3 = pid4
            temp_pid4 = pid1
            temp_val3 = val4
            temp_val4 = val1
            case = 31
        elif (pressure>=val2):
            temp_pid3 = pid1
            temp_pid4 = pid2
            temp_val3 = val1
            temp_val4 = val2
            case = 32
        else:
            temp_pid3 = pid2
            temp_pid4 = pid3
            temp_val3 = val2
            temp_val4 = val3
            case = 33
    elif (pressure<val3 and pressure>=val4):
        temp_pid1 = pid3
        temp_pid2 = pid4
        temp_val1 = val3
        temp_val2 = val4
        if (pressure<val1):
            temp_pid3 = pid4
            temp_pid4 = pid1
            temp_val3 = val4
            temp_val4 = val1
            case = 31
        elif (pressure<val2):
            temp_pid3 = pid1
            temp_pid4 = pid2
            temp_val3 = val1
            temp_val4 = val2
            case = 32
        else:
            temp_pid3 = pid2
            temp_pid4 = pid3
            temp_val3 = val2
            temp_val4 = val3
            case = 33
    elif (pressure>=val4 and pressure<val1):
        temp_pid1 = pid4
        temp_pid2 = pid1
        temp_val1 = val4
        temp_val2 = val1
        if (pressure>=val2):
            temp_pid3 = pid1
            temp_pid4 = pid2
            temp_val3 = val1
            temp_val4 = val2
            case = 41
        elif (pressure>=val3):
            temp_pid3 = pid2
            temp_pid4 = pid3
            temp_val3 = val2
            temp_val4 = val3
            case = 42
        else:
            temp_pid3 = pid3
            temp_pid4 = pid4
            temp_val3 = val3
            temp_val4 = val4
            case = 43
    elif (pressure<val4 and pressure>=val1):
        temp_pid1 = pid4
        temp_pid2 = pid1
        temp_val1 = val4
        temp_val2 = val1
        if (pressure<val2):
            temp_pid3 = pid1
            temp_pid4 = pid2
            temp_val3 = val1
            temp_val4 = val2
            case = 41
        elif (pressure<val3):
            temp_pid3 = pid2
            temp_pid4 = pid3
            temp_val3 = val2
            temp_val4 = val3
            case = 42
        else:
            temp_pid3 = pid3
            temp_pid4 = pid4
            temp_val3 = val3
            temp_val4 = val4
            case = 43
    else:
        continue
    
#After I have received all the temp_pids and temp_vals, I calculate the location of the point on the side and store those in l and r respectively
    l = [data.GetPoint(temp_pid1)[0] + (data.GetPoint(temp_pid2)[0] - data.GetPoint(temp_pid1)[0])*((pressure - temp_val1)/(temp_val2-temp_val1)),data.GetPoint(temp_pid1)[1] + (data.GetPoint(temp_pid2)[1] - data.GetPoint(temp_pid1)[1])*((pressure - temp_val1)/(temp_val2-temp_val1)),25]
    r = [data.GetPoint(temp_pid3)[0] + (data.GetPoint(temp_pid4)[0] - data.GetPoint(temp_pid3)[0])*((pressure - temp_val3)/(temp_val4-temp_val3)),data.GetPoint(temp_pid3)[1] + (data.GetPoint(temp_pid4)[1] - data.GetPoint(temp_pid3)[1])*((pressure - temp_val3)/(temp_val4-temp_val3)),25]

#Inserting points
    points.InsertNextPoint(l)
    points.InsertNextPoint(r)
#If I have case 11 i.e. the necessity for ambiguous case, then i'll check the 3rd and 4th sides too for the ambiguous case.
    if (case == 11 and ((pressure>=val3 and pressure<val4 and pressure>=val1) or (pressure<val3 and pressure>=val4 and pressure<val1))) :
        temp_pid1 = pid3
        temp_pid2 = pid4
        temp_val1 = val3
        temp_val2 = val4
        temp_pid3 = pid4
        temp_pid4 = pid1
        temp_val3 = val4
        temp_val4 = val1

    l = [data.GetPoint(temp_pid1)[0] + (data.GetPoint(temp_pid2)[0] - data.GetPoint(temp_pid1)[0])*((pressure - temp_val1)/(temp_val2-temp_val1)),data.GetPoint(temp_pid1)[1] + (data.GetPoint(temp_pid2)[1] - data.GetPoint(temp_pid1)[1])*((pressure - temp_val1)/(temp_val2-temp_val1)),25]
    r = [data.GetPoint(temp_pid3)[0] + (data.GetPoint(temp_pid4)[0] - data.GetPoint(temp_pid3)[0])*((pressure - temp_val3)/(temp_val4-temp_val3)),data.GetPoint(temp_pid3)[1] + (data.GetPoint(temp_pid4)[1] - data.GetPoint(temp_pid3)[1])*((pressure - temp_val3)/(temp_val4-temp_val3)),25]
    points.InsertNextPoint(l)
    points.InsertNextPoint(r)

polyLine3 = vtkPolyLine()
#Inserting lines according the the points stored
for i in range(0,points.GetNumberOfPoints(),2): 
    polyLine3.GetPointIds().SetNumberOfIds(2)    
    polyLine3.GetPointIds().SetId(0, i)
    polyLine3.GetPointIds().SetId(1, i+1)
    cells.InsertNextCell(polyLine3)

pdata.SetPoints(points)
pdata.SetLines(cells)

# print(pdata)

writer = vtkXMLPolyDataWriter()
writer.SetInputData(pdata)
writer.SetFileName('grp66_test_val'+str(pressure)+'.vtp')
writer.Write()