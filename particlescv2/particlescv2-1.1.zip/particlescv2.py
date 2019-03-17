# particles.py
from __future__ import print_function
from builtins import next
from math import sqrt, pow
from blist import blist
import cv2, math, random, sys
import numpy as np

DRAWTYPE_POINT = 0
DRAWTYPE_CIRCLE = 1
DRAWTYPE_LINE = 2
DRAWTYPE_SCALELINE = 3
DRAWTYPE_BUBBLE = 4
DRAWTYPE_IMAGE = 5
UNIVERSAL_CONSTANT_OF_MAKE_GRAVITY_LESS_STUPIDLY_SMALL = 1000.0 
MAXDIST = 20.0

# Interpolation type constants
INTERPOLATIONTYPE_LINEAR = 200
INTERPOLATIONTYPE_COSINE = 201

# Gravity constants
UNIVERSAL_CONSTANT_OF_MAKE_GRAVITY_LESS_STUPIDLY_SMALL = 1000.0  # Well, Newton got one to make it less stupidly large.
VORTEX_ACCELERATION = 0.01  # A tiny value added to the centripetal force exerted by vortex gravities to draw in particles
VORTEX_SWALLOWDIST = 20.0  # Particles closer than this will be swallowed up and regurgitated in the bit bucket

# Fraction of radius which can go inside an object
RADIUS_PERMITTIVITY = 0.3

def LinearInterpolate(val1, val2, t):
    diff = val2 - val1
    dist = float(diff) * t
    return val1 + dist

def CosineInterpolate(val1, val2, t, clockwise=1):
    amplitude = float(val2 - val1) / 2.0
    midpoint = float(val1 + val2) / 2.0
    # clockwise = 1 means clockwise
    # clockwise = -1 means anti-clockwise
    return (clockwise*amplitude * math.cos(math.pi * (1.0 - t))) + midpoint

def LinearInterpolateKeyframes(curframe, key1, key2, val1, val2):
    if key1 == key2:
        return val2
    factor = float(curframe - key1) / float(key2 - key1)
    return LinearInterpolate(val1, val2, factor)

def CosineInterpolateKeyframes(curframe, key1, key2, val1, val2):
    if key1 == key2:
        return val2
    factor = float(curframe - key1) / float(key2 - key1)
    return CosineInterpolate(val1, val2, factor)

def InterpolateKeyframes(curframe, variables, keyframes):
    if keyframes is None: return None
    if len(keyframes) == 1:
        return keyframes[0].variables
    finalvariables = {}
    if not ('interpolationtype' in variables):
        variables['interpolationtype'] = "linear"
    keys = list(variables.keys())
    for i in range(len(keys)):  # Determine current keyframe and next one for this variable
        key = keys[i]
        curkeyframe = None
        nextkeyframe = None
        for i in range(len(keyframes)):
            try:
                frame = keyframes[i]
                if (frame.variables[key] != None):  # If the current keyframe has a keyed value for the current variable
                    if frame.frame <= curframe:  # If its frame is below or equal to the current, it is the current keyframe
                        curkeyframe = i
                    if (nextkeyframe == None) and (frame.frame > curframe):  # If this is the first keyframe with a frame higher than the current, it is the next keyframe
                        nextkeyframe = i
            except KeyError:
                pass
        if nextkeyframe == None or key == "interpolationtype":  # If there is no next key frame, maintain the value specified by the current one
            finalvariables[key] = keyframes[curkeyframe].variables[key]  # (Also do this if it is an interpolation type variable; they should only change once their next keyframe has been reached
        else:  # Interpolate between the current and next keyframes
            if keyframes[nextkeyframe].variables['interpolationtype'] == "linear":
                finalvariables[key] = LinearInterpolateKeyframes(curframe, keyframes[curkeyframe].frame, keyframes[nextkeyframe].frame, keyframes[curkeyframe].variables[key], keyframes[nextkeyframe].variables[key])
            elif keyframes[nextkeyframe].variables['interpolationtype'] == "cosine":
                finalvariables[key] = CosineInterpolateKeyframes(curframe, keyframes[curkeyframe].frame, keyframes[nextkeyframe].frame, keyframes[curkeyframe].variables[key], keyframes[nextkeyframe].variables[key])
    return finalvariables

def dotproduct2d(v1, v2):
    return ((v1[0] * v2[0]) + (v1[1] * v2[1]))

def magnitude(vec):
    # print("type(vec)", type(vec))
    try:
        return sqrt(vec[0] ** 2 + vec[1] ** 2)
    except:
        return 1.0

def magnitudesquared(vec):
    try:
        return (vec[0] ** 2 + vec[1] ** 2)
    except:
        return 1.0

def normalise(vec):
    mag = magnitude(vec)
    return [vec[0] / mag, vec[1] / mag]

def RandomiseStrength(base, range):
    return base + (float(random.randrange(int(-range * 100), int(range * 100))) / 100.0)

def CreateKeyframe(parentframes, frame, variables):
    newframe = Keyframe(frame, variables)
    # Look for duplicate keyframes and copy other defined variables
    try:
        oldkey = next(keyframe for keyframe in parentframes if keyframe.frame == frame)
    except StopIteration:
        oldkey = None
    if oldkey != None:
        for var in oldkey.variables.keys():  # For every variable defined by the old keyframe
            if (var not in newframe.variables or newframe.variables[var] == None) and (oldkey.variables[var] != None):  # If a variable is undefined, copy its value to the new keyframe
                newframe.variables[var] = oldkey.variables[var]
    # Remove the duplicate keyframe, if it existed
    for duplicate in (keyframe for keyframe in parentframes if keyframe.frame == frame):
        parentframes.remove(duplicate)
        break
    # Append the new keyframe then sort them all by frame
    parentframes.append(newframe)
    sortedframes = sorted(parentframes, key=lambda keyframe: keyframe.frame)
    parentframes[:] = sortedframes

def ConsolidateKeyframes(parentframes, frame, variables):
    newframe = Keyframe(frame, variables)
    parentframes.append(newframe)
    finallist = []  # A truncated list of keyframes
    # Append all the frames which come after the current one to the final list
    for keyframe in parentframes:
        if keyframe.frame >= frame:
            finallist.append(keyframe)
    # Sort the keyframes and give them to the parent object
    sortedframes = sorted(finallist, key=lambda keyframe: keyframe.frame)
    parentframes[:] = sortedframes

class XMLNode:
    def __init__(self, parent, tag, meta, data, inside):
        self.tag = tag
        self.meta = meta
        self.data = data
        self.inside = inside
        self.parent = parent
        self.children = []
        self.parsed = False

class XMLParser:
    def __init__(self, data):
        self.data = data
        self.meta = {}
        self.root = None

    def ReadMeta(self):
        while "<?" in self.data:
            index = self.data.find("<?")  # Start of tag
            startindex = index + 2  # Start of tag inside
            endindex = self.data.find("?>", index)  # Tag end

            # Get the contents of the angular brackets and split into separate meta tags
            metaraw = self.data[startindex:endindex].strip()
            separated = metaraw.split("\" ")  # Split like so ('|' = split off):
            # thingy = "value|" |other = "whatever|" |third = "woo!"
            
            for splitraw in separated:
                split = splitraw.split("=")

                # Add it to the dictionary of meta data
                self.meta[split[0].strip()] = split[1].strip().strip('\"')

            # Remove this tag from the stored data
            before = self.data[:index]
            after = self.data[(endindex + 2):]
            self.data = "".join([before, after])

    def GetTagMeta(self, tag):
        meta = {}
        
        metastart = tag.find(" ") + 1
        metaraw = tag[metastart:]
        separated = metaraw.split("\" ")  # Split like so ('|' = split off):
        # thingy = "value|" |other = "whatever|" |third = "woo!"

        for splitraw in separated:
            split = splitraw.split("=")

            # Add it to the dictionary of meta data
            meta[split[0].strip()] = split[1].strip().strip('\"')

        return meta

    def StripXML(self):
        # Remove comments
        while "<!--" in self.data:
            index = self.data.find("<!--")
            endindex = self.data.find("-->", index)
            before = self.data[:index]
            after = self.data[(endindex + 3):]
            self.data = "".join([before, after])

        # Remove whitespace
        self.data = self.data.replace("\n", "").replace("\t", "")

    def GetChildren(self, node):
        pass

    def GetRoot(self):
        rootstart = self.data.find("<")
        rootstartclose = self.data.find(">", rootstart)
        roottagraw = self.data[(rootstart + 1):rootstartclose]
        
        rootmeta = {}
        if len(roottagraw.split("=")) > 1:
            rootmeta = self.GetTagMeta(roottagraw)
        
        roottag = roottagraw.strip()
        
        rootend = self.data.find("</%s" % roottag)
        rootendclose = self.data.find(">", rootend)
        rootdata = self.data[rootstart:(rootendclose + 1)].strip()
        rootinside = self.data[(rootstartclose + 1):rootend]

        self.root = XMLNode(parent = None, tag = roottag, meta = rootmeta, data = rootdata, inside = rootinside)

    def SearchNode(self, node):
        node.parsed = True
        
        tempdata = node.inside
        children = []
        
        while "<" in tempdata:
            start = tempdata.find("<")
            startclose = tempdata.find(">", start)
            tagraw = tempdata[(start + 1):startclose]

            meta = {}
            if "=" in tagraw:
                meta = self.GetTagMeta(tagraw)

            tag = tagraw.split(" ")[0]

            end = tempdata.find("</%s" % tag)
            endclose = tempdata.find(">", end)

            data = tempdata[start:(endclose + 1)].strip()
            inside = tempdata[(startclose + 1):end]

            newnode = XMLNode(node, tag, meta, data, inside)
            children.append(newnode)

            before = tempdata[:start]
            after = tempdata[(endclose + 1):]
            tempdata = "".join([before, after])

        node.children = children

        for child in node.children:
            self.SearchNode(child)

    def Parse(self):
        self.ReadMeta()
        self.StripXML()
        self.GetRoot()
        self.SearchNode(self.root)
        
        return self.root


class Keyframe:
    def __init__(self, frame = 0, variables = {}):
        self.frame = frame
        self.variables = variables
        if not ('interpolationtype' in self.variables):
            self.variables['interpolationtype'] = "linear"          
            
