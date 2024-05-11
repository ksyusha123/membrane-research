import pathlib
import json
import numpy as np
import vtk


def create_folder(folder_name: str) -> pathlib.Path:
    folder_path = pathlib.Path(folder_name)
    folder_path.mkdir(exist_ok=True)
    return folder_path


def save_distance_as_json(distance_info, filename, folder_name):
    create_folder(folder_name)

    filepath = pathlib.Path(folder_name) / pathlib.Path(filename)

    if not filepath.is_file():
        current = {'experiments': []}
    else:
        with open(filepath) as f:
            current_str = f.read()
            current = json.loads(current_str)
    
    current['experiments'].append(distance_info)

    with open(filepath, 'w') as f:
        f.write(json.dumps(current, indent=2))


def write_vtk_file(system, filename, folder, step_number, radiuses_by_type, bonds=[]):
    filename = f'{filename}.step.{step_number}.vtk'
    point_num = len(system.part.all())
    part_idx = list(np.arange(point_num))

    ugrid_l = vtk.vtkUnstructuredGrid()

    # Points
    points = vtk.vtkPoints()
    for i in part_idx:
        px, py, pz = system.part.by_id(i).pos_folded
        points.InsertNextPoint(px, py, pz)

    ugrid_l.SetPoints(points)

    # Dipoles
    moments = vtk.vtkFloatArray()
    moments.SetNumberOfComponents(3)
    moments.SetName('mag_moments')
    for i in part_idx:
        dip = system.part.by_id(i).dip
        dip_norm = dip
        if dip.all():
            dip_norm = dip / np.linalg.norm(dip)
        mx, my, mz = dip_norm[0], dip_norm[1], dip_norm[2]
        moments.InsertNextTuple3(mx, my, mz)

    ugrid_l.GetPointData().SetVectors(moments)

    # Bonds
    if bonds:
        cellArray_l = vtk.vtkCellArray()
        for pair in bonds:
            line_vtk = vtk.vtkLine()
            line_vtk.GetPointIds().SetId(0, part_idx.index(pair[0]))
            line_vtk.GetPointIds().SetId(1, part_idx.index(pair[1]))
            cellArray_l.InsertNextCell(line_vtk)
        ugrid_l.SetCells(vtk.VTK_LINE, cellArray_l)

    # Clusters
    mask = vtk.vtkFloatArray()
    mask.SetNumberOfComponents(1)
    mask.SetName('cluster_num')
    for i in range(point_num):
        mask.InsertNextValue(system.part.by_id(i).type)
    ugrid_l.GetPointData().AddArray(mask)

    
    # Radiuses
    radiuses = vtk.vtkFloatArray()
    radiuses.SetNumberOfComponents(1)
    radiuses.SetName('radius')
    for i in range(point_num):
        radiuses.InsertNextValue(radiuses_by_type[system.part.by_id(i).type])
    ugrid_l.GetPointData().AddArray(radiuses)

    # Particle number
    mask_num = vtk.vtkFloatArray()
    mask_num.SetNumberOfComponents(1)
    mask_num.SetName('particle_num')
    for i in part_idx:
        mask_num.InsertNextValue(i)
    ugrid_l.GetPointData().AddArray(mask_num)

    create_folder(folder)
    filepath = pathlib.Path(folder) / pathlib.Path(filename)
    writer = vtk.vtkUnstructuredGridWriter()
    writer.SetFileName(filepath)
    writer.SetInputData(ugrid_l)
    writer.Write()
