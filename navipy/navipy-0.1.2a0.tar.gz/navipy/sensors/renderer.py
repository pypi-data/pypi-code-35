"""
Renderer
"""
import warnings
try:
    import bpy
except ImportError:  # noqa F821
    warnings.warn(
        'bpy could not be imported, ' +
        'please run your python program in blender')
import numpy as np
import tempfile
import os
import pandas as pd
import yaml  # Used to load config files
import pkg_resources
from navipy.maths.homogeneous_transformations import compose_matrix
from navipy.maths.quaternion import matrix as quatmatrix
from navipy.scene import spherical_indeces
from navipy.maths import constants
from navipy.trajectories import Trajectory
from PIL import Image
from navipy.scene import check_scene
from navipy.database import DataBase
import logging


class AbstractRender():
    """
    List method to render on a grid or along a trajectory
    """

    def __init__(self):
        self._logger = logging.getLogger('navipy')
        self.__worldlimit = np.inf

    @property
    def worldlimit(self):
        """ worldlimit is the max distance return in scene

        :getter: return a worldlimit
        :setter: set a worldlimit
        :type: list
        """
        return self.__worldlimit

    @worldlimit.setter
    def worldlimit(self, worldlimit):
        """ worldlimit"""
        self.__worldlimit = worldlimit

    @property
    def viewing_directions(self):
        """ Need to be implemented by children classes """
        return None

    def render_trajectory(self, outputfile,
                          trajectory, imformat='.jpg'):
        """
        Render on a trajectory
        """
        # Check the user input
        if not isinstance(outputfile, str):
            msg = 'OutputFile should be a path {}'.format(outputfile)
            self._logger.exception(msg)
            raise TypeError(msg)
        if not isinstance(trajectory, Trajectory):
            msg = 'trajectory should be {}'.format(Trajectory)
            msg += 'and not {}'.format(type(trajectory))
            self._logger.exception(msg)
            raise TypeError(msg)
        # Create the directory name if it does
        # not exist
        self._logger.debug('render output:{}'.format(outputfile))
        dirname = os.path.dirname(outputfile)
        # Todo empty dirname
        if not os.path.isdir(dirname):
            os.makedirs(dirname)
        # Check the file type
        if os.path.isdir(outputfile):
            mode = 'array'
            nbdigit = np.floor(np.log10(trajectory.shape[0])) + 1
            fileformat = os.path.join(
                outputfile,
                'frame_{:0' + str(nbdigit) + 'd}' + imformat)
        else:
            mode = 'database'
            self._logger.debug('render outputmode:{}'.format(mode))
            dataloger = DataBase(outputfile,
                                 mode='a',
                                 channels=['R', 'G', 'B', 'D'],
                                 arr_dtype=np.uint8)
            self._logger.debug('database created')
            dataloger.viewing_directions = self.viewing_directions
        # We now can render
        self._logger.info('Start rendering')
        for frame_i, posorient in trajectory.iterrows():
            # Check if posorient is a valid one
            # otherwise skip to next position
            if np.any(np.isnan(posorient)):
                # Skip because we can not render when nans
                self._logger.info('Skip nan frame_i : {}'.format(frame_i))
                continue
            # Avoid rerendering by checking if data already
            # exist
            if mode == 'database':
                self._logger.warning(posorient)
                rowid = dataloger.get_posid(posorient)
                if dataloger.check_data_validity(rowid):
                    msg = 'frame_i: {} data is valid rowid {}'
                    msg = msg.format(frame_i, rowid)
                    self._logger.warning(msg)
                    continue
            elif mode == 'array':
                filename = fileformat.format(frame_i)
                if os.path.exists(filename):
                    msg = 'frame_i: {} already exist'
                    msg = msg.format(frame_i)
                    self._logger.warning(msg)
                    continue
            # The position-orientatios is valid (none nan)
            # and the cmaxminrange has not already been assigned
            # so the image need to be rendered
            self._logger.info('Update frame_i : {}'.format(frame_i))
            scene = self.scene(posorient)
            check_scene(scene)
            scene = scene[..., 0]
            distance = scene[..., -1]
            distance[distance > self.worldlimit] = self.worldlimit
            scene[..., -1] = distance
            if mode == 'database':
                self._logger.info('Write image')
                dataloger.write_image(posorient, scene)
            elif mode == 'array':
                if imformat == '.npy':
                    np.save(filename, scene)
                else:
                    result = Image.fromarray(
                        (scene * 255).astype(np.uint8))
                    result.save(filename)

    def render_ongrid(self, outputfile,
                      x, y, z,
                      alpha_0=[0], alpha_1=[0], alpha_2=[0],
                      q_0=None, q_1=None, q_2=None, q_3=None,
                      rotconv='zyx'):
        # Check inputs
        if rotconv == 'quaternion':
            if (q_0 is None) or \
               (q_1 is None) or \
               (q_2 is None) or \
               (q_3 is None):
                msg = 'With rotconv {}, q_0,q_1,q_2,q_3 can not be None'
                msg = msg.format(rotconv)
                raise ValueError(msg)
        if not (isinstance(x, np.ndarray) or isinstance(x, list)):
            raise TypeError('x must be list or np.array')
        if not (isinstance(y, np.ndarray) or isinstance(y, list)):
            raise TypeError('y must be list or np.array')
        if not (isinstance(z, np.ndarray) or isinstance(z, list)):
            raise TypeError('z must be list or np.array')
        if rotconv == 'quaternion':
            if not (isinstance(q_0, np.ndarray) or
                    isinstance(q_0, list)):
                raise TypeError('q_0 must be list or np.array')
            if not (isinstance(q_1, np.ndarray) or
                    isinstance(q_1, list)):
                raise TypeError('q_1 must be list or np.array')
            if not (isinstance(q_2, np.ndarray) or
                    isinstance(q_2, list)):
                raise TypeError('q_3 must be list or np.array')
            if not (isinstance(q_3, np.ndarray) or
                    isinstance(q_3, list)):
                raise TypeError('q_3 must be list or np.array')
        else:
            if not (isinstance(alpha_0, np.ndarray) or
                    isinstance(alpha_0, list)):
                raise TypeError('alpha_0 must be list or np.array')
            if not (isinstance(alpha_1, np.ndarray) or
                    isinstance(alpha_1, list)):
                raise TypeError('alpha_1 must be list or np.array')
            if not (isinstance(alpha_2, np.ndarray) or
                    isinstance(alpha_2, list)):
                raise TypeError('alpha_2 must be list or np.array')
        # We create data on a grid.
        # To then render it as a trajectory
        if rotconv == 'quaternion':
            [mx, my, mz, mq0, mq1, mq2, mq3] = \
                np.meshgrid(x, y, z, q_0, q_1, q_2, q_3)

            mx = mx.flatten()
            grid_point = Trajectory(rotconv,
                                    indeces=range(0, mx.shape[0]))
            grid_point.x = mx
            grid_point.y = my.flatten()
            grid_point.z = mz.flatten()
            grid_point.q0 = mq0.flatten()
            grid_point.q1 = mq1.flatten()
            grid_point.q2 = mq2.flatten()
            grid_point.q3 = mq3.flatten()

        else:
            [mx, my, mz, ma0, ma1, ma2] = \
                np.meshgrid(x, y, z, alpha_0, alpha_1, alpha_2)

            mx = mx.flatten()
            grid_point = Trajectory(rotconv,
                                    indeces=range(0, mx.shape[0]))
            grid_point.x = mx
            grid_point.y = my.flatten()
            grid_point.z = mz.flatten()
            grid_point.alpha_0 = ma0.flatten()
            grid_point.alpha_1 = ma1.flatten()
            grid_point.alpha_2 = ma2.flatten()
        #
        self.render_trajectory(outputfile, grid_point)