class Particle:
    def __init__(self, parent, initpos, velocity, life, drawtype = 0, colour = (0, 0, 0), radius = 0.0, length = 0.0, image = None, keyframes = []):
        self.parent = parent
        self.pos = initpos
        self.velocity = velocity
        self.life = life
        self.colour = colour
        self.radius = radius
        self.length = length
        self.image = image
        self.drawtype = drawtype
        self.keyframes = []
        self.keyframes.extend(keyframes[:])
        self.curframe = 0
        self.alive = True
    
    def Update(self):
        self.pos = [self.pos[0] + self.velocity[0], self.pos[1] + self.velocity[1]]
        if self.curframe > self.life:
            self.alive = False
        else:
            if not self.parent.color_changed:
                self.colour = (self.parent.particlecache[self.curframe]['colour_r'], self.parent.particlecache[self.curframe]['colour_g'], self.parent.particlecache[self.curframe]['colour_b'])
            self.radius = self.parent.particlecache[self.curframe]['radius']
            self.length = self.parent.particlecache[self.curframe]['length']
            self.curframe = self.curframe + 1
    
    def Draw(self, display):
        if (self.pos[0] > 10000) or (self.pos[1] > 10000) or (self.pos[0] < -10000) or (self.pos[1] < -10000):
            return
        if self.drawtype == DRAWTYPE_POINT:  # Point
            # pygame.draw.circle(display, self.colour, self.pos, 0)
            # cv.Circle(display, (int(self.pos[0]), int(self.pos[1])), 0, self.colour)
            cv2.circle(display ,(int(self.pos[0]), int(self.pos[1])), 0, self.colour)
            
        elif self.drawtype == DRAWTYPE_CIRCLE:  # Circle
            # pygame.draw.circle(display, self.colour, self.pos, self.radius)
            # cv.Circle(display, (int(self.pos[0]), int(self.pos[1])), int(self.radius), self.colour, -1)
            cv2.circle(display ,(int(self.pos[0]), int(self.pos[1])), int(self.radius), self.colour, -1)
            
        elif self.drawtype == DRAWTYPE_LINE:
            if self.length == 0.0:
                # pygame.draw.circle(display, self.colour, self.pos, 0)
                # cv.Circle(display, (int(self.pos[0]), int(self.pos[1])), 0, self.colour)
                cv2.circle(display ,(int(self.pos[0]), int(self.pos[1])), 0, self.colour)
            else:
                velocitymagoverlength = sqrt(self.velocity[0]**2 + self.velocity[1]**2) / self.length
                linevec = [(self.velocity[0] / velocitymagoverlength), (self.velocity[1] / velocitymagoverlength)]
                endpoint = [self.pos[0] + linevec[0], self.pos[1] + linevec[1]]
                # pygame.draw.aaline(display, self.colour, self.pos, endpoint)
                # cv.Line(display, (int(self.pos[0]), int(self.pos[1])), (int(endpoint[0]), int(endpoint[1])), self.colour, lineType=cv.CV_AA)
                cv2.line(display, (int(self.pos[0]), int(self.pos[1])), (int(endpoint[0]), int(endpoint[1])), self.colour)
            
        elif self.drawtype == DRAWTYPE_SCALELINE:  # Scaling line (scales with velocity)
            endpoint = [self.pos[0] + self.velocity[0], self.pos[1] + self.velocity[1]]
            # pygame.draw.aaline(display, self.colour, self.pos, endpoint)
            # cv.Line(display, (int(self.pos[0]), int(self.pos[1])), (int(endpoint[0]), int(endpoint[1])), self.colour, lineType=cv.CV_AA)
            cv2.line(display, (int(self.pos[0]), int(self.pos[1])), (int(endpoint[0]), int(endpoint[1])), self.colour)
            
        elif self.drawtype == DRAWTYPE_BUBBLE:  # Bubble
            if self.radius >= 1.0:
                # pygame.draw.circle(display, self.colour, self.pos, self.radius, 1)
                # cv.Circle(display, (int(self.pos[0]), int(self.pos[1])), int(self.radius), self.colour, 1)
                cv2.circle(display ,(int(self.pos[0]), int(self.pos[1])), int(self.radius), self.colour, 1)
            else:  # Pygame won't draw circles with thickness < radius, so if radius is smaller than one don't bother trying to set thickness
                # pygame.draw.circle(display, self.colour, self.pos, self.radius)
                # cv.Circle(display, (int(self.pos[0]), int(self.pos[1])), int(self.radius), self.colour)
                cv2.circle(display ,(int(self.pos[0]), int(self.pos[1])), int(self.radius), self.colour)
        
        elif self.drawtype == DRAWTYPE_IMAGE:  # Image
            # size = self.image.get_size()
            # display.blit(self.image, (self.pos[0] - size[1], self.pos[1] - size[1]))
            size = self.image.shape
            x, y = self.pos[0] - size[1], self.pos[1] - size[1]
            # print(x, y)
            display = self.Paste(display, self.image, x, y)
    
    def Paste(self, mother, child, x, y):
        "Pastes the numpy image child into the numpy image mother at position (x, y) = coord"
        size = mother.shape
        csize = child.shape
        x = int(x)
        y = int(y)
        # target coordinates need to be within the sizes of the mother
        # otherwise it is outside of the mother and we cancel the pasting
        if y<size[0] and x<size[1] and y+csize[0]>0 and x+csize[1]>0:
            c_offset = [0, 0]
            sel = [y, x, csize[0], csize[1]]
            # if coord x is smaller than 0 (next to the left side of the mother)
            if x<0:
                c_offset[1] = -x
                sel[1] = x = 0
            # if coord y is smaller than 0 (above the upper side of the mother)
            if y<0:
                c_offset[0] = -y
                sel[0] = y = 0
            # if coord x plus childsize x extends mothersize x we cut the selection
            if x+sel[3]>=size[1]:
                sel[3] = int(size[1]-x)
            # if coord y plus childsize y extends mothersize y we cut the selection
            if y+sel[2]>=size[0]:
                sel[2] = int(size[0]-y)
            # we get the region of interest (ROI) from the child
            childpart = child[c_offset[0]:sel[2], c_offset[1]:sel[3]]
            mother[sel[0]:sel[2]+sel[0]-c_offset[0], sel[1]:sel[3]+sel[1]-c_offset[1]] = childpart

    def CreateKeyframe(self, frame, colour = (None, None, None), radius = None, length = None):
        CreateKeyframe(self.keyframes, frame, {'colour_r':colour[0], 'colour_g':colour[1], 'colour_b':colour[2], 'radius':radius, 'length':length})

class ParticleSource:
    def __init__(self, parenteffect, pos, initspeed, initdirection, initspeedrandrange, initdirectionrandrange, particlesperframe, particlelife, genspacing, drawtype = 0, colour = (0, 0, 0), radius = 0.0, length = 0.0, image = None):
        self.parenteffect = parenteffect
        self.pos = pos
        self.initspeed = initspeed
        self.initdirection = initdirection
        self.initspeedrandrange = initspeedrandrange
        self.initdirectionrandrange = initdirectionrandrange
        self.particlesperframe = particlesperframe
        self.particlelife = particlelife
        self.genspacing = genspacing
        self.colour = colour
        self.old_colour = self.colour
        self.color_changed = False
        self.drawtype = drawtype
        self.radius = radius
        self.length = length
        self.image = image
        self.keyframes = []
        self.CreateKeyframe(0, self.pos, self.initspeed, self.initdirection, self.initspeedrandrange, self.initdirectionrandrange, self.particlesperframe, self.genspacing)
        self.particlekeyframes = []
        self.particlecache = []
        self.CreateParticleKeyframe(0, colour = self.colour, radius = self.radius, length = self.length)
        self.curframe = 0
    
    def Update(self):       
        newvars = InterpolateKeyframes(self.curframe, {'pos_x':self.pos[0], 'pos_y':self.pos[1], 'initspeed':self.initspeed, 'initdirection':self.initdirection, 'initspeedrandrange':self.initspeedrandrange, 'initdirectionrandrange':self.initdirectionrandrange, 'particlesperframe':self.particlesperframe, 'genspacing':self.genspacing}, self.keyframes)
        self.pos = (newvars['pos_x'], newvars['pos_y'])
        self.initspeed = newvars['initspeed']
        self.initdirection = newvars['initdirection']
        self.initspeedrandrange = newvars['initspeedrandrange']
        self.initdirectionrandrange = newvars['initdirectionrandrange']
        self.particlesperframe = newvars['particlesperframe']
        self.genspacing = newvars['genspacing']
        particlesperframe = self.particlesperframe
        if (self.genspacing == 0) or ((self.curframe % self.genspacing) == 0):
            for i in range(0, int(particlesperframe)):
                self.CreateParticle()
        self.curframe = self.curframe + 1
    
    def CreateParticle(self):
        if self.initspeedrandrange != 0.0:
            speed = self.initspeed + (float(random.randrange(int(-self.initspeedrandrange * 100.0), int(self.initspeedrandrange * 100.0))) / 100.0)
        else:
            speed = self.initspeed
        if self.initdirectionrandrange != 0.0:
            direction = self.initdirection + (float(random.randrange(int(-self.initdirectionrandrange * 100.0), int(self.initdirectionrandrange * 100.0))) / 100.0)
        else:
            direction = self.initdirection
        velocity = [speed * np.sin(direction), -speed * np.cos(direction)]
        newparticle = Particle(self, initpos = self.pos, velocity = velocity, life = self.particlelife, drawtype = self.drawtype, colour = self.colour, radius = self.radius, length = self.length, image = self.image, keyframes = self.particlekeyframes)
        self.parenteffect.AddParticle(newparticle)

    def CreateKeyframe(self, frame, pos = (None, None), initspeed = None, initdirection = None, initspeedrandrange = None, initdirectionrandrange = None, particlesperframe = None, genspacing = None, interpolationtype = "linear"):
        CreateKeyframe(self.keyframes, frame, {'pos_x':pos[0], 'pos_y':pos[1], 'initspeed':initspeed, 'initdirection':initdirection, 'initspeedrandrange':initspeedrandrange, 'initdirectionrandrange':initdirectionrandrange, 'particlesperframe':particlesperframe, 'genspacing':genspacing, 'interpolationtype':interpolationtype})
    
    def CreateParticleKeyframe(self, frame, colour = (None, None, None), radius = None, length = None, interpolationtype = "linear"):
        CreateKeyframe(self.particlekeyframes, frame, {'colour_r':colour[0], 'colour_g':colour[1], 'colour_b':colour[2], 'radius':radius, 'length':length, 'interpolationtype':interpolationtype})
        self.PreCalculateParticles()
    
    def PreCalculateParticles(self):
        self.particlecache = []  # Clear the cache
        # Interpolate the particle variables for each frame of its life
        for i in range(0, self.particlelife + 1):
            vars = InterpolateKeyframes(i, {'colour_r':0, 'colour_g':0, 'colour_b':0, 'radius':0, 'length':0}, self.particlekeyframes)
            self.particlecache.append(vars)
    
    def ConsolidateKeyframes(self):
        ConsolidateKeyframes(self.keyframes, self.curframe, {'pos_x':self.pos[0], 'pos_y':self.pos[1], 'initspeed':self.initspeed, 'initdirection':self.initdirection, 'initspeedrandrange':self.initspeedrandrange, 'initdirectionrandrange':self.initdirectionrandrange, 'particlesperframe':self.particlesperframe, 'genspacing':self.genspacing})
    
    def SetColour(self, colour):
        self.old_colour = self.colour
        if self.colour != colour:
            self.color_changed = True
        self.colour = colour

    def SetPos(self, newpos):
        self.CreateKeyframe(self.curframe, pos = newpos)
    
    def SetInitSpeed(self, newinitspeed):
        self.CreateKeyframe(self.curframe, initspeed = newinitspeed)
    
    def SetInitDirection(self, newinitdirection):
        self.CreateKeyframe(self.curframe, initdirection = newinitdirection)
    
    def SetInitSpeedRandRange(self, newinitspeedrandrange):
        self.CreateKeyframe(self.curframe, initspeedrandrange = newinitspeedrandrange)
    
    def SetInitDirectionRandRange(self, newinitdirectionrandrange):
        self.CreateKeyframe(self.curframe, initdirectionrandrange = newinitdirectionrandrange)
    
    def SetParticlesPerFrame(self, newparticlesperframe):
        self.CreateKeyframe(self.curframe, particlesperframe = newparticlesperframe)
    
    def SetGenSpacing(self, newgenspacing):
        self.CreateKeyframe(self.curframe, genspacing = newgenspacing)

