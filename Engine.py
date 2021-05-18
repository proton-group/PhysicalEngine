import numpy as np 
from math import sin, cos
class body:
    def __init__(self):
        self.pos = []
        self.time = 0
        self.speed = 0
        self.pcollision = False
        self.rot_check = False

class physics:
    def __init__(self):
        self.g = 9.8
        self.timespeed = 1
        self.op_precision = 5
        self.ang = 0

    def rot_direction_chooser(self, obj):
        if obj.pcollision != False and obj.pcollision != True and obj.rot_check == False:
                cpoint = obj.pcollision
                center = self.mass_center(obj.pos)
                if center[1] > cpoint[1]:
                    return "right"
                if center[1] < cpoint[1]:
                    return "left"
                obj.rot_check = True
        else:
            return None
            
    def mass_center(self, points):
        sumpoint_x, sumpoint_y = 0, 0
        for point in points:
            sumpoint_x += point[0]
            sumpoint_y += point[1]
        
        return (sumpoint_x/len(points), sumpoint_y/len(points))

    def set_ang(self, ang):
        self.ang = ang
    def remove_ang(self, ang):        
        self.ang = 0
    def rotation(self, direction, obj, ang): #для левого поворота ументшать угл, а не менять знак
        if obj.pcollision != False and obj.pcollision != True:
            export = []
            if direction == "left":
                ang += self.ang
            if direction == "right":
                ang -= self.ang
            for point in obj.pos:
                r_point = (point[0] - obj.pcollision[0], point[1] - obj.pcollision[1])
                export.append(((r_point[0] * cos(ang) - r_point[1] * sin(ang))+obj.pcollision[0], (r_point[0] * sin(ang) + r_point[1] * cos(ang))+obj.pcollision[1]))
            obj.pos = export

    def setGravConst(self, g):
        self.g = g

    def setTimeSpeed(self, speed): #without this use QTimer
        self.timespeed = speed
        
    def timeReset(self, obj):
        obj.time = 0
        
    def settime(self, time, obj):
        obj.time = time * self.timespeed

    def gravity(self, obj):
        newpos = []
        for point in obj.pos:
            newpos.append((point[0], point[1] + obj.speed * obj.time * (self.g*obj.time**2)/2))
        obj.pos = newpos
        obj.speed = self.g*obj.time
    
    def check_collision(self, f_archive, s_archive, t_archive):
        self.check = True
        for id_a in f_archive:
            for id_b in s_archive:
                if id_a.pos != id_b.pos:
                    if self.prop(id_a, id_b.pos):
                        pass
                    else:
                        self.check = False
                        break

            for prop_pos in t_archive:
                if id_a.pos != prop_pos:
                    if self.prop(id_a, prop_pos):
                        pass
                    else:
                        self.check = False
                        self.rotation(self.rot_direction_chooser(id_a), id_a, self.ang)
                        break

            if self.check:
                self.settime(0.5, id_a)
                self.gravity(id_a)
            else:
                #self.gravity(id_a)
                pass
            self.check = True

    def prop(self, obj_a, pos_b): #rotation, numpy for phis
        def overlap(apoints, bpoints):
            return (apoints[0] <= bpoints[0] + self.op_precision and apoints[0] >= bpoints[0] - self.op_precision) and (apoints[1] <= bpoints[1] + self.op_precision and apoints[1] >= bpoints[1] - self.op_precision)

        check = True
        for apoint in obj_a.pos:
            for bpoint in pos_b:
                if overlap(apoint, bpoint):
                    self.add_rotation_object(obj_a, apoint)
                    check = False
        return check

    def add_rotation_object(self, body, cpoint):
        if body.pcollision == False:
            body.pcollision = cpoint
        else:
            if body.pcollision != cpoint:
                body.pcollision = True
