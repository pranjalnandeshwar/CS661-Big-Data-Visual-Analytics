
import vtk
def rk4_integration(start_point, step_size, max_steps, probe_filter, bounds):
    points = vtk.vtkPoints() #new points array
    points.InsertNextPoint(start_point) #appending point
    
    current_point_index = probe_filter.GetOutput().FindPoint(start_point) # Find the closest point in the data set to the specified point 
    current_point = start_point

    for _ in range(max_steps):
        # Forward integration
        temp= vtk.vtkPoints()
        temp.InsertNextPoint(current_point)
        tempdata=vtk.vtkPolyData()
        tempdata.SetPoints(temp)
        probe_filter.SetInputData(tempdata)
        probe_filter.SetSourceData(data)
        probe_filter.Update() #updating probe_filter
        k1 = probe_filter.GetOutput().GetPointData().GetVectors().GetTuple(0) # Get the interpolated vector at the specified point, op = (,,)
        # probe_filter.Update()
        k1 = [step_size * x for x in k1]

        next_point = [current_point[i] + 0.5 * k1[i] for i in range(3)]
        if not all(bounds[2*i] <= next_point[i] <= bounds[2*i+1] for i in range(3)):
            break
        next_point_indices = probe_filter.GetOutput().FindPoint(next_point) # Find the closest point in the data set to the specified point
        if next_point_indices == -1:
            break
        temp= vtk.vtkPoints()
        temp.InsertNextPoint(next_point)
        tempdata=vtk.vtkPolyData()
        tempdata.SetPoints(temp)
        probe_filter.SetInputData(tempdata)
        probe_filter.SetSourceData(data)
        probe_filter.Update()
        k2 = probe_filter.GetOutput().GetPointData().GetVectors().GetTuple(0)
        # probe_filter.Update()
        k2 = [step_size * x for x in k2]

        next_point = [current_point[i] + 0.5 * k2[i] for i in range(3)] # Find the closest point in the data set to the specified point
        if not all(bounds[2*i] <= next_point[i] <= bounds[2*i+1] for i in range(3)):
            break
        next_point_indices = probe_filter.GetOutput().FindPoint(next_point) # Find the closest point in the data set to the specified point
        if next_point_indices == -1:
            break
        temp= vtk.vtkPoints()
        temp.InsertNextPoint(next_point)
        tempdata=vtk.vtkPolyData()
        tempdata.SetPoints(temp)
        probe_filter.SetInputData(tempdata)
        probe_filter.SetSourceData(data)
        probe_filter.Update()
        k3 = probe_filter.GetOutput().GetPointData().GetVectors().GetTuple(0)
        # probe_filter.Update()
        k3 = [step_size * x for x in k3]

        next_point = [current_point[i] + k3[i] for i in range(3)]
        if not all(bounds[2*i] <= next_point[i] <= bounds[2*i+1] for i in range(3)):
            break
        next_point_indices = probe_filter.GetOutput().FindPoint(next_point) # Find the closest point in the data set to the specified point
        if next_point_indices == -1:
            break
        temp= vtk.vtkPoints()
        temp.InsertNextPoint(next_point)
        tempdata=vtk.vtkPolyData()
        tempdata.SetPoints(temp)
        probe_filter.SetInputData(tempdata)
        probe_filter.SetSourceData(data)
        probe_filter.Update()
        k4 = probe_filter.GetOutput().GetPointData().GetVectors().GetTuple(0)
        # probe_filter.Update()
        k4 = [step_size * x for x in k4]

        next_point = [current_point[i] + (k1[i] + 2*k2[i] + 2*k3[i] + k4[i]) / 6 for i in range(3)]

        points.InsertNextPoint(next_point)
        current_point_index = probe_filter.GetOutput().FindPoint(next_point) # Find the closest point in the data set to the specified point
        if current_point_index == -1:
            break
        current_point = next_point
    # print(points)
    return points

reader = vtk.vtkXMLImageDataReader()
reader.SetFileName("tornado3d_vector.vti")
reader.Update()
data = reader.GetOutput()
# print(data)

# Seed location
print('Input seed location: \n')
seed_point = [0, 0, 7]
# seed_point[0] = float(input("x: "))
# seed_point[1] = float(input("y: "))
# seed_point[2] = float(input("z: "))
step_size = 0.05
max_steps = 1000

probe_filter = vtk.vtkProbeFilter()
probe_filter.SetInputData(data)
# probe_filter.SetValidPointMaskArrayName("valid")
probe_filter.SetSourceData(data)
probe_filter.Update()

bounds = data.GetBounds()

# Trace backward
backward_points = rk4_integration(seed_point, -step_size, max_steps, probe_filter, bounds)

# Trace forward
forward_points = rk4_integration(seed_point, step_size, max_steps, probe_filter, bounds)

# forward_points.GetPoint(0)

# Combine backward, seed, and forward points
streamline_points = vtk.vtkPoints() #638
for i in range(backward_points.GetNumberOfPoints()-1,0,-1):
    point = [backward_points.GetPoint(i)[j] for j in range(3)] #going from the most backward to seed
    streamline_points.InsertNextPoint(point) #skipping the seed point here and including in forward points

for i in range(forward_points.GetNumberOfPoints()):
    point = [forward_points.GetPoint(i)[j] for j in range(3)] #going from seed to the most forward
    streamline_points.InsertNextPoint(point)

# print(forward_points.GetNumberOfPoints(), backward_points.GetNumberOfPoints())

# x =[]

# for i in range(streamline_points.GetNumberOfPoints()):
#     x.append(streamline_points.GetPoint(i))

# with open('t1.txt','w') as f:
#     for item in x:
#         for its in item:
#             f.write(str(its))
#             f.write(' ')
#         f.write('\n')


def render_data(points):
    # Create a vtkPolyData object
    pdata = vtk.vtkPolyData()
    pdata.SetPoints(points)
    
    # Create a vtkPolyLine to represent the streamline trajectory
    pline = vtk.vtkCellArray()
    pline.InsertNextCell(points.GetNumberOfPoints())
    for i in range(points.GetNumberOfPoints()):
        pline.InsertCellPoint(i)
    pdata.SetLines(pline)
    
    # Create a vtkPolyDataMapper
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(pdata)
    
    # Create a vtkActor
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(1.0, 0.0, 0.0)  # Set color to red
    
    # Create a vtkRenderer
    renderer = vtk.vtkRenderer()
    renderer.AddActor(actor)
    renderer.SetBackground(1.0, 1.0, 1.0)  # Set background to white
    
    # Create a vtkRenderWindow
    render_window = vtk.vtkRenderWindow()
    render_window.AddRenderer(renderer)
    
    # Create a vtkRenderWindowInteractor
    render_window_interactor = vtk.vtkRenderWindowInteractor()
    render_window_interactor.SetRenderWindow(render_window)
    
    # Write the files to a vtp file
    writer = vtk.vtkXMLPolyDataWriter()
    writer.SetFileName("seed_at_"+str(seed_point[0])+"_"+str(seed_point[1])+"_"+str(seed_point[2])+".vtp")
    writer.SetInputData(pdata)
    writer.Write()

    # Initialize the interactor and start the rendering loop
    render_window.Render()
    render_window_interactor.Start()

render_data(streamline_points)

print(streamline_points.GetNumberOfPoints())