class ParticleEffect:
    def __init__(self, display, pos, size):
        self.display = display
        self.pos = pos
        self.size = size
        self.left = pos[0]
        self.top = pos[1]
        self.right = pos[0] + size[0]
        self.bottom = pos[1] + size[1]
        self.particles = blist([])
        self.sources = blist([])
        self.gravities = blist([])
        self.obstacles = blist([])
    
    def Update(self):
        for source in self.sources:
            source.Update()
        
        for gravity in self.gravities:
            gravity.Update()
        
        for obstacle in self.obstacles:
            obstacle.Update()

        for particle in self.particles:
            totalforce = [0.0, 0.0]
            
            for gravity in self.gravities:
                force = gravity.GetForce(particle.pos)
                totalforce[0] += force[0]
                totalforce[1] += force[1]
            
            for obstacle in self.obstacles:
                if (not obstacle.OutOfRange(particle.pos)) and (obstacle.InsideObject(particle.pos)):
                    particle.pos = obstacle.GetResolved(particle.pos)
                
                force = obstacle.GetForce(particle.pos, particle.velocity)
                totalforce[0] += force[0]
                totalforce[1] += force[1]
            
            particle.velocity = [particle.velocity[0] + totalforce[0], particle.velocity[1] + totalforce[1]]
            
            particle.Update()
        
        # Delete dead particles
        for particle in self.particles:
            if not particle.alive:
                self.particles.remove(particle)
    
    def Redraw(self):
        for particle in self.particles:
            particle.Draw(self.display)
            
        for obstacle in self.obstacles:
            obstacle.Draw(self.display)
    
    def CreateSource(self, pos = (0, 0), initspeed = 0.0, initdirection = 0.0, initspeedrandrange = 0.0, initdirectionrandrange = 0.0, particlesperframe = 0, particlelife = 0, genspacing = 0, drawtype = 0, colour = (0, 0, 0), radius = 0.0, length = 0.0, image = None):
        newsource = ParticleSource(self, pos, initspeed, initdirection, initspeedrandrange, initdirectionrandrange, particlesperframe, particlelife, genspacing, drawtype, colour, radius, length, image)
        self.sources.append(newsource)
        return newsource  # Effectively a reference
    
    def CreatePointGravity(self, strength = 0.0, strengthrandrange = 0.0, pos = (0, 0)):
        newgrav = PointGravity(strength, strengthrandrange, pos)
        self.gravities.append(newgrav)
        return newgrav
    
    def CreateDirectedGravity(self, strength = 0.0, strengthrandrange = 0.0, direction = [0, 1]):
        newgrav = DirectedGravity(strength, strengthrandrange, direction)
        self.gravities.append(newgrav)
        return newgrav

    def CreateVortexGravity(self, strength = 0.0, strengthrandrange = 0.0, pos = (0, 0)):
        newgrav = VortexGravity(strength, strengthrandrange, pos)
        self.gravities.append(newgrav)
        return newgrav
    
    def CreateCircle(self, pos = (0, 0), colour = (0, 0, 0), bounce = 1.0, radius = 0.0):
        newcircle = Circle(pos, colour, bounce, radius)
        self.obstacles.append(newcircle)
        return newcircle
    
    def CreateRectangle(self, pos = (0, 0), colour = (0, 0, 0), bounce = 1.0, width = 0.0, height = 0.0):
        newrect = Rectangle(pos, colour, bounce, width, height)
        self.obstacles.append(newrect)
        return newrect
    
    def CreateBoundaryLine(self, pos = (0, 0), colour = (0, 0, 0), bounce = 1.0, normal = [0, 1]):
        newline = BoundaryLine(pos, colour, bounce, normal)
        self.obstacles.append(newline)
        return newline
    
    def AddParticle(self, particle):
        self.particles.append(particle)

    def GetDrawtypeAsString(self, drawtype):
        if drawtype == DRAWTYPE_POINT:
            return "point"
        elif drawtype == DRAWTYPE_CIRCLE:
            return "circle"
        elif drawtype == DRAWTYPE_LINE:
            return "line"
        elif drawtype == DRAWTYPE_SCALELINE:
            return "scaleline"
        elif drawtype == DRAWTYPE_BUBBLE:
            return "bubble"
        elif drawtype == DRAWTYPE_IMAGE:
            return "image"
        else:
            return "ERROR: Invalid drawtype"
    
    def GetStringAsDrawtype(self, string):
        if string == "point":
            return DRAWTYPE_POINT
        elif string == "circle":
            return DRAWTYPE_CIRCLE
        elif string == "line":
            return DRAWTYPE_LINE
        elif string == "scaleline":
            return DRAWTYPE_SCALELINE
        elif string == "bubble":
            return DRAWTYPE_BUBBLE
        elif string == "image":
            return DRAWTYPE_IMAGE
        else:
            return DRAWTYPE_POINT
    
    def GetInterpolationtypeAsString(self, interpolationtype):
        if interpolationtype == INTERPOLATIONTYPE_LINEAR:
            return "linear"
        elif interpolationtype == INTERPOLATIONTYPE_COSINE:
            return "cosine"
    
    def GetStringAsInterpolationtype(self, string):
        if string == "linear":
            return INTERPOLATIONTYPE_LINEAR
        elif string == "cosine":
            return INTERPOLATIONTYPE_COSINE
        else:
            return INTERPOLATIONTYPE_LINEAR
    
    def TranslatePos(self, pos):
        return (pos[0] - self.pos[0], pos[1] - self.pos[1])
    
    def ConvertXMLTuple(self, string):
        # 'string' must be of the form "(value, value, value, [...])"
        bracketless = string.replace("(", "").replace(")", "")
        strings = bracketless.split(", ")
        finaltuple = []
        for string in strings:
            temp = string.split(".")
            if len(temp) > 1:
                finaltuple.append(float(string))
            else:
                finaltuple.append(int(string))
        
        return tuple(finaltuple)
    
    def SaveToFile(self, outfilename):
        outfile = open(outfilename, 'w')
        
        outfile.write("<?xml version = \"1.0\"?>\n<?pyignition version = \"%f\"?>\n\n" % PYIGNITION_VERSION)
        outfile.write("<effect>\n")
        
        # Write out sources
        for source in self.sources:
            outfile.write("\t<source>\n")
            
            # Write out source variables
            outfile.write("\t\t<pos>(%i, %i)</pos>\n" % source.pos)
            outfile.write("\t\t<initspeed>%f</initspeed>\n" % source.initspeed)
            outfile.write("\t\t<initdirection>%f</initdirection>\n" % source.initdirection)
            outfile.write("\t\t<initspeedrandrange>%f</initspeedrandrange>\n" % source.initspeedrandrange)
            outfile.write("\t\t<initdirectionrandrange>%f</initdirectionrandrange>\n" % source.initdirectionrandrange)
            outfile.write("\t\t<particlesperframe>%i</particlesperframe>\n" % source.particlesperframe)
            outfile.write("\t\t<particlelife>%i</particlelife>\n" % source.particlelife)
            outfile.write("\t\t<genspacing>%i</genspacing>\n" % source.genspacing)
            outfile.write("\t\t<drawtype>%s</drawtype>\n" % self.GetDrawtypeAsString(source.drawtype))
            outfile.write("\t\t<colour>(%i, %i, %i)</colour>\n" % source.colour)
            outfile.write("\t\t<radius>%f</radius>\n" % source.radius)
            outfile.write("\t\t<length>%f</length>\n" % source.length)
            outfile.write("\t\t<imagepath>%s</imagepath>\n" % source.imagepath)
            
            # Write out source keyframes
            outfile.write("\t\t<keyframes>\n")
            
            for keyframe in source.keyframes:
                if keyframe.frame == 0:  # Don't bother writing out the first keyframe
                    continue
                
                outfile.write("\t\t\t<keyframe frame = \"%i\">\n" % keyframe.frame)
                
                # Write out keyframed variables
                for variable in keyframe.variables.keys():
                    if variable == "interpolationtype":
                        outfile.write("\t\t\t\t<%s>%s</%s>\n" % (variable, self.GetInterpolationtypeAsString(keyframe.variables[variable]), variable))
                    else:
                        outfile.write("\t\t\t\t<%s>%s</%s>\n" % (variable, str(keyframe.variables[variable]), variable))
                
                outfile.write("\t\t\t</keyframe>\n")
            
            outfile.write("\t\t</keyframes>\n")
            
            # Write out source particle keyframes
            outfile.write("\t\t<particlekeyframes>\n")
            
            for keyframe in source.particlekeyframes:
                if keyframe.frame == 0:  # Don't bother writing out the first keyframe
                    continue
                    
                outfile.write("\t\t\t<keyframe frame = \"%i\">\n" % keyframe.frame)
                
                # Write out keyframed variables
                for variable in keyframe.variables.keys():
                    if variable == "interpolationtype":
                        outfile.write("\t\t\t\t<%s>%s</%s>\n" % (variable, self.GetInterpolationtypeAsString(keyframe.variables[variable]), variable))
                    else:
                        outfile.write("\t\t\t\t<%s>%s</%s>\n" % (variable, str(keyframe.variables[variable]), variable))
                
                outfile.write("\t\t\t</keyframe>\n")
            
            outfile.write("\t\t</particlekeyframes>\n")
            
            outfile.write("\t</source>\n\n")
        
        # Write out gravities
        for gravity in self.gravities:
            # Identify type
            gtype = gravity.type
            
            outfile.write("\t<%sgravity>\n" % gtype)
            
            # Write out gravity variables
            outfile.write("\t\t<strength>%f</strength>\n" % gravity.initstrength)
            outfile.write("\t\t<strengthrandrange>%f</strengthrandrange>\n" % gravity.strengthrandrange)
            if gtype == "directed":
                outfile.write("\t\t<direction>(%f, %f)</direction>\n" % tuple(gravity.direction))
            elif gtype == "point" or gtype == "vortex":
                outfile.write("\t\t<pos>(%i, %i)</pos>\n" % gravity.pos)
            
            # Write out gravity keyframes
            outfile.write("\t\t<keyframes>\n")
            
            for keyframe in gravity.keyframes:
                if keyframe.frame == 0:  # Don't bother writing out the first keyframe
                    continue
                
                outfile.write("\t\t\t<keyframe frame = \"%i\">\n" % keyframe.frame)
                
                # Write out keyframed variables
                for variable in keyframe.variables.keys():
                    if variable == "interpolationtype":
                        outfile.write("\t\t\t\t<%s>%s</%s>\n" % (variable, self.GetInterpolationtypeAsString(keyframe.variables[variable]), variable))
                    else:
                        outfile.write("\t\t\t\t<%s>%s</%s>\n" % (variable, str(keyframe.variables[variable]), variable))
                
                outfile.write("\t\t\t</keyframe>\n")
            
            outfile.write("\t\t</keyframes>\n")
            
            outfile.write("\t</%sgravity>\n\n" % gtype)
        
        # Write out obstacles
        for obstacle in self.obstacles:
            # Identify type
            otype = obstacle.type
            
            outfile.write("\t<%s>\n" % otype)
            
            # Write out obstacle variables
            outfile.write("\t\t<pos>(%i, %i)</pos>\n" % obstacle.pos)
            outfile.write("\t\t<colour>(%i, %i, %i)</colour>\n" % obstacle.colour)
            outfile.write("\t\t<bounce>%f</bounce>\n" % obstacle.bounce)
            if otype == "circle":
                outfile.write("\t\t<radius>%f</radius>\n" % obstacle.radius)
            elif otype == "rectangle":
                outfile.write("\t\t<width>%i</width>\n" % obstacle.width)
                outfile.write("\t\t<height>%i</height>\n" % obstacle.height)
            elif otype == "boundaryline":
                outfile.write("\t\t<normal>(%f, %f)</normal>\n" % tuple(obstacle.normal))
            
            # Write out obstacle keyframes
            outfile.write("\t\t<keyframes>\n")
            
            for keyframe in obstacle.keyframes:
                if keyframe.frame == 0:  # Don't bother writing out the first keyframe
                    continue
                
                outfile.write("\t\t\t<keyframe frame = \"%i\">\n" % keyframe.frame)
                
                # Write out keyframed variables
                for variable in keyframe.variables.keys():
                    if variable == "interpolationtype":
                        outfile.write("\t\t\t\t<%s>%s</%s>\n" % (variable, self.GetInterpolationtypeAsString(keyframe.variables[variable]), variable))
                    else:
                        outfile.write("\t\t\t\t<%s>%s</%s>\n" % (variable, str(keyframe.variables[variable]), variable))
                
                outfile.write("\t\t\t</keyframe>\n")
            
            outfile.write("\t\t</keyframes>\n")
            
            outfile.write("\t</%s>\n\n" % otype)
        
        outfile.write("</effect>")
        outfile.close()
    
    def LoadFromFile(self, infilename):
        infile = open(infilename, "r")
        
        data = xml.XMLParser(infile.read()).Parse()
        infile.close()
        
        for child in data.children:
            if child.tag == "source":  # Source object
                pos = (0, 0)
                initspeed = 0.0
                initdirection = 0.0
                initspeedrandrange = 0.0
                initdirectionrandrange = 0.0
                particlesperframe = 0
                particlelife = 0
                genspacing = 0
                drawtype = DRAWTYPE_POINT
                colour = (0, 0, 0)
                radius = 0.0
                length = 0.0
                imagepath = None
                
                keyframes = None
                particlekeyframes = None
                
                for parameter in child.children:
                    if parameter.tag == "pos":
                        pos = self.ConvertXMLTuple(parameter.inside)
                    elif parameter.tag == "initspeed":
                        initspeed = float(parameter.inside)
                    elif parameter.tag == "initdirection":
                        initdirection = float(parameter.inside)
                    elif parameter.tag == "initspeedrandrange":
                        initspeedrandrange = float(parameter.inside)
                    elif parameter.tag == "initdirectionrandrange":
                        initdirectionrandrange = float(parameter.inside)
                    elif parameter.tag == "particlesperframe":
                        particlesperframe = int(parameter.inside)
                    elif parameter.tag == "particlelife":
                        particlelife = int(parameter.inside)
                    elif parameter.tag == "genspacing":
                        genspacing = int(parameter.inside)
                    elif parameter.tag == "drawtype":
                        drawtype = self.GetStringAsDrawtype(parameter.inside)
                    elif parameter.tag == "colour":
                        colour = self.ConvertXMLTuple(parameter.inside)
                    elif parameter.tag == "radius":
                        radius = float(parameter.inside)
                    elif parameter.tag == "length":
                        length = float(parameter.inside)
                    elif parameter.tag == "image":
                        imagepath = float(parameter.inside)
                    elif parameter.tag == "keyframes":
                        keyframes = parameter.children
                    elif parameter.tag == "particlekeyframes":
                        particlekeyframes = parameter.children
                
                newsource = self.CreateSource(pos, initspeed, initdirection, initspeedrandrange, initdirectionrandrange, particlesperframe, particlelife, genspacing, drawtype, colour, radius, length, imagepath)
                
                for keyframe in keyframes:
                    frame = int(keyframe.meta['frame'])
                    variables = {}
                    
                    for variable in keyframe.children:
                        if variable.tag == "pos_x" and variable.inside != "None":
                            variables['pos_x'] = int(variable.inside)
                        elif variable.tag == "pos_y" and variable.inside != "None":
                            variables['pos_y'] = int(variable.inside)
                        elif variable.tag == "initspeed" and variable.inside != "None":
                            variables['initspeed'] = float(variable.inside)
                        elif variable.tag == "initdirection" and variable.inside != "None":
                            variables['initdirection'] = float(variable.inside)
                        elif variable.tag == "initspeedrandrange" and variable.inside != "None":
                            variables['initspeedrandrange'] = float(variable.inside)
                        elif variable.tag == "initdirectionrandrange" and variable.inside != "None":
                            variables['initdirectionrandrange'] = float(variable.inside)
                        elif variable.tag == "particlesperframe" and variable.inside != "None":
                            variables['particlesperframe'] = int(variable.inside)
                        elif variable.tag == "genspacing" and variable.inside != "None":
                            variables['genspacing'] = int(variable.inside)
                        elif variable.tag == "interpolationtype" and variable.inside != "None":
                            variables['interpolationtype'] = self.GetStringAsInterpolationtype(variable.inside)
                        
                    newframe = newsource.CreateKeyframe(frame = frame)
                    newframe.variables = variables
                
                for keyframe in particlekeyframes:
                    frame = int(keyframe.meta['frame'])
                    variables = {}
                    
                    for variable in keyframe.children:
                        if variable.tag == "colour_r" and variable.inside != "None":
                            variables['colour_r'] = int(variable.inside)
                        elif variable.tag == "colour_g" and variable.inside != "None":
                            variables['colour_g'] = int(variable.inside)
                        elif variable.tag == "colour_b" and variable.inside != "None":
                            variables['colour_b'] = int(variable.inside)
                        elif variable.tag == "radius" and variable.inside != "None":
                            variables['radius'] = float(variable.inside)
                        elif variable.tag == "length" and variable.inside != "None":
                            variables['length'] = float(variable.inside)
                        elif variable.tag == "interpolationtype" and variable.inside != "None":
                            variables['interpolationtype'] = self.GetStringAsInterpolationtype(variable.inside)
                    
                    newframe = newsource.CreateParticleKeyframe(frame = frame)
                    newframe.variables = variables
                    newsource.PreCalculateParticles()
            
            elif child.tag == "directedgravity":
                strength = 0.0
                strengthrandrange = 0.0
                direction = [0, 0]
                
                keyframes = None
                
                for parameter in child.children:
                    if parameter.tag == "strength":
                        strength = float(parameter.inside)
                    elif parameter.tag == "strengthrandrange":
                        strengthrandrange = float(parameter.inside)
                    elif parameter.tag == "direction":
                        direction = self.ConvertXMLTuple(parameter.inside)
                    elif parameter.tag == "keyframes":
                        keyframes = parameter.children
                
                newgrav = self.CreateDirectedGravity(strength, strengthrandrange, direction)
                
                for keyframe in keyframes:
                    frame = int(keyframe.meta['frame'])
                    variables = {}
                    
                    for variable in keyframe.children:
                        if variable.tag == "strength" and variable.inside != "None":
                            variables['strength'] = float(variable.inside)
                        elif variable.tag == "strengthrandrange" and variable.inside != "None":
                            variables['strengthrandrange'] = float(variable.inside)
                        elif  variable.tag == "direction_x" and variable.inside != "None":
                            variables['direction_x'] = float(variable.inside)
                        elif  variable.tag == "direction_y" and variable.inside != "None":
                            variables['direction_y'] = float(variable.inside)
                        elif variable.tag == "interpolationtype" and variable.inside != "None":
                            variables['interpolationtype'] = self.GetStringAsInterpolationtype(variable.inside)
                    
                    newframe = newgrav.CreateKeyframe(frame = frame)
                    newframe.variables = variables
            
            elif child.tag == "pointgravity":
                strength = 0.0
                strengthrandrange = 0.0
                pos = (0, 0)
                
                keyframes = None
                
                for parameter in child.children:
                    if parameter.tag == "strength":
                        strength = float(parameter.inside)
                    elif parameter.tag == "strengthrandrange":
                        strengthrandrange = float(parameter.inside)
                    elif parameter.tag == "pos":
                        pos = self.ConvertXMLTuple(parameter.inside)
                    elif parameter.tag == "keyframes":
                        keyframes = parameter.children
                
                newgrav = self.CreatePointGravity(strength, strengthrandrange, pos)
                
                for keyframe in keyframes:
                    frame = int(keyframe.meta['frame'])
                    variables = {}
                    
                    for variable in keyframe.children:
                        if variable.tag == "strength" and variable.inside != "None":
                            variables['strength'] = float(variable.inside)
                        elif variable.tag == "strengthrandrange" and variable.inside != "None":
                            variables['strengthrandrange'] = float(variable.inside)
                        elif  variable.tag == "pos_x" and variable.inside != "None":
                            variables['pos_x'] = int(variable.inside)
                        elif  variable.tag == "pos_y" and variable.inside != "None":
                            variables['pos_y'] = int(variable.inside)
                        elif variable.tag == "interpolationtype" and variable.inside != "None":
                            variables['interpolationtype'] = self.GetStringAsInterpolationtype(variable.inside)
                    
                    newframe = newgrav.CreateKeyframe(frame = frame)
                    newframe.variables = variables
            
            elif child.tag == "vortexgravity":
                strength = 0.0
                strengthrandrange = 0.0
                pos = (0, 0)
                
                keyframes = None
                
                for parameter in child.children:
                    if parameter.tag == "strength":
                        strength = float(parameter.inside)
                    elif parameter.tag == "strengthrandrange":
                        strengthrandrange = float(parameter.inside)
                    elif parameter.tag == "pos":
                        direction = self.ConvertXMLTuple(parameter.inside)
                    elif parameter.tag == "keyframes":
                        keyframes = parameter.children
                
                newgrav = self.CreateVortexGravity(strength, strengthrandrange, pos)
                
                for keyframe in keyframes:
                    frame = int(keyframe.meta['frame'])
                    variables = {}
                    
                    for variable in keyframe.children:
                        if variable.tag == "strength" and variable.inside != "None":
                            variables['strength'] = float(variable.inside)
                        elif variable.tag == "strengthrandrange" and variable.inside != "None":
                            variables['strengthrandrange'] = float(variable.inside)
                        elif  variable.tag == "pos_x" and variable.inside != "None":
                            variables['pos_x'] = int(variable.inside)
                        elif  variable.tag == "pos_y" and variable.inside != "None":
                            variables['pos_y'] = int(variable.inside)
                        elif variable.tag == "interpolationtype" and variable.inside != "None":
                            variables['interpolationtype'] = self.GetStringAsInterpolationtype(variable.inside)
                    
                    newframe = newgrav.CreateKeyframe(frame = frame)
                    newframe.variables = variables
            
            elif child.tag == "circle":
                pos = (0, 0)
                colour = (0, 0, 0)
                bounce = 0.0
                radius = 0.0
                
                keyframes = None
                
                for parameter in child.children:
                    if parameter.tag == "pos":
                        pos = self.ConvertXMLTuple(parameter.inside)
                    elif parameter.tag == "colour":
                        colour = self.ConvertXMLTuple(parameter.inside)
                    elif parameter.tag == "bounce":
                        bounce = float(parameter.inside)
                    elif parameter.tag == "radius":
                        radius = float(parameter.inside)
                    elif parameter.tag == "keyframes":
                        keyframes = parameter.children
                
                newobstacle = self.CreateCircle(pos, colour, bounce, radius)
                
                for keyframe in keyframes:
                    frame = int(keyframe.meta['frame'])
                    variables = {}
                    
                    for variable in keyframe.children:
                        if variable.tag == "pos_x" and variable.inside != "None":
                            variables['pos_x'] = int(variable.inside)
                        elif variable.tag == "pos_y" and variable.inside != "None":
                            variables['pos_y'] = int(variable.inside)
                        elif variable.tag == "colour_r" and variable.inside != "None":
                            variables['colour_r'] = int(variable.inside)
                        elif variable.tag == "colour_g" and variable.inside != "None":
                            variables['colour_g'] = int(variable.inside)
                        elif variable.tag == "colour_b" and variable.inside != "None":
                            variables['colour_b'] = int(variable.inside)
                        elif variable.tag == "bounce" and variable.inside != "None":
                            variables['bounce'] = float(variable.inside)
                        elif variable.tag == "radius" and variable.inside != "None":
                            variables['radius'] = float(variable.inside)
                        elif variable.tag == "interpolationtype" and variable.inside != "None":
                            variables['interpolationtype'] = self.GetStringAsInterpolationtype(variable.inside)
                    
                    newframe = newobstacle.CreateKeyframe(frame = frame)
                    newframe.variables = variables
        
            elif child.tag == "rectangle":
                pos = (0, 0)
                colour = (0, 0, 0)
                bounce = 0.0
                width = 0.0
                height = 0.0
                
                keyframes = None
                
                for parameter in child.children:
                    if parameter.tag == "pos":
                        pos = self.ConvertXMLTuple(parameter.inside)
                    elif parameter.tag == "colour":
                        colour = self.ConvertXMLTuple(parameter.inside)
                    elif parameter.tag == "bounce":
                        bounce = float(parameter.inside)
                    elif parameter.tag == "width":
                        width = float(parameter.inside)
                    elif parameter.tag == "height":
                        height = float(parameter.inside)
                    elif parameter.tag == "keyframes":
                        keyframes = parameter.children
                
                newobstacle = self.CreateRectangle(pos, colour, bounce, width, height)
                
                for keyframe in keyframes:
                    frame = int(keyframe.meta['frame'])
                    variables = {}
                    
                    for variable in keyframe.children:
                        if variable.tag == "pos_x" and variable.inside != "None":
                            variables['pos_x'] = int(variable.inside)
                        elif variable.tag == "pos_y" and variable.inside != "None":
                            variables['pos_y'] = int(variable.inside)
                        elif variable.tag == "colour_r" and variable.inside != "None":
                            variables['colour_r'] = int(variable.inside)
                        elif variable.tag == "colour_g" and variable.inside != "None":
                            variables['colour_g'] = int(variable.inside)
                        elif variable.tag == "colour_b" and variable.inside != "None":
                            variables['colour_b'] = int(variable.inside)
                        elif variable.tag == "bounce" and variable.inside != "None":
                            variables['bounce'] = float(variable.inside)
                        elif variable.tag == "width" and variable.inside != "None":
                            variables['width'] = float(variable.inside)
                        elif variable.tag == "height" and variable.inside != "None":
                            variables['height'] = float(variable.inside)
                        elif variable.tag == "interpolationtype" and variable.inside != "None":
                            variables['interpolationtype'] = self.GetStringAsInterpolationtype(variable.inside)
                    
                    newframe = newobstacle.CreateKeyframe(frame = frame)
                    newframe.variables = variables
        
            elif child.tag == "boundaryline":
                pos = (0, 0)
                colour = (0, 0, 0)
                bounce = 0.0
                direction = [0.0, 0.0]
                
                keyframes = None
                
                for parameter in child.children:
                    if parameter.tag == "pos":
                        pos = self.ConvertXMLTuple(parameter.inside)
                    elif parameter.tag == "colour":
                        colour = self.ConvertXMLTuple(parameter.inside)
                    elif parameter.tag == "bounce":
                        bounce = float(parameter.inside)
                    elif parameter.tag == "normal":
                        normal = self.ConvertXMLTuple(parameter.inside)
                    elif parameter.tag == "keyframes":
                        keyframes = parameter.children
                
                newobstacle = self.CreateBoundaryLine(pos, colour, bounce, normal)
                
                for keyframe in keyframes:
                    frame = int(keyframe.meta['frame'])
                    variables = {}
                    
                    for variable in keyframe.children:
                        if variable.tag == "pos_x" and variable.inside != "None":
                            variables['pos_x'] = int(variable.inside)
                        elif variable.tag == "pos_y" and variable.inside != "None":
                            variables['pos_y'] = int(variable.inside)
                        elif variable.tag == "colour_r" and variable.inside != "None":
                            variables['colour_r'] = int(variable.inside)
                        elif variable.tag == "colour_g" and variable.inside != "None":
                            variables['colour_g'] = int(variable.inside)
                        elif variable.tag == "colour_b" and variable.inside != "None":
                            variables['colour_b'] = int(variable.inside)
                        elif variable.tag == "bounce" and variable.inside != "None":
                            variables['bounce'] = float(variable.inside)
                        elif variable.tag == "normal_x" and variable.inside != "None":
                            variables['normal_x'] = float(variable.inside)
                        elif variable.tag == "normal_y" and variable.inside != "None":
                            variables['normal_y'] = float(variable.inside)
                        elif variable.tag == "interpolationtype" and variable.inside != "None":
                            variables['interpolationtype'] = self.GetStringAsInterpolationtype(variable.inside)
                    
                    newframe = newobstacle.CreateKeyframe(frame = frame)
                    newframe.variables = variables


