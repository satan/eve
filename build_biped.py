import c4d
from c4d import documents as docs
from c4d import utils
from c4d import gui
import math
import itertools

###
global doc
global Tracer
global Constraint
global Circle
global AlignSpline
global IKTag
global null
global ik_hierarchy
global ctrl_hierarchy
global visuals_hierarchy
global visuals_tags
global Directions
global Trees
global Index
global IndexName
global TreeBranchDepth
global body_controllers
global leg_controllers
global GroupTopBody
#
doc = c4d.documents.GetActiveDocument()
Tracer = 1018655
Constraint = 1019364
Circle = 5181
AlignSpline = 5699
IKTag = 1019561
null = 5140
#
GroupTopBody = ['Spine2_CTRL', 'Neck_CTRL', 'Head_CTRL', 'Spine1_CTRL', 'Hips_CTRL', 'RightShoulder_CTRL', 'LeftShoulder_CTRL']
#
leg_controllers = [['Hips', 'UpLeg', 40], ['Spine2','Breast',10]]
#
Directions = ['Left','Right']
Trees = ['Foot', 'Arm']
Index = ['Toe', 'Hand']
IndexName = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
TreeBranchDepth = 4 #Tip of Fingers
#
body_controllers = [['Root_Controls', 'Hips', 60],['Hips', 'Spine', 50],['Root_Controls', 'Spine1', 55],['Root_Controls', 'Spine2', 60],['Root_Controls','Neck',35],['Root_Controls','Head',30]]
#
hierarchy = [['Root', 'Hips', (0,305,0),(0,0,0),(0,0,0)],
['Hips', 'Spine',(0,25,-12),(0,0,0),(0,19,0)],
['Spine', 'Spine1',(0,34,8),(0,0,0),(0,-16.5,0)],
['Spine1', 'Spine2',(0,25,6),(0,0,0),(0,0,0)],
['Spine2', 'Neck',(0,35,3),(0,0,0),(0,20,0)],
['Neck', 'Head',(0,28.5,0.5),(0,0,0),(0,0,0)],
['Head', 'HeadTop_End',(0,48.5,-14.5),(0,0,0),(0,0,0)],
['Head', 'Jaw',(0,0.5,-28.5),(0,0,0),(0,0,0)],
['Spine2', 'LeftShoulder',(27,27.5,11),(0,0,0),(0,-1,0)],
['LeftShoulder', 'LeftArm',(26.5,-1.5,0.5),(0,0,0),(0,0,0)],
['LeftArm', 'LeftForeArm',(70,0,0),(0,0,0),(0,0,0)],
['LeftForeArm', 'LeftHand',(62,0,0),(0,0,0),(88.5,91,7)],

['LeftHand', 'LeftHandThumb1',(-9,8,-2),(0,0,0),(-99,-56,-148)],
['LeftHandThumb1', 'LeftHandThumb2',(0,0,-7),(0,0,0),(3,0,7)],
['LeftHandThumb2', 'LeftHandThumb3',(0,0,-7),(0,0,0),(3,0,7)],
['LeftHandThumb3', 'LeftHandThumb4',(0,0,-7),(0,0,0),(3,0,7)],
['LeftHand', 'LeftHandIndex1',(-9,28,0),(0,0,0),(0,-90,0)],
['LeftHandIndex1', 'LeftHandIndex2',(-1.5,0,-8),(0,0,0),(0,0,0)],
['LeftHandIndex2', 'LeftHandIndex3',(-1,0.5,-7.5),(0,0,0),(0,0,0)],
['LeftHandIndex3', 'LeftHandIndex4',(-0.5,0,-6),(0,0,0),(0,90,4.5)],
['LeftHand', 'LeftHandMiddle1',(-3,30,1),(0,0,0),(0,-90,0)],
['LeftHandMiddle1', 'LeftHandMiddle2',(-1,0,-8.5),(0,0,0),(0,0,0)],
['LeftHandMiddle2', 'LeftHandMiddle3',(-1,0,-7.5),(0,0,0),(-3,0,0)],
['LeftHandMiddle3', 'LeftHandMiddle4',(0,0,-6),(0,0,0),(0,90,0)],
['LeftHand', 'LeftHandRing1',(2,30,0.5),(0,0,0),(0,-90,0)],
['LeftHandRing1', 'LeftHandRing2',(-1,0,-8),(0,0,0),(0,0,0)],
['LeftHandRing2', 'LeftHandRing3',(-0.5,-0.5,-6),(0,0,0),(-2,8,0)],
['LeftHandRing3', 'LeftHandRing4',(-0.5,0.5,-6),(0,0,0),(0,90,0)],
['LeftHand', 'LeftHandPinky1',(7,29,0.5),(0,0,0),(90,-82,90)],
['LeftHandPinky1', 'LeftHandPinky2',(-1,0,-6),(0,0,0),(-5,0,0)],
['LeftHandPinky2', 'LeftHandPinky3',(-0.5,0,-5.5),(0,0,0),(0,0,0)],
['LeftHandPinky3', 'LeftHandPinky4',(-0.5,0,-5),(0,0,0),(0,90,0)],

['Spine2', 'RightShoulder',(-27,27.5,11),(0,0,0),(0,-1,0)],
['RightShoulder', 'RightArm',(-26.5,-1.5,0.5),(0,0,0),(0,0,0)],
['RightArm', 'RightForeArm',(-70,0,0),(0,0,0),(0,0,0)],
['RightForeArm', 'RightHand',(-62,0,0),(0,0,0),(-88.5,91,-7)],

['RightHand', 'RightHandThumb1',(9,8,-2),(0,0,0),(99,-56,148)],
['RightHandThumb1', 'RightHandThumb2',(0,0,-7),(0,0,0),(-3,0,-7)],
['RightHandThumb2', 'RightHandThumb3',(0,0,-7),(0,0,0),(-3,0,-7)],
['RightHandThumb3', 'RightHandThumb4',(0,0,-7),(0,0,0),(-3,0,-7)],
['RightHand', 'RightHandIndex1',(9,28,0),(0,0,0),(0,-90,0)],
['RightHandIndex1', 'RightHandIndex2',(1.5,0,-8),(0,0,0),(0,0,0)],
['RightHandIndex2', 'RightHandIndex3',(1,0.5,-7.5),(0,0,0),(0,0,0)],
['RightHandIndex3', 'RightHandIndex4',(0.5,0,-6),(0,0,0),(0,90,-4.5)],
['RightHand', 'RightHandMiddle1',(3,30,1),(0,0,0),(0,-90,0)],
['RightHandMiddle1', 'RightHandMiddle2',(1,0,-8.5),(0,0,0),(0,0,0)],
['RightHandMiddle2', 'RightHandMiddle3',(1,0,-7.5),(0,0,0),(3,0,0)],
['RightHandMiddle3', 'RightHandMiddle4',(0,0,-6),(0,0,0),(0,90,0)],
['RightHand', 'RightHandRing1',(-2,30,0.5),(0,0,0),(0,-90,0)],
['RightHandRing1', 'RightHandRing2',(1,0,-8),(0,0,0),(0,0,0)],
['RightHandRing2', 'RightHandRing3',(0.5,-0.5,-6),(0,0,0),(2,8,0)],
['RightHandRing3', 'RightHandRing4',(0.5,0.5,-6),(0,0,0),(0,90,0)],
['RightHand', 'RightHandPinky1',(-7,29,0.5),(0,0,0),(-90,-82,-90)],
['RightHandPinky1', 'RightHandPinky2',(1,0,-6),(0,0,0),(5,0,0)],
['RightHandPinky2', 'RightHandPinky3',(0.5,0,-5.5),(0,0,0),(0,0,0)],
['RightHandPinky3', 'RightHandPinky4',(0.5,0,-5),(0,0,0),(0,90,0)],

['Spine2', 'LeftBreast',(28,-10.5,-49),(0,0,0),(0,20,0)],
['Spine2', 'RightBreast',(-28,-10.5,-49),(0,0,0),(0,20,0)],

['Hips', 'LeftUpLeg',(26,-13,0),(0,0,0),(0,0,0)],
['LeftUpLeg', 'LeftLeg',(-6.5,-142,-13),(0,0,0),(0,0,0)],
['LeftLeg', 'LeftFoot',(7.5,-124,7.5),(0,0,0),(0,0,0)],
['LeftFoot', 'LeftToeBase',(4.6,-17,-1),(0,0,0),(0,0,0)],
['LeftToeBase', 'LeftToeThumb1',(-5,-5,-29),(0,0,0),(-5,16,0)],
['LeftToeThumb1', 'LeftToeThumb2',(0,0,-11.5),(0,0,0),(4,-23,0)],
['LeftToeThumb2', 'LeftToeThumb3',(0,0,-6.5),(0,0,0),(0,0,0)],
['LeftToeBase', 'LeftToeIndex1',(-1,-4,-36),(0,0,0),(0,11,0)],
['LeftToeIndex1', 'LeftToeIndex2',(0,0,-5.5),(0,0,0),(0,5.5,0)],
['LeftToeIndex2', 'LeftToeIndex3',(0,0,-4.5),(0,0,0),(0,-7,0)],
['LeftToeIndex3', 'LeftToeIndex4',(0,0,-3.5),(0,0,0),(0,0,0)],
['LeftToeBase', 'LeftToeMiddle1',(2,-3,-36),(0,0,0),(10.5,12,-3)],
['LeftToeMiddle1', 'LeftToeMiddle2',(0,0,-5),(0,0,0),(-10,-12,-2)],
['LeftToeMiddle2', 'LeftToeMiddle3',(0.7,-2,-5),(0,0,0),(0,0,0)],
['LeftToeMiddle3', 'LeftToeMiddle4',(0.3,-0.7,-3.3),(0,0,0),(0,0,0)],
['LeftToeBase', 'LeftToeRing1',(6,-4,-35),(0,0,0),(12.5,11,0)],
['LeftToeRing1', 'LeftToeRing2',(0,0,-5),(0,0,0),(0,0,0)],
['LeftToeRing2', 'LeftToeRing3',(0,0,-4.5),(0,0,0),(1,0,0)],
['LeftToeRing3', 'LeftToeRing4',(0,0,-3.5),(0,0,0),(-14,0,0)],
['LeftToeBase', 'LeftToePinky1',(9,-4,-36),(0,0,0),(22,6.5,0)],
['LeftToePinky1', 'LeftToePinky2',(0,0,-4),(0,0,0),(-0.5,11,0)],
['LeftToePinky2', 'LeftToePinky3',(0,0,-4),(0,0,0),(3,0,0)],
['LeftToePinky3', 'LeftToePinky4',(0,0,-3),(0,0,0),(-24.5,0,0)],

['Hips', 'RightUpLeg',(-26,-13,0),(0,0,0),(0,0,0)],
['RightUpLeg', 'RightLeg',(6.5,-142,-13),(0,0,0),(0,0,0)],
['RightLeg', 'RightFoot',(-7.5,-124,7.5),(0,0,0),(0,0,0)],
['RightFoot', 'RightToeBase',(-4.6,-17,-1),(0,0,0),(0,0,0)],
['RightToeBase', 'RightToeThumb1',(5,-5,-29),(0,0,0),(5,16,0)],
['RightToeThumb1', 'RightToeThumb2',(0,0,-11.5),(0,0,0),(-4,-23,0)],
['RightToeThumb2', 'RightToeThumb3',(0,0,-6.5),(0,0,0),(0,0,0)],
['RightToeBase', 'RightToeIndex1',(-1,-4,-36),(0,0,0),(0,11,0)],
['RightToeIndex1', 'RightToeIndex2',(0,0,-5.5),(0,0,0),(0,5.5,0)],
['RightToeIndex2', 'RightToeIndex3',(0,0,-4.5),(0,0,0),(0,-7,0)],
['RightToeIndex3', 'RightToeIndex4',(0,0,-3.5),(0,0,0),(0,0,0)],
['RightToeBase', 'RightToeMiddle1',(-2,-3,-36),(0,0,0),(-10.5,12,-3)],
['RightToeMiddle1', 'RightToeMiddle2',(0,0,-5),(0,0,0),(10,-12,-2)],
['RightToeMiddle2', 'RightToeMiddle3',(-0.7,-2,-5),(0,0,0),(0,0,0)],
['RightToeMiddle3', 'RightToeMiddle4',(-0.3,-0.7,-3.3),(0,0,0),(0,0,0)],
['RightToeBase', 'RightToeRing1',(-6,-4,-35),(0,0,0),(-12.5,11,0)],
['RightToeRing1', 'RightToeRing2',(0,0,-5),(0,0,0),(0,0,0)],
['RightToeRing2', 'RightToeRing3',(0,0,-4.5),(0,0,0),(-1,0,0)],
['RightToeRing3', 'RightToeRing4',(0,0,-3.5),(0,0,0),(14,0,0)],
['RightToeBase', 'RightToePinky1',(-9,-4,-36),(0,0,0),(-22,6.5,0)],
['RightToePinky1', 'RightToePinky2',(0,0,-4),(0,0,0),(0.5,11,0)],
['RightToePinky2', 'RightToePinky3',(0,0,-4),(0,0,0),(-3,0,0)],
['RightToePinky3', 'RightToePinky4',(0,0,-3),(0,0,0),(24.5,0,0)]]