class BlenderRender(AbstractRender):
    """
    BlenderRender is a small class binding python with blender.
    With BlenderRender one can move the bee to a position, and render what
    the bee see at this position.

    The Bee eye is a panoramic camera with equirectangular projection
    The light rays attaining the eyes are filtered with a gaussian.

    """

    def __init__(self):
        """Initialise the Cyberbee
        ..todo check that TemporaryDirectory is writtable and readable
        """
        super(BlenderRender, self).__init__()
        self._renderaxis = '+x'
        # Rendering engine needs to be Cycles to support panoramic
        # equirectangular camera
        bpy.context.scene.render.engine = 'CYCLES'
        # To get the distances we need to pass the z-buffer
        bpy.context.scene.render.layers["RenderLayer"].use_pass_z = True
        # Look for object camera
        camera_found = False
        for obj in bpy.context.scene.objects:
            if obj.type == 'CAMERA':
                self.camera = obj
                camera_found = True
                break
        assert camera_found, 'The blender file does not contain a camera'
        # Remove animation to be able to move the camera
        # and add animation
        self.camera.animation_data_clear()
        # The bee eye is panoramic, and with equirectangular projection
        self.camera.data.type = 'PANO'
        self.camera.data.cycles.panorama_type = 'EQUIRECTANGULAR'
        # switch on nodes
        # Create render link to OutputFile with Image and Z buffer
        # so that we can read the image from somewhere.
        # This is a hack, because we did not manage to
        # directly blender buffer...
        bpy.context.scene.use_nodes = True
        scene = bpy.context.scene
        nodes = scene.node_tree.nodes

        render_layers = nodes['Render Layers']
        output_file = nodes.new("CompositorNodeOutputFile")
        output_file.format.file_format = "OPEN_EXR"
        output_file.file_slots.remove(output_file.inputs[0])
        tmp_fileoutput = dict()
        tmp_fileoutput['Image'] = 'Image'
        tmp_fileoutput['Depth'] = 'Depth'
        tmp_fileoutput['Folder'] = tempfile.TemporaryDirectory().name
        tmp_fileoutput['ext'] = '.exr'
        output_file.file_slots.new(tmp_fileoutput['Image'])
        output_file.file_slots.new(tmp_fileoutput['Depth'])
        output_file.base_path = tmp_fileoutput['Folder']
        scene.node_tree.links.new(
            render_layers.outputs['Image'],
            output_file.inputs['Image']
        )
        # Z buffer has been renamed in Depth in newer versionW
        if bpy.app.version < (2, 79, 0):
            scene.node_tree.links.new(
                render_layers.outputs['Z'],
                output_file.inputs['Depth']
            )
        else:
            scene.node_tree.links.new(
                render_layers.outputs['Depth'],
                output_file.inputs['Depth']
            )
        self.tmp_fileoutput = tmp_fileoutput

        # Filtering props
        bpy.context.scene.cycles.filter_type = 'GAUSSIAN'
        self.config_file = pkg_resources.resource_filename(
            'navipy', 'resources/configs/BlenderRender.yaml')

    @property
    def config_file(self):
        return self.__config_file

    @config_file.setter
    def config_file(self, config_file):
        if not isinstance(config_file, str):
            raise TypeError('Config file should be a file path')
        self._logger.debug('Open config file {}'.format(config_file))
        try:
            with open(config_file, 'r') as stream:
                try:
                    config = yaml.load(stream)
                except yaml.YAMLError as exc:
                    print(exc)
        except IOError:
            msg = "The file could not be read"
            self._logger.exception(msg)
            raise IOError(msg)
        if 'BlenderRender' not in config.keys():
            msg = "The file could not be read"
            self._logger.exception(msg)
            raise KeyError(msg)
        self._logger.debug('Access BlenderRender')
        blendconfig = config['BlenderRender']
        # Loading the field of view in the camera
        if 'fov' in blendconfig.keys():
            fov = np.zeros((2, 2))
            if 'elevation' in blendconfig['fov'].keys():
                fov[0, 0] = min(blendconfig['fov']['elevation'])
                fov[0, 1] = max(blendconfig['fov']['elevation'])
            else:
                raise KeyError(
                    'Yaml config file should contain fov/elevation key')
            if 'azimuth' in blendconfig['fov'].keys():
                fov[1, 0] = min(blendconfig['fov']['azimuth'])
                fov[1, 1] = max(blendconfig['fov']['azimuth'])
            else:
                raise KeyError(
                    'Yaml config file should contain fov/azimuth key')
            self.camera_fov = fov
        else:
            raise KeyError('Yaml config file should contain fov')
        # Loading the resolution ie number of pixel of the camera
        if 'resolution' in blendconfig.keys():
            self.camera_resolution = blendconfig['resolution']
        else:
            raise KeyError('Yaml config file should contain resolution')
        # Load the filter of rendering
        if 'gaussian_width' in blendconfig.keys():
            self.camera_gaussian_width = blendconfig['gaussian_width']
        else:
            raise KeyError(
                'Yaml config file should contain gaussian_width')
        # Load cycle for rendering
        if 'samples' in blendconfig.keys():
            self.camera_samples = blendconfig['samples']
        else:
            raise KeyError(
                'Yaml config file should contain samples')
        # Load worldlimit
        if 'worldlimit' in blendconfig.keys():
            self.worldlimit = blendconfig['worldlimit']
        self.__config_file = config_file
        self._logger.debug('END: BlendRender configured')

    @property
    def cycle_samples(self):
        """get the samples for rendering with cycle

        : returns: the number of samples used for the rendering
        : rtype: int

        """
        return bpy.context.scene.cycles.samples

    @cycle_samples.setter
    def cycle_samples(self, samples=30):
        """change the samples for rendering with cycle

        : param samples: the number of samples to use when rendering images
        : type samples: int

        """
        if not isinstance(samples, int):
            raise TypeError('samples must be an integer')
        bpy.context.scene.cycles.samples = samples

    @property
    def camera_fov(self):
        """get fov of camera

        : returns: the field of view of the camera as \
        [[minimum latitude, maximum latitude],
                            [minimum longitude, maximum longitude]]
                            (in deg)
        : rtype: np.array

        ..todo Change assert to if -> raise TypeError/KeyError

        """
        if not self.camera.data.type == 'PANO':
            raise TypeError('Camera is not panoramic')
        if not self.camera.data.cycles.panorama_type == 'EQUIRECTANGULAR':
            raise TypeError('The panoramic camera is not equirectangular')
        fov = np.zeros((2, 2))
        fov[0, 0] = np.rad2deg(self.camera.data.cycles.latitude_min)
        fov[0, 1] = np.rad2deg(self.camera.data.cycles.latitude_max)
        fov[1, 0] = np.rad2deg(self.camera.data.cycles.longitude_min)
        fov[1, 1] = np.rad2deg(self.camera.data.cycles.longitude_max)
        return fov

    @camera_fov.setter
    def camera_fov(self, resolution):
        """change the field of view of the panoramic camera

        : param resolution: [[minimum latitude, maximum latitude],
                            [minimum longitude, maximum longitude]]
                            (in deg)
        : type latmin: 2x2 float array or list
        """
        if not (isinstance(resolution, tuple) or
                isinstance(resolution, list) or
                isinstance(resolution, np.ndarray)):
            raise TypeError('resolution must be list,  array, or tuple')
        if not self.camera.data.type == 'PANO':
            raise TypeError('Camera is not panoramic')
        if not self.camera.data.cycles.panorama_type == 'EQUIRECTANGULAR':
            raise TypeError('Camera is not equirectangular')
        self.camera.data.cycles.latitude_min = np.deg2rad(
            resolution[0][0])
        self.camera.data.cycles.latitude_max = np.deg2rad(
            resolution[0][1])
        self.camera.data.cycles.longitude_min = np.deg2rad(
            resolution[1][0])
        self.camera.data.cycles.longitude_max = np.deg2rad(
            resolution[1][1])

    @property
    def camera_gaussian_width(self):
        """get width of the gaussian spatial filter

        : returns: the width of the gaussian filter
        : rtype: float

        """
        return bpy.context.scene.cycles.filter_width

    @camera_gaussian_width.setter
    def camera_gaussian_width(self, gauss_w):
        """change width of the gaussian spatial filter

        : param gauss_w: width of the gaussian filter
        : type gauss_w: float

        """
        if not (isinstance(gauss_w, int) or isinstance(gauss_w, float)):
            raise TypeError('gauss window must be integer or float')
        bpy.context.scene.cycles.filter_width = gauss_w

    @property
    def camera_resolution(self):
        """return camera resolution(x, y)

        : returns: the resolution of the camera along(x-axis, y-axis)
        : rtype: (int, int)

        """
        resolution_x = bpy.context.scene.render.resolution_x
        resolution_y = bpy.context.scene.render.resolution_y
        return resolution_x, resolution_y

    @camera_resolution.setter
    def camera_resolution(self, resolution):
        """change the camera resolution(nb of pixels)

        : param resolution_x: number of pixels along the x-axis of the camera
        : type resolution_x: int
        : param resolution_y: number of pixels along the y-axis of the camera
        : type resolution_y: int
        """
        if not (isinstance(resolution, list) or
                isinstance(resolution, np.ndarray)):
            raise TypeError('resolution list or array')
        bpy.context.scene.render.resolution_x = resolution[0]
        bpy.context.scene.render.resolution_y = resolution[1]
        bpy.context.scene.render.resolution_percentage = 100

    @property
    def viewing_directions(self):
        self._logger.info('get viewdir')
        rx, ry = self.camera_resolution
        fov = self.camera_fov
        az = np.linspace(fov[1, 0], fov[1, 1], rx)
        el = np.linspace(fov[0, 0], fov[0, 1], ry)
        [ma, me] = np.meshgrid(az, el)
        view_dir = np.zeros((ma.shape[0], ma.shape[1], 2))
        view_dir[..., spherical_indeces()['elevation']] = me
        view_dir[..., spherical_indeces()['azimuth']] = ma
        return view_dir

    @property
    def image(self):
        """return the last rendered image as a numpy array

        : returns: the image(height, width, nchannel)
        : rtype: a double numpy array

        .. note: A temporary file will be written on the harddrive,
                 due to API blender limitation
        """
        self._logger.info('get image')
        # save image as a temporary file, and then loaded
        # sadly the rendered image pixels can not directly be access
        keyframe = bpy.context.scene.frame_current
        filename = os.path.join(self.tmp_fileoutput['Folder'],
                                self.tmp_fileoutput['Image'] +
                                '{:04d}'.format(keyframe) +
                                self.tmp_fileoutput['ext'])
        im_width, im_height = self.camera_resolution
        im = bpy.data.images.load(filename)
        pixels = np.array(im.pixels).copy()
        pixels = pixels.reshape([im_height, im_width, -1])
        # The last channel is the alpha channel
        pixels = pixels[..., :(pixels.shape[2] - 1)]
        self._logger.debug('Image -> Ok')
        # remote image once we read it. To avoid storing all images
        self._logger.debug('Delete file {}'.format(filename))
        os.remove(filename)
        return pixels

    @property
    def distance(self):
        """return the last rendered distance map as a numpy array

        : returns: the distance map(height, width)
        : rtype: a double numpy array

        .. note: A temporary file will be written on the harddrive,
                 due to API blender limitation

        .. todo: use @property
                     def distance(self)
        """
        self._logger.info('get distances')
        # save image as a temporary file, and then loaded
        # sadly the rendered image pixels can not directly be access
        keyframe = bpy.context.scene.frame_current
        filename = os.path.join(self.tmp_fileoutput['Folder'],
                                self.tmp_fileoutput['Depth'] +
                                '{:04d}'.format(keyframe) +
                                self.tmp_fileoutput['ext'])
        im_width, im_height = self.camera_resolution
        im = bpy.data.images.load(filename)
        distance = np.array(im.pixels).copy()
        self._logger.debug('Reshape {}->{}'.format(
            distance.shape, self.camera_resolution))
        distance = distance.reshape([im_height, im_width, -1])
        # Distance are channel independent
        distance = distance[:, :, 0]
        self._logger.debug('Distance -> Ok')
        # remote image once we read it. To avoid storing all images
        self._logger.debug('Delete file {}'.format(filename))
        os.remove(filename)
        return distance[..., np.newaxis]

    def update(self, posorient):
        """assign the position and the orientation of the camera.

        : param posorient: is a 1x6 vector containing:
             *in case of euler angeles the index should be
              ['location']['x']
              ['location']['y']
              ['location']['z']
              [convention][alpha_0]
              [convention][alpha_1]
              [convention][alpha_2]
             **where convention can be:
               xyz, xzy, yxz, yzx, zyx, zxy
             *in case of quaternions the index should be
              ['location']['x']
              ['location']['y']
              ['location']['z']
              [convention]['q_0']
              [convention]['q_1']
              [convention]['q_2']
              [convention]['q_3']
             **where convention can be:
               quaternion
             here the angles are euler rotation around the axis
             specified by scene.camera.rotation_mode
        : type posorient: pandas Series with multi-index
        """
        self._logger.info('update posorient to {}'.format(posorient))
        if isinstance(posorient, pd.Series):
            # set frame
            cframe = int(posorient.name)
            if cframe > bpy.context.scene.frame_end:
                bpy.context.scene.frame_end = cframe
            if cframe < bpy.context.scene.frame_start:
                bpy.context.scene.frame_start = cframe
            bpy.context.scene.frame_current = cframe
            # set roation mode
            conv_found = False
            index = posorient.index
            convention = index.get_level_values(0)[-1]
            for key, _ in constants._AXES2TUPLE.items():
                if convention == key:
                    conv_found = True
                    break
            if convention == 'quaternion':
                conv_found = True
            if not conv_found:
                msg = 'The convention {} used for the orientation'
                msg = msg.format(convention)
                msg += ' is not supported'
                raise ValueError(msg)
        else:
            raise TypeError(
                'posorient must be of type array, list, or pandas Series')
        # Render
        rotmat = compose_matrix(
            angles=posorient.loc[convention],
            translate=posorient.loc['location'],
            axes=convention)
        if self._renderaxis == '+x':
            initrot = quatmatrix([0.5, -0.5, 0.5, 0.5])
            # The camera is aligned in -z
            # A rotation along z wll thus roll the camera
            # Althougth the camera should yaw in such case
            rotmat[:3, :3] = rotmat[:3, :3].dot(initrot[:3, :3])
        # matrix_world in blender are column-major order
        # and numpy row-major order
        self.camera.matrix_world = np.transpose(rotmat)
        bpy.ops.render.render()

    def scene(self, posorient):
        """ update position orientation and return a RGBD image

        : param posorient: is a 1x6 vector containing:
             x, y, z, angle_1, angle_2, angle_3,
             here the angles are euler rotation around the axis
             specified by scene.camera.rotation_mode
        : type posorient: 1x6 double array
        : returns: a(height, width, channel) array here the last channel \
is the distance.
        : rtype: a double numpy array
        """
        self._logger.info('get a scene')
        self.update(posorient)
        toreturn = np.concatenate((self.image,
                                   self.distance), axis=2)
        ninffound = 0
        for chan_i in range(4):
            cim = toreturn[..., chan_i]
            cmax = cim.max()
            if np.isinf(cmax):
                ninffound += np.sum(np.isinf(cim))
                cmax = cim[np.isinf(cim) == 0].max()
                toreturn[np.isinf(cim) == 1] = cmax
        if ninffound > 0:
            warnings.warn('{} Inf found in image'.format(ninffound))
        self._logger.info('Scene -> Ok')
        return toreturn[..., np.newaxis]