class DirectedGravity:
    def __init__(self, strength = 0.0, strengthrandrange = 0.0, direction = [0, 1]):
        self.initstrength = strength
        self.strength = strength
        self.strengthrandrange = strengthrandrange
        directionmag = sqrt(direction[0]**2 + direction[1]**2)
        self.direction = [direction[0] / directionmag, direction[1] / directionmag]
        
        self.keyframes = []
        self.CreateKeyframe(0, self.strength, self.strengthrandrange, self.direction)
        self.curframe = 0
    
    def Update(self):
        newvars = InterpolateKeyframes(self.curframe, {'strength':self.initstrength, 'strengthrandrange':self.strengthrandrange, 'direction_x':self.direction[0], 'direction_y':self.direction[1]}, self.keyframes)
        self.initstrength = newvars['strength']
        self.strengthrandrange = newvars['strengthrandrange']
        self.direction = [newvars['direction_x'], newvars['direction_y']]
        if self.strengthrandrange != 0.0:
            self.strength = RandomiseStrength(self.initstrength, self.strengthrandrange)
        self.curframe = self.curframe + 1
    
    def GetForce(self, pos):
        force = [self.strength * self.direction[0], self.strength * self.direction[1]]
        return force
    
    def GetForceOnParticle(self, particle):
        return self.GetForce(particle.pos)

    def CreateKeyframe(self, frame, strength = None, strengthrandrange = None, direction = [None, None], interpolationtype = "linear"):
        CreateKeyframe(self.keyframes, frame, {'strength':strength, 'strengthrandrange':strengthrandrange, 'direction_x':direction[0], 'direction_y':direction[1], 'interpolationtype':interpolationtype})
    
    def ConsolidateKeyframes(self):
        ConsolidateKeyframes(self.keyframes, self.curframe, {'strength':self.initstrength, 'strengthrandrange':self.strengthrandrange, 'direction_x':self.direction[0], 'direction_y':self.direction[1]})
    
    def SetStrength(self, newstrength):
        self.CreateKeyframe(self.curframe, strength = newstrength)
    
    def SetStrengthRandRange(self, newstrengthrandrange):
        self.CreateKeyframe(self.curframe, strengthrandrange = newstrengthrandrange)
    
    def SetDirection(self, newdirection):
        self.CreateKeyframe(self.curframe, direction = newdirection)