ik_hierarchy = [['RightUpLeg', 'RightFoot', 'Root_Controls'],
['RightFoot', 'RightToeBase', 'RightUpLeg.Goal'],
['LeftUpLeg', 'LeftFoot', 'Root_Controls'],
['LeftFoot', 'LeftToeBase', 'LeftUpLeg.Goal'],
['LeftForeArm', 'LeftHand', 'Root_Controls'],
['RightForeArm', 'RightHand', 'Root_Controls']
]

ik_hierarchy_hands = [['LeftArm_CTRL', 'LeftHand_Visual', 'LeftShoulder_CTRL'],
['RightArm_CTRL', 'RightHand_Visual', 'RightShoulder_CTRL']
]

ctrl_hierarchy = [['Shoulder', 'Arm'],
['Arm', 'ForeArm'],
['ForeArm', 'Hand']]

#
visuals_hierarchy = [['LeftFoot','red',(28,-25,1),[(-9,-25,-65),(7.5,-25,-65),(25,-25,-55),(25,-25,-25.5),(7,-16,25),(-8,-16,25)]],
['RightFoot','blue',(-28,-25,1),[(9,-25,-65),(-7.5,-25,-65),(-25,-25,-55),(-25,-25,-25.5),(-7,-16,25),(8,-16,25)]],
['LeftHand','red',(-20,0,8),[(-12,-2,11),(11,0,11),(15,0,-11)]],
['RightHand','blue',(-180,410,5.5),[(12,-2,11),(-11,0,11),(-15,0,-11)]]]

