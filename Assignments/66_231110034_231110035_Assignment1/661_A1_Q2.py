from vtk import *
PhongShading = input("Use phong shading (Yes/No):")

## Importing Data file
reader = vtkXMLImageDataReader()
reader.SetFileName('Data/Isabel_3D.vti')
reader.Update()
data = reader.GetOutput()

#Colour transfer function
ctf = vtkColorTransferFunction()
ctf.AddRGBPoint(-4931.54,0,1,1)      
ctf.AddRGBPoint(-2508.95,0,0,1)      
ctf.AddRGBPoint(-1873.9,0,0,0.5)     
ctf.AddRGBPoint(-1027.16,1,0,0)      
ctf.AddRGBPoint(-298.031,1,0.4,0)    
ctf.AddRGBPoint(2594.97,1,1,0)

# Opacity Transfer Function
otf = vtkPiecewiseFunction()
otf.AddPoint(-4931.54,1.0)
otf.AddPoint(101.815,0.002)
otf.AddPoint(2594.97,0.0)

# vtkSmartVolumeMapper()
volumeMapper = vtkSmartVolumeMapper()
volumeMapper.SetInputData(data)

# vtkVolumeProperty
volumeProperty = vtkVolumeProperty()
volumeProperty.SetColor(ctf)
volumeProperty.SetScalarOpacity(otf)

# Phong Shading
if PhongShading == 'Yes':
    volumeProperty.ShadeOn()
    volumeProperty.SetAmbient(0.5)
    volumeProperty.SetDiffuse(0.5)
    volumeProperty.SetSpecular(0.5)

# vtkVolume
volume = vtkVolume()
volume.SetMapper(volumeMapper)
volume.SetProperty(volumeProperty)

# vtkOutlineFilter
outlineFilter = vtkOutlineFilter()
outlineFilter.SetInputData(data)

# vtkPolyDataMapper
outlineMapper = vtkPolyDataMapper()
outlineMapper.SetInputConnection(outlineFilter.GetOutputPort()) #?

# vtkActor
outlineActor = vtkActor()
outlineActor.SetMapper(outlineMapper)
outlineActor.GetProperty().SetColor(0,0,0) 

# Setup render window, renderer, and interactor
renderer = vtkRenderer()
renderer.SetBackground(1,1,1)
renderWindow = vtkRenderWindow()
renderWindow.SetSize(1000,1000)
renderWindow.AddRenderer(renderer)
renderWindowInteractor = vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)

# Add the volume and outline to the renderer
renderer.AddVolume(volume)
renderer.AddActor(outlineActor)

### Finally render the object
renderWindow.Render()
renderWindowInteractor.Start()