class PointGravity:
    def __init__(self, strength = 0.0, strengthrandrange = 0.0, pos = (0, 0)):
        self.initstrength = strength
        self.strength = strength
        self.strengthrandrange = strengthrandrange
        self.pos = pos
        
        self.keyframes = []
        self.CreateKeyframe(0, self.strength, self.strengthrandrange, self.pos)
        self.curframe = 0
    
    def Update(self):
        newvars = InterpolateKeyframes(self.curframe, {'strength':self.initstrength, 'strengthrandrange':self.strengthrandrange, 'pos_x':self.pos[0], 'pos_y':self.pos[1]}, self.keyframes)
        self.initstrength = newvars['strength']
        self.strengthrandrange = newvars['strengthrandrange']
        self.pos = (newvars['pos_x'], newvars['pos_y'])
        
        if self.strengthrandrange != 0.0:
            self.strength = RandomiseStrength(self.initstrength, self.strengthrandrange)
        else:
            self.strength = self.initstrength
        
        self.curframe = self.curframe + 1
    
    def GetForce(self, pos):
        distsquared = (pow(float(pos[0] - self.pos[0]), 2.0) + pow(float(pos[1] - self.pos[1]), 2.0))
        if distsquared == 0.0:
            return [0.0, 0.0]
        
        forcemag = (self.strength * UNIVERSAL_CONSTANT_OF_MAKE_GRAVITY_LESS_STUPIDLY_SMALL) / (distsquared)
        
        # Calculate normal vector from pos to the gravity point and multiply by force magnitude to find force vector
        dist = sqrt(distsquared)
        dx = float(self.pos[0] - pos[0]) / dist
        dy = float(self.pos[1] - pos[1]) / dist
        
        force = [forcemag * dx, forcemag * dy]
        
        return force

    def GetForceOnParticle(self, particle):
        return self.GetForce(particle.pos)

    def GetMaxForce(self):
        return self.strength * UNIVERSAL_CONSTANT_OF_MAKE_GRAVITY_LESS_STUPIDLY_SMALL
    
    def CreateKeyframe(self, frame, strength = None, strengthrandrange = None, pos = (None, None), interpolationtype = "linear"):
        CreateKeyframe(self.keyframes, frame, {'strength':strength, 'strengthrandrange':strengthrandrange, 'pos_x':pos[0], 'pos_y':pos[1], 'interpolationtype':interpolationtype})
    
    def ConsolidateKeyframes(self):
        ConsolidateKeyframes(self.keyframes, self.curframe, {'strength':self.initstrength, 'strengthrandrange':self.strengthrandrange, 'pos_x':self.pos[0], 'pos_y':self.pos[1]})
    
    def SetStrength(self, newstrength):
        self.CreateKeyframe(self.curframe, strength = newstrength)
    
    def SetStrengthRandRange(self, newstrengthrandrange):
        self.CreateKeyframe(self.curframe, strengthrandrange = newstrengthrandrange)
    
    def SetPos(self, newpos):
        self.CreateKeyframe(self.curframe, pos = newpos)