visuals_tags = [['FingersTag',(0,0,0),[(0,0,0),(0,8,0),(0,10,1.5),(0,10,-1.5),(0,8,0)]]]

#
global pythontagcode

pythontagcode = '''
import c4d
from c4d import gui
import math
#Welcome to the world of Python
Directions = ['Left','Right']
IndexName = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']

def main():
	fingerdata = 0
	
	for dir in Directions:
		for finger in IndexName:
			finger_part = 1
			fingerdata = fingerdata + 2

			root_item = doc.SearchObject('Root_Controls')
			end_item = doc.SearchObject(dir+'Hand'+finger+str(finger_part)+'_CTRL')
			end_item_1 = doc.SearchObject(dir+'Hand'+finger+str(finger_part+1)+'_CTRL')
			end_item_2 = doc.SearchObject(dir+'Hand'+finger+str(finger_part+2)+'_CTRL')
			obj = doc.SearchObject("Root_Controls")

			if obj[c4d.ID_USERDATA,fingerdata] == 0:
				if 'Thumb' in finger:
					end_item[c4d.ID_BASEOBJECT_REL_ROTATION,c4d.VECTOR_Y] = end_item[c4d.ID_BASEOBJECT_REL_ROTATION,c4d.VECTOR_Y] / 2
					end_item_1[c4d.ID_BASEOBJECT_REL_ROTATION,c4d.VECTOR_Y] = end_item_1[c4d.ID_BASEOBJECT_REL_ROTATION,c4d.VECTOR_Y]
					end_item_2[c4d.ID_BASEOBJECT_REL_ROTATION,c4d.VECTOR_Y] = end_item_2[c4d.ID_BASEOBJECT_REL_ROTATION,c4d.VECTOR_Y]
				else:
					end_item[c4d.ID_BASEOBJECT_REL_ROTATION,c4d.VECTOR_Y] = end_item[c4d.ID_BASEOBJECT_REL_ROTATION,c4d.VECTOR_Y]
					end_item_1[c4d.ID_BASEOBJECT_REL_ROTATION,c4d.VECTOR_Y] = end_item_1[c4d.ID_BASEOBJECT_REL_ROTATION,c4d.VECTOR_Y]
					end_item_2[c4d.ID_BASEOBJECT_REL_ROTATION,c4d.VECTOR_Y] = end_item_2[c4d.ID_BASEOBJECT_REL_ROTATION,c4d.VECTOR_Y]
			else:
				if 'Thumb' in finger:
					end_item[c4d.ID_BASEOBJECT_REL_ROTATION,c4d.VECTOR_Y] = root_item[c4d.ID_USERDATA,fingerdata-1] / 2
					end_item_1[c4d.ID_BASEOBJECT_REL_ROTATION,c4d.VECTOR_Y] = root_item[c4d.ID_USERDATA,fingerdata-1]
					end_item_2[c4d.ID_BASEOBJECT_REL_ROTATION,c4d.VECTOR_Y] = root_item[c4d.ID_USERDATA,fingerdata-1]
				else:
					end_item[c4d.ID_BASEOBJECT_REL_ROTATION,c4d.VECTOR_Y] = root_item[c4d.ID_USERDATA,fingerdata-1]
					end_item_1[c4d.ID_BASEOBJECT_REL_ROTATION,c4d.VECTOR_Y] = root_item[c4d.ID_USERDATA,fingerdata-1]
					end_item_2[c4d.ID_BASEOBJECT_REL_ROTATION,c4d.VECTOR_Y] = root_item[c4d.ID_USERDATA,fingerdata-1]
'''
#
class Biped():
	

	def mergeObjects(self, objs, name):
		for o in objs:
			doc.InsertObject(o)
			o.ToggleBit(c4d.BIT_ACTIVE)
			o.GetBit(c4d.BIT_ACTIVE)

		c4d.CallCommand(16768)
		
		group = doc.GetActiveObject()
		group.SetName(name)

		result = group
		c4d.CallCommand(100004767)

		return result

	def groupObjects(self, objs, name, parent):

		obj_null = c4d.BaseObject(null)

		find_hips = doc.SearchObject('Hips')
		mg = find_hips.GetMg()
		obj_null.SetMg(mg)

		obj_null.SetName(name)
		doc.InsertObject(obj_null)

		find_parent = doc.SearchObject(parent)
		obj_null.InsertUnder(find_parent)

		for obj in objs:
			find_obj = doc.SearchObject(obj)
			mg = find_obj.GetMg()
			find_obj.InsertUnder(obj_null)
			find_obj.SetMg(mg)

	def Colorize(self, color):
		if color == 'red':
			return c4d.Vector(1,0,0)
		elif color == 'green':
			return c4d.Vector(0,1,0)
		elif color == 'blue':
			return c4d.Vector(0,0,1)

	def GenerateSpline(self, name, color, position, d_points):
		i = 0

		spline_product = c4d.SplineObject(len(d_points), 0)
		spline_product.SetName(name)
		spline_product[c4d.ID_BASEOBJECT_USECOLOR] = 2
		spline_product[c4d.ID_BASEOBJECT_COLOR] = self.Colorize(color)

		for coords in d_points:
			try:
				spline_vec = c4d.Vector(coords[0],coords[1],coords[2])
				spline_product.SetPoint(i, spline_vec)
			except IndexError:
				pass
			i = i + 1

		return spline_product

	def InsertNull(self, name):

		obj_null = c4d.BaseObject(null)
		obj_null.SetName(name)
		doc.InsertObject(obj_null)
	
	def InsertWireSphere(self, name, radius, color):

		sphere_points_array_x = self.MakeCircle(20, radius, 0, 'x')
		sphere_points_array_y = self.MakeCircle(20, radius, 0, 'y')
		sphere_points_array_z = self.MakeCircle(20, radius, 0, 'z')

		circle_spline_x = self.GenerateSpline(name, color, (0,0,0), sphere_points_array_x)
		circle_spline_y = self.GenerateSpline(name, color, (0,0,0), sphere_points_array_y)
		circle_spline_z = self.GenerateSpline(name, color, (0,0,0), sphere_points_array_z)

		list=[circle_spline_x, circle_spline_y, circle_spline_z]

		wireframe_circle = self.mergeObjects(list, name)

	def InsertWireTarget(self, name, radius, color):
		
		sphere_points_array_y = self.MakeCircle(20, radius, 0, 'y')
		sphere_points_array_y_inner = self.MakeCircle(20, radius - 5, 0, 'y')

		circle_spline_y = self.GenerateSpline(name, color, (0,0,0), sphere_points_array_y)
		circle_spline_y_inner = self.GenerateSpline(name, color, (0,0,0), sphere_points_array_y_inner)

		list=[circle_spline_y, circle_spline_y_inner]

		wireframe_circle = self.mergeObjects(list, name)

	def InsertSpineCircle(self, name, radius, color):
		
		sphere_points_array_y = self.MakeCircle(20, radius, 0, 'z')
		circle_spline_y = self.GenerateSpline(name, color, (0,0,0), sphere_points_array_y)
		list=[circle_spline_y]
		wireframe_circle = self.mergeObjects(list, name) #could be InsertObject

	def MakeCircle(self, points, radius, center, plane):

		res = []
		i = 0
		slice = 2 * math.pi / points;

		if plane == 'x':
			while i <= points:
				angle = slice * i
				newX = radius * math.cos(angle)
				newY = radius * math.sin(angle)
				p = (newX, newY, 0)
				res.append(p)
				i = i + 1
		elif plane == 'y':
			while i <= points:
				angle = slice * i
				newY = radius * math.cos(angle)
				newZ = radius * math.sin(angle)
				p = (0, newY, newZ)
				res.append(p)
				i = i + 1
		else:
			while i <= points:
				angle = slice * i
				newZ = radius * math.cos(angle)
				newX = radius * math.sin(angle)
				p = (newZ, 0, newX)
				res.append(p)
				i = i + 1
		return res

	def c4d_insert_ik(self, ik_parent, ik_target, group_parent):

		startObj = doc.SearchObject(ik_parent)
		endObj = doc.SearchObject(ik_target)
		
		ikTag = c4d.BaseTag(IKTag)
		startObj.InsertTag(ikTag)

		find_group_parent = doc.SearchObject(group_parent)
		IK_Goal = c4d.BaseObject(null)

		IK_Goal.SetName(ik_parent+'.Goal')
		doc.InsertObject(IK_Goal, parent = find_group_parent)

		ikTag[c4d.ID_CA_IK_TAG_TIP] = endObj
		ikTag[c4d.ID_CA_IK_TAG_TARGET] = IK_Goal

		if 'Leg' in ik_parent:
			IK_Pole = c4d.BaseObject(null)
			IK_Pole.SetName(ik_parent+'.Pole')
			dire =  ik_parent.rsplit('Up', 1)[0]
			
			find_group = doc.SearchObject(dire+'UpLeg.Goal')

			startObj = doc.SearchObject(ik_parent)
			endObj = doc.SearchObject(ik_target)

			doc.InsertObject(IK_Pole, parent = find_group)
			ikTag[c4d.ID_CA_IK_TAG_POLE] = IK_Pole

		ik_target_pos = doc.SearchObject(ik_target)
		mg = ik_target_pos.GetMg()
		IK_Goal.SetMg(mg)

	def c4d_insert_hand_ik(self, ik_parent, ik_target, group_parent):

		startObj = doc.SearchObject(ik_parent)
		endObj = doc.SearchObject(ik_target)
		groupObj = doc.SearchObject(group_parent)
		
		ikTag = c4d.BaseTag(IKTag)
		startObj.InsertTag(ikTag)

		find_group_parent = doc.SearchObject(group_parent)
		IK_Goal = c4d.BaseObject(null)

		IK_Goal.SetName(ik_parent+'.Goal')
		doc.InsertObject(IK_Goal, parent = find_group_parent)

		ikTag[c4d.ID_CA_IK_TAG_TIP] = endObj
		ikTag[c4d.ID_CA_IK_TAG_TARGET] = IK_Goal

		if 'Left' in ik_parent:
			ikTag[c4d.ID_CA_IK_TAG_POLE_AXIS] = 4
			ikTag[c4d.ID_CA_IK_TAG_POLE_TWIST] = 3.1415926535897931 # 180deg
		else:
			ikTag[c4d.ID_CA_IK_TAG_POLE_AXIS] = 1
			ikTag[c4d.ID_CA_IK_TAG_POLE_TWIST] = 0

		# if 'Leg' in ik_parent:
		# 	IK_Pole = c4d.BaseObject(null)
		# 	IK_Pole.SetName(ik_parent+'.Pole')
		# 	dire =  ik_parent.rsplit('Up', 1)[0]
			
		# 	find_group = doc.SearchObject(dire+'UpLeg.Goal')

		# 	startObj = doc.SearchObject(ik_parent)
		# 	endObj = doc.SearchObject(ik_target)

		# 	doc.InsertObject(IK_Pole, parent = find_group)
		# 	ikTag[c4d.ID_CA_IK_TAG_POLE] = IK_Pole

		ik_target_pos = doc.SearchObject(ik_target)
		mg = ik_target_pos.GetMg()
		IK_Goal.SetMg(mg)

	def c4d_insert_joint(self, joint_name, joint_parent, joint_length, position, scale, rotation, state):

		print 'Making Joint: '+ joint_name
		if state == 'actual':

			joint = c4d.BaseObject(1019362)
			joint.SetName(joint_name)
			end_item = doc.SearchObject(joint_name)
			end_vec = c4d.Vector(math.radians(rotation[0]),math.radians(rotation[1]),math.radians(rotation[2]))
			joint[c4d.ID_BASEOBJECT_REL_POSITION] =  c4d.Vector(position[0], position[1], position[2])
			joint[c4d.ID_BASEOBJECT_REL_ROTATION] =  end_vec
			doc.InsertObject(joint, parent = joint_parent)
			joint[c4d.ID_CA_JOINT_OBJECT_LENGTH] = joint_length

	def BuildBones(self):
		for parent, child, position, scale, rotation in hierarchy:
			p_item = doc.SearchObject(parent)
			self.c4d_insert_joint(child, p_item, 10, position, scale, rotation,'actual')

	def BuildLegIK(self):

		for ik_parent, ik_target, group_parent in ik_hierarchy:
			self.c4d_insert_ik(ik_parent, ik_target, group_parent)

	def BuildHandIK(self):

		for ik_parent, ik_target, group_parent in ik_hierarchy_hands:
			self.c4d_insert_hand_ik(ik_parent, ik_target, group_parent)

	def BuildVisuals(self):

		SplineNull = c4d.BaseObject(null)
		SplineNull.SetName('Root_Controls')
		doc.InsertObject(SplineNull)

		for name, color, position, points in visuals_hierarchy:

			find_tree = doc.SearchObject(name)
			mg = find_tree.GetMg()

			spline = self.GenerateSpline(name, color, mg, points)
			spline.SetName(name+'_Visual')
			doc.InsertObject(spline, parent = SplineNull)
			find_visual = doc.SearchObject(name+'_Visual')

			find_parent = doc.SearchObject(name)

			mg = find_parent.GetMg()
			find_visual.SetMg(mg)

	def insertConstraint(self, target,ctrl_label):

		constr_tag = c4d.BaseTag(Constraint)
		constr_tag[c4d.ID_CA_CONSTRAINT_TAG_PSR] = True
		constr_tag[10001] = ctrl_label
		corr_ik = doc.SearchObject(target)
		corr_ik.InsertTag(constr_tag)

	def insertTargetConstraint(self, target,ctrl_label):

		constr_tag = c4d.BaseTag(Constraint)
		constr_tag[c4d.ID_CA_CONSTRAINT_TAG_AIM] = True
		constr_tag[10001] = ctrl_label
		corr_ik = doc.SearchObject(target)
		corr_ik.InsertTag(constr_tag)

	def build_tree(self, tree_array, direction, tree, index, ext_name):

		goal_name = direction+tree

		if 'Foot' in tree:

			find_par = doc.SearchObject(direction+tree+'.Goal')
			mg = find_par.GetMg()
			tree_name = 'Root_'+direction+tree+index+'s'
			self.InsertNull(tree_name)
			find_tree = doc.SearchObject(tree_name)
			find_tree.SetMg(mg)
		else:
			tree_name = 'Root_'+direction+index+'Fingers'
			self.InsertNull(tree_name)

		tree_set = []
		for target in tree_array: tree_set.append(target[1])
		tree_set.insert(0,direction+index+IndexName[0]+'1') 
		ThumbRemoveLastCTRL = direction+index+IndexName[0]+str(TreeBranchDepth-1)

		if 'Foot' in tree:
			tree_set = [ x for x in tree_set if (str(TreeBranchDepth) not in x and ThumbRemoveLastCTRL not in x) ]
		else:
			tree_set = [ x for x in tree_set if (str(TreeBranchDepth) not in x ) ]

		p = 0
		for target in tree_set:
			i = 0
			parent_1 = tree_set[p]

			for name, position, points in visuals_tags:
				
				if p == 0 or "1" in target:
					ctrl_label = self.GenerateSpline(target+'_CTRL', 'green', position, points)
					parent_1 = tree_name
					p_item = doc.SearchObject(target)
					parent_find = doc.SearchObject(parent_1)
					child = doc.SearchObject(name)

					doc.InsertObject(ctrl_label, parent = parent_find)

					mg = p_item.GetMg()
					ctrl_label.SetMg(mg)

					self.insertConstraint(target, ctrl_label)

				else:
					ctrl_label = self.GenerateSpline(target+'_CTRL', 'green', position, points)
					parent_1 = tree_set[p-1]
					p_item = doc.SearchObject(target)
					parent_find = doc.SearchObject(parent_1+'_CTRL')
					child = doc.SearchObject(name)
					
					doc.InsertObject(ctrl_label, parent = parent_find)

					mg = p_item.GetMg()
					ctrl_label.SetMg(mg)

					self.insertConstraint(target, ctrl_label)

				i = i + 1

			p = p + 1

		if 'Foot' in tree:
			find_root_group = doc.SearchObject(tree_name)
			mg = find_root_group.GetMg()
			find_goal = doc.SearchObject(goal_name+'.Goal')
			find_root_group.InsertUnder(find_goal)
			find_root_group.SetMg(mg)

			find_ext = doc.SearchObject(ext_name+'.Goal')
			mg = find_ext.GetMg()
			find_visual = doc.SearchObject(goal_name+'_Visual')
			find_ext.InsertUnder(find_visual)
			find_ext.SetMg(mg)
		else:
			find_root_group = doc.SearchObject(tree_name)
			mg = find_root_group.GetMg()

			find_ext = doc.SearchObject(ext_name+'.Goal')
			find_root_group.InsertUnder(find_ext)
			find_root_group.SetMg(mg)
			
			root_visual = tree_name.replace('Root_', '').replace('Fingers', '_Visual')
			find_root_group = doc.SearchObject(root_visual)
			
			find_ext = doc.SearchObject(ext_name+'.Goal')
			mg = find_ext.GetMg()
			find_ext.InsertUnder(find_root_group)
			find_ext.SetMg(mg)

	def BuildEnds(self):
		for tree in Trees:
			
			if tree == 'Foot':
				index = Index[0]
				for direction in Directions:
					if direction == 'Left':
						#print 'tree_foot_left'
						tree_array = hierarchy[63:len(hierarchy)-23]
					else:
						#print 'tree_foot_right'
						tree_array = hierarchy[len(hierarchy)-18:len(hierarchy)]
					
					self.build_tree(tree_array, direction, tree, index, direction+'UpLeg')

			elif tree == 'Arm':
				index = Index[1]
				for direction in Directions:
					if direction == 'Left':
						tree_array = hierarchy[13:32]
					else:
						tree_array = hierarchy[37:56]

					self.build_tree(tree_array, direction, tree, index, direction+'ForeArm')

	def build_controllers(self):

		i = 0
		for cont in ctrl_hierarchy:
			for dir in Directions:

				if dir == 'Left':
					color = 'red'
				else:
					color = 'blue'
				if 'Shoulder' in dir+cont[0]:
					ctrl_sphere = self.InsertWireTarget(dir+cont[0]+'_CTRL',30,color)
					
					find_ctrl = doc.SearchObject(dir+cont[0]+'_CTRL')
					self.insertConstraint(dir+'Shoulder',find_ctrl)
				else:
					ctrl_sphere = self.InsertWireSphere(dir+cont[0]+'_CTRL',20,color)

				find_ctrl_sphere = doc.SearchObject(dir+cont[0]+'_CTRL')

				find_joint = doc.SearchObject(dir+cont[0])
				mg = find_joint.GetMg()
				find_ctrl_sphere.SetMg(mg)

				# Controller Grouping
				find_root_ctrl = doc.SearchObject('Root_Controls')
				mg = find_ctrl_sphere.GetMg()
				find_ctrl_sphere.InsertUnder(find_root_ctrl)
				find_ctrl_sphere.SetMg(mg)

				i = i + 1
		for cont in ctrl_hierarchy:
			for dir in Directions:

				find_ctrl_sphere = doc.SearchObject(dir+cont[1]+'_CTRL')
				find_parent = doc.SearchObject(dir+cont[0]+'_CTRL')

				if find_ctrl_sphere is not None:
					mg = find_ctrl_sphere.GetMg()
					find_ctrl_sphere.InsertUnder(find_parent)
					find_ctrl_sphere.SetMg(mg)

				if 'ForeArm' in dir+cont[0]:
					find_visual = doc.SearchObject(dir+cont[1]+'_Visual')
					mg = find_visual.GetMg()
					find_ctrl_sphere = doc.SearchObject(dir+'ForeArm_CTRL')
					find_visual.InsertUnder(find_ctrl_sphere)
					find_visual.SetMg(mg)

		for dir in Directions:
			find_ctrl = doc.SearchObject(dir+'ForeArm_CTRL')
			self.insertConstraint(dir+'ForeArm',find_ctrl)

			find_ctrl = doc.SearchObject(dir+'Arm_CTRL')
			self.insertConstraint(dir+'Arm',find_ctrl)

			find_ctrl = doc.SearchObject(dir+'Hand_Visual')
			self.insertConstraint(dir+'Hand',find_ctrl)

	def build_spine_controllers(self, array):
		i = 0
		for parent, child, radius in array:
			ctrl = '_CTRL'

			if 'Root' in parent:
				find_root_ctrl = doc.SearchObject(parent)
			else:
				find_root_ctrl = doc.SearchObject(parent+ctrl)

			ctrl_sphere = self.InsertSpineCircle(child+ctrl,radius,'green')
			find_ctrl_circle = doc.SearchObject(child+ctrl)
			find_target_joint = doc.SearchObject(child)
			mg = find_target_joint.GetMg()
			find_ctrl_circle.InsertUnder(find_root_ctrl)
			find_ctrl_circle.SetMg(mg)
			#add constraint
			find_ctrl = doc.SearchObject(child+ctrl)
			self.insertConstraint(child,find_ctrl)

			i = i + 1

	def build_leg_controllers(self, array):
		for parent, child, radius in array:

			for dir in Directions:
				ctrl = '_CTRL'


				find_root_ctrl = doc.SearchObject(parent+ctrl)

				if dir == 'Left':
					color = 'red'
				else:
					color = 'blue'

				if 'Breast' in child:
					ctrl_sphere = self.InsertWireSphere(dir+child+ctrl,radius,color)
				else:
					ctrl_sphere = self.InsertSpineCircle(dir+child+ctrl,radius,color)
				find_ctrl_circle = doc.SearchObject(dir+child+ctrl)
				#print dir+child+ctrl
				find_target_joint = doc.SearchObject(dir+child)
				mg = find_target_joint.GetMg()
				find_ctrl_circle.InsertUnder(find_root_ctrl)
				find_ctrl_circle.SetMg(mg)
				#add constraint
				find_ctrl = doc.SearchObject(dir+child+ctrl)
				self.insertConstraint(dir+child,find_ctrl)

	def build_finger_controllers(self):

		for dir in Directions:
			obj = doc.SearchObject('Root_Controls')
			
			for finger in IndexName:
				
				#userdata
				bc = c4d.GetCustomDataTypeDefault(c4d.DTYPE_REAL)
				bc[c4d.DESC_NAME] = dir+finger+'Finger'
				bc[c4d.DESC_UNIT] = c4d.DESC_UNIT_DEGREE
				bc[c4d.DESC_MIN] = 0
				bc[c4d.DESC_MAX] = math.radians(360)
				bc[c4d.DESC_STEP] = math.radians(1)
				bc[c4d.DESC_CUSTOMGUI] = c4d.CUSTOMGUI_REALSLIDER
				element1 = obj.AddUserData(bc)
				obj[element1] = 0
				
				# Assign Tick
				bc = c4d.GetCustomDatatypeDefault(c4d.DTYPE_BOOL) # Create default container
				bc[c4d.DESC_NAME] = dir+finger+'Controlled'
				# Rename the entry
				element2 = obj.AddUserData(bc)
				# Add userdata container
				obj[element2] = 0

	def BuildPoles(self):
		for dire in Directions:
			find_pole = doc.SearchObject(dire+'UpLeg.Pole')
			splineTag = c4d.BaseTag(AlignSpline)
			find_ctrl = doc.SearchObject(dire+'UpLeg_CTRL')
			splineTag[c4d.ALIGNTOSPLINETAG_LINK] = find_ctrl
			if dire == 'Left':
				splineTag[c4d.ALIGNTOSPLINETAG_POSITION] = 0.8
			else:
				splineTag[c4d.ALIGNTOSPLINETAG_POSITION] = 0.7
			find_pole.InsertTag(splineTag)

	def __init__(self):

		nul = c4d.BaseObject(null)
		nul.SetName('Root')
		doc.InsertObject(nul)

		self.BuildBones()
		self.BuildLegIK()
		self.BuildVisuals()
		self.BuildEnds()
		self.build_controllers()
		self.build_spine_controllers(body_controllers)
		self.build_leg_controllers(leg_controllers)
		self.BuildHandIK()
		# parenting
		merged_top_body_group = self.groupObjects(GroupTopBody, 'TopBody', 'Root_Controls')
		find_head = doc.SearchObject('Head_CTRL')
		find_neck = doc.SearchObject('Neck_CTRL')

		mg = find_head.GetMg()
		find_head.InsertUnder(find_neck)
		find_head.SetMg(mg)

		self.BuildPoles()
		self.build_finger_controllers()
		pythontag = c4d.BaseTag(c4d.Tpython)

		rC = doc.SearchObject('Root_Controls')
		rC.InsertTag(pythontag)
		pythontag[c4d.TPYTHON_CODE] = pythontagcode


Biped()