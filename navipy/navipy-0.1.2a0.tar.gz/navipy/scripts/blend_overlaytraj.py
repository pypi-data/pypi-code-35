"""
 Overlay a trajectory in a blender environment
"""
import sys
import argparse
import os
import inspect
import pkg_resources
import tempfile
# Following need to be imported in blender as well
from navipy.trajectories import Trajectory
from navipy.maths.homogeneous_transformations import compose_matrix
from navipy.maths.quaternion import matrix as quatmatrix


importwithinblender = [
    'from navipy.trajectories import Trajectory',
    'from navipy.maths.homogeneous_transformations import compose_matrix',
    'from navipy.maths.quaternion import matrix as quatmatrix']


def parser_blend_overlaytraj():
    # Create command line options
    parser = argparse.ArgumentParser()
    arghelp = 'Path to the environment (.blend) in which your agent lives'
    defaultworld = pkg_resources.resource_filename(
        'navipy', 'resources/sample_experiment/Ravi_2018/corridor.blend')
    defaulttraj = pkg_resources.resource_filename(
        'navipy', 'resources/sample_experiment/Ravi_2018/corridor_traj.csv')
    parser.add_argument('--blender-world',
                        type=str,
                        default=defaultworld,
                        help=arghelp)
    arghelp = 'File containing the trajectory'
    parser.add_argument('--trajectory',
                        type=str,
                        default=defaulttraj,
                        help=arghelp)
    arghelp = 'Command to run blender\n'
    arghelp += 'If not provided, the script will try to find the command'
    arghelp += " by using: shutil.which('blender')"
    parser.add_argument('--blender-command',
                        type=str,
                        default=None,
                        help=arghelp)
    arghelp = 'To display some stuff \n'
    arghelp += ' * -v print command \n'
    arghelp += ' * -vv print also script'
    parser.add_argument('-v', '--verbose',
                        action='count',
                        default=0,
                        help=arghelp)

    return parser


def run(trajfile):
    import bpy
    # Load trajectory
    trajectory = Trajectory().read_csv(trajfile)
    # create the Curve Datablock
    curveData = bpy.data.curves.new('myCurve', type='CURVE')
    curveData.dimensions = '3D'
    curveData.resolution_u = 2
    # map coords to spline
    polyline = curveData.splines.new('POLY')
    polyline.points.add(trajectory.shape[0] - 1)
    i = 0
    for _, coord in trajectory.iterrows():
        polyline.points[i].co = (coord.loc[('location', 'x')],
                                 coord.loc[('location', 'y')],
                                 coord.loc[('location', 'z')],
                                 1)
        i += 1

    # create Object
    curveOB = bpy.data.objects.new('my_trajectory', curveData)
    # attach to scene and validate context
    scn = bpy.context.scene
    scn.objects.link(curveOB)
    scn.objects.active = curveOB
    curveOB.select = True
    # bpy.ops.curve.primitive_nurbs_circle_add(
    #    radius=1, view_align=False, enter_editmode=False, location=(0, 0, 0))
    # bpy.context.object.data.resolution_u = 3
    # bpy.context.object.data.bevel_object = bpy.data.objects["NurbsCircle"]

    # add frame
    bpy.ops.object.empty_add(type='ARROWS',
                             radius=1,
                             view_align=False,
                             location=(0, 0, 0),
                             layers=(True, False, False, False, False,
                                     False, False, False, False, False,
                                     False, False, False, False, False,
                                     False, False, False, False, False))
    frameobject = bpy.context.object
    frameobject.name = "camera_frame"
    # find camera:
    # to then move it on each frame
    camera_found = False
    for obj in bpy.context.scene.objects:
        if obj.type == 'CAMERA':
            camera = obj
            camera_found = True
            break
    if not camera_found:
        raise NameError('The blender file does not contain a camera')
    # Remove animation to be able to move the camera
    # and add animation
    camera.animation_data_clear()
    # set first and last frame
    context = bpy.context
    context.scene.frame_start = trajectory.index.min()
    context.scene.frame_end = trajectory.index.max()
    keyInterp = context.user_preferences.edit.keyframe_new_interpolation_type
    context.user_preferences.edit.keyframe_new_interpolation_type = 'LINEAR'
    convention = trajectory.rotation_mode
    _renderaxis = '+x'
    for frame_i, posorient in trajectory.iterrows():
        context.scene.frame_current = frame_i
        # Render
        rotmat = compose_matrix(
            angles=posorient.loc[convention],
            translate=posorient.loc['location'],
            axes=convention)
        frameobject.matrix_world = rotmat.transpose()
        if _renderaxis == '+x':
            initrot = quatmatrix([0.5, -0.5, 0.5, 0.5])
            # The camera is aligned in -z
            # A rotation along z wll thus roll the camera
            # Althougth the camera should yaw in such case
            rotmat[:3, :3] = rotmat[:3, :3].dot(initrot[:3, :3])
        # matrix_world in blender are column-major order
        # and numpy row-major order
        camera.matrix_world = rotmat.transpose()
        camera.keyframe_insert(data_path='location', frame=(frame_i))
        camera.keyframe_insert(data_path='rotation_euler', frame=(frame_i))
        frameobject.keyframe_insert(data_path='location', frame=(frame_i))
        frameobject.keyframe_insert(
            data_path='rotation_euler', frame=(frame_i))
    context.user_preferences.edit.keyframe_new_interpolation_type = keyInterp


def main():
    # encoding for temporary file
    encoding = 'utf-8'

    # Fetch arguments
    args = parser_blend_overlaytraj().parse_args()
    # Create tempfile with testing code and then call blendnavipy
    header = '# Generated by {}\n'.format(sys.argv[0])
    with tempfile.NamedTemporaryFile() as tfile:
        # Start of file
        tfile.write(header.encode(encoding))
        for line in importwithinblender:
            tfile.write(line.encode(encoding))
            tfile.write('\n'.encode(encoding))
        for line in inspect.getsourcelines(run)[0]:
            tfile.write(line.encode(encoding))
        tfile.write('\n\n'.encode(encoding))
        tfile.write('try:\n'.encode(encoding))
        tfile.write('     run("{}")\n'.format(
            args.trajectory).encode(encoding))
        tfile.write('except Exception:\n'.encode(encoding))
        tfile.write('     sys.exit(1)\n'.encode(encoding))
        tfile.seek(0)

        command = 'blendnavipy --blender-world {} --python-script {}'
        command = command.format(args.blender_world, tfile.name)
        if args.blender_command is not None:
            command += ' --blender-command {}'.format(args.blender_command)
        for _ in range(args.verbose):
            command += ' -v'
        os.system(command)


if __name__ == "__main__":
    # execute only if run as a script
    main()