class VortexGravity(PointGravity):
    def __init__(self, strength = 0.0, strengthrandrange = 0.0, pos = (0, 0)):
        PointGravity.__init__(self, strength, strengthrandrange, pos)
        self.type = "vortex"
        self.keyframes = self.CreateKeyframe(0, self.strength, self.strengthrandrange, self.pos)
    
    def Update(self):           
        newvars = InterpolateKeyframes(self.curframe, {'strength':self.initstrength, 'strengthrandrange':self.strengthrandrange, 'pos_x':self.pos[0], 'pos_y':self.pos[1]}, self.keyframes)
        if newvars is None: return
        self.initstrength = newvars['strength']
        self.strengthrandrange = newvars['strengthrandrange']
        self.pos = (newvars['pos_x'], newvars['pos_y'])
        
        if self.strengthrandrange != 0.0:
            self.strength = RandomiseStrength(self.initstrength, self.strengthrandrange)
        else:
            self.strength = self.initstrength
        
        self.curframe = self.curframe + 1
    
    def GetForce(self, pos):
        try:
            self.alreadyshownerror
        except:
            print("WARNING: VortexGravity relies upon particle velocities as well as positions, and so its \
                force can only be obtained using GetForceOnParticle([PyIgnition particle object]).".replace("\t", ""))
            self.alreadyshownerror = True
        
        return [0.0, 0.0]
    
    def GetForceOnParticle(self, particle):
        # This uses F = m(v^2 / r) (the formula for centripetal force on an object moving in a circle)
        # to determine what force should be applied to keep an object circling the gravity. A small extra
        # force (self.strength * VORTEX_ACCELERATION) is added in order to accelerate objects inward as
        # well, thus creating a spiralling effect. Note that unit mass is assumed throughout.
        
        distvector = [self.pos[0] - particle.pos[0], self.pos[1] - particle.pos[1]]  # Vector from the particle to this gravity
        try:
            distmag = sqrt(float(distvector[0] ** 2) + float(distvector[1] ** 2))  # Distance from the particle to this gravity
        except:
            return [0.0, 0.0]  # This prevents OverflowErrors
        
        if distmag == 0.0:
            return [0.0, 0.0]
        
        if distmag <= VORTEX_SWALLOWDIST:
            particle.alive = False
        
        normal = [float(distvector[0]) / distmag, float(distvector[1]) / distmag]  # Normal from particle to this gravity
        
        velocitymagsquared = (particle.velocity[0] ** 2) + (particle.velocity[1] ** 2)  # Velocity magnitude squared
        forcemag = (velocitymagsquared / distmag) + (self.strength * VORTEX_ACCELERATION)  # Force magnitude = (v^2 / r) + radial acceleration
        
        #velparmag = (particle.velocity[0] * normal[0]) + (particle.velocity[1] * normal[1])  # Magnitude of velocity parallel to normal
        #velpar = [normal[0] * velparmag, normal[1] * velparmag]  # Vector of velocity parallel to normal
        #velperp = [particle.velocity[0] - velpar[0], particle.velocity[1] - velpar[1]]  # Vector of velocity perpendicular to normal
        #
        #fnpar = [-velperp[1], velperp[0]]  # Force normal parallel to normal
        #fnperp = [velpar[1], -velpar[0]]  # Force normal perpendicular to normal
        #
        #force = [(fnpar[0] + fnperp[0]) * forcemag, (fnpar[1] + fnperp[1]) * forcemag]
        
        force = [normal[0] * forcemag, normal[1] * forcemag]  # Works, but sometimes goes straight to the gravity w/ little spiraling
        
        return force
    
    def CreateKeyframe(self, frame, strength = None, strengthrandrange = None, pos = (None, None), interpolationtype = INTERPOLATIONTYPE_LINEAR):
        return CreateKeyframe(self.keyframes, frame, {'strength':strength, 'strengthrandrange':strengthrandrange, 'pos_x':pos[0], 'pos_y':pos[1], 'interpolationtype':interpolationtype})
    
    def ConsolidateKeyframes(self):
        self.keyframes.ConsolidateKeyframes(self.keyframes, self.curframe, {'strength':self.initstrength, 'strengthrandrange':self.strengthrandrange, 'pos_x':self.pos[0], 'pos_y':self.pos[1]})

class Obstacle:
    def __init__(self, pos, colour, bounce):
        self.pos = pos
        self.colour = colour
        self.bounce = bounce
        self.maxdist = MAXDIST  # The maximum (square-based, not circle-based) distance away for which forces will still be calculated
        self.curframe = 0
        self.keyframes = []
    
    def Draw(self, display):
        pass
    
    def Update(self):
        self.curframe = self.curframe + 1
    
    def OutOfRange(self, pos):
        return (abs(pos[0] - self.pos[0]) > self.maxdist) or (abs(pos[1] - self.pos[1]) > self.maxdist)
    
    def InsideObject(self, pos):
        pass
    
    def GetResolved(self, pos):  # Get a resolved position for a particle located inside the object
        pass
    
    def GetDist(self, pos):
        return magnitude([pos[0] - self.pos[0], pos[1] - self.pos[1]])
    
    def GetNormal(self, pos):  # Gets the normal relevant to a particle at the supplied potision (for example, that of the appropriate side of a squre)
        pass
    
    def GetForceFactor(self, pos):  # Gets the force as a factor of maximum available force (0.0 - 1.0), determined by an inverse cube distance law
        pass
    
    def GetForce(self, pos, velocity):  # Gets the final (vector) force
        if self.OutOfRange(pos) or self.bounce == 0.0:
            return [0.0, 0.0]
        
        if (pos[0] == self.pos[0]) and (pos[1] == self.pos[1]):
            return [0.0, 0.0]
        
        normal = self.GetNormal(pos)
        scalingfactor = -dotproduct2d(normal, velocity)  # An integer between 0.0 and 1.0 used to ensure force is maximised for head-on collisions and minimised for scrapes
        
        if scalingfactor <= 0.0:  # The force should never be attractive, so take any negative value of the scaling factor to be zero
            return [0.0, 0.0]  # A scaling factor of zero always results in zero force
        
        forcefactor = (self.GetForceFactor(pos))
        velmag = magnitude(velocity)  # Magnitude of the velocity - multiplied in the force equation
        
        # Force = bounce factor * velocity * distance force factor (0.0 - 1.0) * angle force factor (0.0 - 1.0), along the direction of the normal pointing away from the obstacle
        return [normal[0] * forcefactor * velmag * scalingfactor * self.bounce, normal[1] * forcefactor * velmag * scalingfactor * self.bounce]
    
    def CreateKeyframe(self):
        pass
    
    def SetPos(self, newpos):
        self.CreateKeyframe(self.curframe, pos = newpos)
    
    def SetColour(self, newcolour):
        self.CreateKeyframe(self.curframe, colour = newcolour)
    
    def SetBounce(self, newbounce):
        self.CreateKeyframe(self.curframe, bounce = newbounce)


class Circle(Obstacle):
    def __init__(self, pos, colour, bounce, radius):
        Obstacle.__init__(self, pos, colour, bounce)
        self.radius = radius
        self.radiussquared = self.radius ** 2
        self.maxdist = MAXDIST + self.radius
        self.CreateKeyframe(0, self.pos, self.colour, self.bounce, self.radius)
    
    def Draw(self, display):
        # pygame.draw.circle(display, self.colour, self.pos, self.radius)
        # cv.Circle(display, (int(self.pos[0]), int(self.pos[1])), int(self.radius), self.colour, -1)
        cv2.circle(display, (int(self.pos[0]), int(self.pos[1])), int(self.radius), self.colour, -1)
    
    def Update(self):
        newvars = InterpolateKeyframes(self.curframe, {'pos_x':self.pos[0], 'pos_y':self.pos[1], 'colour_r':self.colour[0], 'colour_g':self.colour[1], 'colour_b':self.colour[2], 'bounce':self.bounce, 'radius':self.radius}, self.keyframes)
        self.pos = (newvars['pos_x'], newvars['pos_y'])
        self.colour = (newvars['colour_r'], newvars['colour_g'], newvars['colour_b'])
        self.bounce = newvars['bounce']
        self.radius = newvars['radius']
        
        Obstacle.Update(self)
    
    def InsideObject(self, pos):
        return (magnitudesquared([pos[0] - self.pos[0], pos[1] - self.pos[1]]) < self.radiussquared)
    
    def GetResolved(self, pos):
        if pos == self.pos:  # If the position is at this obstacle's origin, shift it up a pixel to avoid divide-by-zero errors
            return self.GetResolved([pos[0], pos[1] - 1])
            
        vec = [pos[0] - self.pos[0], pos[1] - self.pos[1]]
        mag = magnitude(vec)
        nor = [vec[0] / mag, vec[1] / mag]
        correctedvec = [nor[0] * self.radius, nor[1] * self.radius]
        
        return [self.pos[0] + correctedvec[0], self.pos[1] + correctedvec[1]]
    
    def GetNormal(self, pos):
        vec = [pos[0] - self.pos[0], pos[1] - self.pos[1]]
        mag = magnitude(vec)
        
        return [vec[0] / mag, vec[1] / mag]
    
    def GetForceFactor(self, pos):      
        nvec = self.GetNormal(pos)
        tempradius = self.radius
        vec = [tempradius * nvec[0], tempradius * nvec[1]]
        newpos = [pos[0] - vec[0], pos[1] - vec[1]]
        
        distcubed = (abs(pow(float(newpos[0] - self.pos[0]), 3.0)) + abs(pow(float(newpos[1] - self.pos[1]), 3.0)))
        if distcubed <= 1.0:
            return 1.0
        
        force = (1.0 / distcubed)
        
        return force
    
    def CreateKeyframe(self, frame, pos = (None, None), colour = (None, None, None), bounce = None, radius = None, interpolationtype = "linear"):
        CreateKeyframe(self.keyframes, frame, {'pos_x':pos[0], 'pos_y':pos[1], 'colour_r':colour[0], 'colour_g':colour[1], 'colour_b':colour[2], 'bounce':bounce, 'radius':radius, 'interpolationtype':interpolationtype})
    
    def ConsolidateKeyframes(self):
        ConsolidateKeyframes(self.keyframes, self.curframe, {'pos_x':self.pos[0], 'pos_y':self.pos[1], 'colour_r':self.colour[0], 'colour_g':self.colour[1], 'colour_b':self.colour[2], 'bounce':self.bounce, 'radius':self.radius})
    
    def SetRadius(self, newradius):
        self.CreateKeyframe(self.curframe, radius = newradius)


class Rectangle(Obstacle):
    def __init__(self, pos, colour, bounce, width, height):
        Obstacle.__init__(self, pos, colour, bounce)
        self.width = width
        self.halfwidth = self.width / 2.0
        self.height = height
        self.halfheight = height / 2.0
        self.maxdist = max(self.halfwidth, self.halfheight) + MAXDIST
        self.CreateKeyframe(0, self.pos, self.colour, self.bounce, self.width, self.height)
    
    def Draw(self, display):
        # pygame.draw.rect(display, self.colour, pygame.Rect(self.pos[0] - self.halfwidth, self.pos[1] - self.halfheight, self.width, self.height))
        (x, y) = (self.pos[0] - self.halfwidth, self.pos[1] - self.halfheight)
        # cv.Rectangle(display, (int(x), int(y)), (int(x+self.width), int(y+self.height)), self.colour)
        cv2.rectangle(display, (int(x), int(y)), (int(x+self.width), int(y+self.height)), self.colour)
    
    def Update(self):
        newvars = InterpolateKeyframes(self.curframe, {'pos_x':self.pos[0], 'pos_y':self.pos[1], 'colour_r':self.colour[0], 'colour_g':self.colour[1], 'colour_b':self.colour[2], 'bounce':self.bounce, 'width':self.width, 'height':self.height}, self.keyframes)
        self.pos = (newvars['pos_x'], newvars['pos_y'])
        self.colour = (newvars['colour_r'], newvars['colour_g'], newvars['colour_b'])
        self.bounce = newvars['bounce']
        self.width = newvars['width']
        self.halfwidth = self.width / 2.0
        self.height = newvars['height']
        self.halfheight = self.height / 2.0
        self.maxdist = max(self.halfwidth, self.halfheight) + MAXDIST
        
        Obstacle.Update(self)
    
    def InsideObject(self, pos):
        return ((pos[0] > (self.pos[0] - self.halfwidth)) and (pos[0] < (self.pos[0] + self.halfwidth)) and (pos[1] > (self.pos[1] - self.halfheight)) and (pos[1] < self.pos[1] + self.halfheight))
    
    def GetResolved(self, pos):
        if pos == self.pos:  # If the position is at this obstacle's origin, shift it up a pixel to avoid divide-by-zero errors
            return self.GetResolved([pos[0], pos[1] - 1])
        
        # Where 'triangles' within the rectangle are referred to, imagine a rectangle with diagonals drawn between its vertices. The four triangles formed by this process are the ones referred to
        if pos[0] == self.pos[0]:  # If it's directly above the centre of the rectangle
            if pos[1] > self.pos[1]:
                return [pos[0], self.pos[1] + self.halfheight]
            else:
                return [pos[0], self.pos[1] - self.halfheight]
        elif pos[1] == self.pos[1]:  # If it's directly to one side of the centre of the rectangle
            if pos[0] > self.pos[0]:
                return [self.pos[0] + self.halfwidth, pos[1]]
            else:
                return [self.pos[0] - self.halfwidth, pos[1]]
        elif abs(float(pos[1] - self.pos[1]) / float(pos[0] - self.pos[0])) > (float(self.height) / float(self.width)):  # If it's in the upper or lower triangle of the rectangle
            return [pos[0], self.pos[1] + (self.halfheight * ((pos[1] - self.pos[1]) / abs(pos[1] - self.pos[1])))]  # Halfheight is multiplied by a normalised version of (pos[1] - self.pos[1]) - thus if (pos[1] - self.pos[1]) is negative, it should be subtracted as the point is in the upper triangle
        else:  # If it's in the left or right triangle of the rectangle
            return [self.pos[0] + (self.halfwidth * ((pos[0] - self.pos[0]) / abs(pos[0] - self.pos[0]))), pos[1]]
    
    def GetNormal(self, pos):
        if pos[1] < (self.pos[1] - self.halfheight):
            return [0, -1]
        elif pos[1] > (self.pos[1] + self.halfheight):
            return [0, 1]
        elif pos[0] < (self.pos[0] - self.halfwidth):
            return [-1, 0]
        elif pos[0] > (self.pos[0] + self.halfwidth):
            return [1, 0]
        else:
            vect = [pos[0] - self.pos[0], pos[1] - self.pos[1]]
            mag = magnitude(vect)
            return [vect[0] / mag, vect[1] / mag]
    
    def GetForceFactor(self, pos):
        nor = self.GetNormal(pos)
        
        if nor[0] == 0:
            if (pos[0] > (self.pos[0] - self.halfwidth)) and (pos[0] < (self.pos[0] + self.halfwidth)):
                r = abs(pos[1] - self.pos[1]) - self.halfheight
            else:
                return 0.0
        elif nor[1] == 0:
            if (pos[1] > (self.pos[1] - self.halfheight)) and (pos[1] < (self.pos[1] + self.halfheight)):
                r = abs(pos[0] - self.pos[0]) - self.halfheight
            else:
                return 0.0
        else:
            return 1.0
        
        if r <= 1.0:
            return 1.0
        
        return (1.0 / pow(float(r), 3.0))
    
    def CreateKeyframe(self, frame, pos = (None, None), colour = (None, None, None), bounce = None, width = None, height = None, interpolationtype = "linear"):
        CreateKeyframe(self.keyframes, frame, {'pos_x':pos[0], 'pos_y':pos[1], 'colour_r':colour[0], 'colour_g':colour[1], 'colour_b':colour[2], 'bounce':bounce, 'width':width, 'height':height, 'interpolationtype':interpolationtype})
    
    def ConsolidateKeyframes(self):
        ConsolidateKeyframes(self.keyframes, self.curframe, {'pos_x':self.pos[0], 'pos_y':self.pos[1], 'colour_r':self.colour[0], 'colour_g':self.colour[1], 'colour_b':self.colour[2], 'bounce':self.bounce, 'width':self.width, 'height':self.height})
    
    def SetWidth(self, newwidth):
        self.CreateKeyframe(self.curframe, width = newwidth)
    
    def SetHeight(self, newheight):
        self.CreateKeyframe(self.curframe, height = newheight)


class BoundaryLine(Obstacle):
    def __init__(self, pos, colour, bounce, normal):
        Obstacle.__init__(self, pos, colour, bounce)
        self.normal = normalise(normal)
        self.edgecontacts = []
        self.hascontacts = False
        self.curframe = 0
        self.CreateKeyframe(0, self.pos, self.colour, self.bounce, self.normal)
    
    def Draw(self, display):
        if not self.hascontacts:
            # W = display.get_width()
            # H = display.get_height()
            (W, H) = display.shape[1], display.shape[0]
            edgecontacts = []  # Where the line touches the screen edges
            
            if self.normal[0] == 0.0:
                edgecontacts = [[0, self.pos[1]], [W, self.pos[1]]]
            
            elif self.normal[1] == 0.0:
                edgecontacts = [[self.pos[0], 0], [self.pos[0], H]]
            
            else:
                pdotn = (self.pos[0] * self.normal[0]) + (self.pos[1] * self.normal[1])
                reciprocaln0 = (1.0 / self.normal[0])
                reciprocaln1 = (1.0 / self.normal[1])
                
                # Left-hand side of the screen
                pointl = [0, 0]
                pointl[1] = pdotn * reciprocaln1
                if (pointl[1] >= 0) and (pointl[1] <= H):
                    edgecontacts.append(pointl)
                
                # Top of the screen
                pointt = [0, 0]
                pointt[0] = pdotn * reciprocaln0
                if (pointt[0] >= 0) and (pointt[0] <= W):
                    edgecontacts.append(pointt)
                
                # Right-hand side of the screen
                pointr = [W, 0]
                pointr[1] = (pdotn - (W * self.normal[0])) * reciprocaln1
                if (pointr[1] >= 0) and (pointr[1] <= H):
                    edgecontacts.append(pointr)
                
                # Bottom of the screen
                pointb = [0, H]
                pointb[0] = (pdotn - (H * self.normal[1])) * reciprocaln0
                if (pointb[0] >= 0) and (pointb[0] <= W):
                    edgecontacts.append(pointb)

            self.edgecontacts = edgecontacts
            self.hascontacts = True
        
        # pygame.draw.aalines(display, self.colour, True, self.edgecontacts)
        # cv.Line(display, (int(self.edgecontacts[0][0]), int(self.edgecontacts[0][1])), (int(self.edgecontacts[1][0]), int(self.edgecontacts[1][1])), self.colour, lineType=cv.CV_AA)
        cv2.line(display, (int(self.edgecontacts[0][0]), int(self.edgecontacts[0][1])), (int(self.edgecontacts[1][0]), int(self.edgecontacts[1][1])), self.colour)
    
    def Update(self):
        newvars = InterpolateKeyframes(self.curframe, {'pos_x':self.pos[0], 'pos_y':self.pos[1], 'colour_r':self.colour[0], 'colour_g':self.colour[1], 'colour_b':self.colour[2], 'bounce':self.bounce, 'normal_x':self.normal[0], 'normal_y':self.normal[1]}, self.keyframes)
        self.pos = (newvars['pos_x'], newvars['pos_y'])
        self.colour = (newvars['colour_r'], newvars['colour_g'], newvars['colour_b'])
        self.bounce = newvars['bounce']
        oldnormal = self.normal[:]
        self.normal = [newvars['normal_x'], newvars['normal_y']]
        if self.normal != oldnormal:
            self.hascontacts = False
        
        Obstacle.Update(self)
    
    def OutOfRange(self, pos):
        return (self.GetDist(pos) > MAXDIST)
    
    def InsideObject(self, pos):
        return (((float(pos[0] - self.pos[0]) * self.normal[0]) + (float(pos[1] - self.pos[1]) * self.normal[1])) <= 0.0)
    
    def GetResolved(self, pos):
        if pos == self.pos:  # If the position is at this obstacle's origin, shift it up a pixel to avoid divide-by-zero errors
            return self.GetResolved([pos[0], pos[1] - 1])
        
        dist = abs(self.GetDist(pos))
        vec = [dist * self.normal[0], dist * self.normal[1]]
        
        return [pos[0] + vec[0], pos[1] + vec[1]]
    
    def GetNormal(self, pos):
        return self.normal
    
    def GetDist(self, pos):
        v = [float(pos[0] - self.pos[0]), float(pos[1] - self.pos[1])]
        return (v[0] * self.normal[0]) + (v[1] * self.normal[1])
    
    def GetForceFactor(self, pos):
        r = self.GetDist(pos)
        
        if r <= 1.0:
            return 1.0
        
        return (1.0 / pow(r, 3.0))
    
    def CreateKeyframe(self, frame, pos = (None, None), colour = (None, None, None), bounce = None, normal = [None, None], interpolationtype = "linear"):
        if (normal != [None, None]) and (abs(magnitudesquared(normal) - 1.0) >= 0.3):
            normal = normalise(normal)
        CreateKeyframe(self.keyframes, frame, {'pos_x':pos[0], 'pos_y':pos[1], 'colour_r':colour[0], 'colour_g':colour[1], 'colour_b':colour[2], 'bounce':bounce, 'normal_x':normal[0], 'normal_y':normal[1], 'interpolationtype':interpolationtype})
    
    def ConsolidateKeyframes(self):
        ConsolidateKeyframes(self.keyframes, self.curframe, {'pos_x':self.pos[0], 'pos_y':self.pos[1], 'colour_r':self.colour[0], 'colour_g':self.colour[1], 'colour_b':self.colour[2], 'bounce':self.bounce, 'normal_x':self.normal[0], 'normal_y':self.normal[1]})
    
    def SetNormal(self, newnormal):
        self.CreateKeyframe(self.curframe, normal = newnormal)

def main():
    # screen = cv.CreateImage((800,600), 8, 3)
    screen = np.zeros((600, 800, 3), np.uint8)
    windowname = "Particles demo"
    cv2.namedWindow(windowname)
    test = ParticleEffect(screen, (0, 0), (800, 600))
    testgrav = test.CreatePointGravity(strength = 1.0, pos = (500, 380))
    testgrav.CreateKeyframe(300, strength = 10.0, pos = (0, 0))
    testgrav.CreateKeyframe(450, strength = 10.0, pos = (40, 40))
    testgrav.CreateKeyframe(550, strength = -2.0, pos = (600, 480))
    testgrav.CreateKeyframe(600, strength = -20.0, pos = (600, 0))
    testgrav.CreateKeyframe(650, strength = 1.0, pos = (500, 380))
    anothertestgrav = test.CreateDirectedGravity(strength = 0.04, direction = [1, 0])
    anothertestgrav.CreateKeyframe(300, strength = 1.0, direction = [-0.5, 1])
    anothertestgrav.CreateKeyframe(600, strength = 1.0, direction = [1.0, -0.1])
    anothertestgrav.CreateKeyframe(650, strength = 0.04, direction = [1, 0])
    testsource = test.CreateSource((10, 10), initspeed = 5.0, initdirection = 2.35619449, initspeedrandrange = 2.0, initdirectionrandrange = 1.0, particlesperframe = 5, particlelife = 125, drawtype = DRAWTYPE_SCALELINE, colour = (255, 255, 255), length = 10.0)
    # testsource = test.CreateSource((10, 10), initspeed = 5.0, initdirection = 2.35619449, initspeedrandrange = 2.0, initdirectionrandrange = 1.0, particlesperframe = 5, particlelife = 125, drawtype = DRAWTYPE_LINE, colour = (255, 255, 255), length = 10.0)
    # testsource = test.CreateSource((10, 10), initspeed = 5.0, initdirection = 2.35619449, initspeedrandrange = 2.0, initdirectionrandrange = 1.0, particlesperframe = 5, particlelife = 125, drawtype = DRAWTYPE_POINT, colour = (255, 255, 255), length = 10.0)
    # testsource = test.CreateSource((10, 10), initspeed = 5.0, initdirection = 2.35619449, initspeedrandrange = 2.0, initdirectionrandrange = 1.0, particlesperframe = 5, particlelife = 125, drawtype = DRAWTYPE_CIRCLE, radius = 20, colour = (255, 255, 255), length = 10.0)
    # testsource = test.CreateSource((10, 10), initspeed = 5.0, initdirection = 2.35619449, initspeedrandrange = 2.0, initdirectionrandrange = 1.0, particlesperframe = 5, particlelife = 125, drawtype = DRAWTYPE_BUBBLE, radius = 3, colour = (255, 255, 255), length = 10.0)
    #star = cv2.imread("Star.png")
    # testsource = test.CreateSource((10, 10), initspeed = 5.0, initdirection = 2.35619449, initspeedrandrange = 2.0, initdirectionrandrange = 1.0, particlesperframe = 5, particlelife = 125, drawtype = DRAWTYPE_IMAGE, colour = (255, 0, 0), length = 10.0, image=star)
    testsource.CreateParticleKeyframe(50, colour = (0, 255, 0), length = 10.0)
    testsource.CreateParticleKeyframe(75, colour = (255, 255, 0), length = 10.0)
    testsource.CreateParticleKeyframe(100, colour = (0, 255, 255), length = 10.0)
    testsource.CreateParticleKeyframe(125, colour = (0, 0, 0), length = 10.0)
    maxframe = 1000
    # maxframe = -1
    i = 0
    while (i<maxframe and maxframe != -1) or maxframe == -1:
        i += 1
        # for event in pygame.event.get():
        #   if event.type == pygame.QUIT:
        k = cv2.waitKey(30)
        if k == 27:
            sys.exit()
        # screen.fill((0, 0, 0))
        # cv.Zero(screen)
        screen[:] = 0
        test.Update()
        test.Redraw()
        # pygame.display.update()
        cv2.imshow(windowname, screen)
        # clock.tick(20)    
        
## Begin testing code
if __name__ == '__main__':
    main()
