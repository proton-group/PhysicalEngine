#itertools, product
#import numpy as np 
from math import sin, cos, sqrt
class body:
    def __init__(self):
        self.pos = []
        self.time = 0
        self.speed = 0
        self.pcollision = False
        self.rot_check = False
        self.cheking = False
        self.ang = 0
        self.hitbox = () # xmin, xmax, ymin, ymax

class physics:
    def __init__(self):
        self.g = 9.8
        self.timespeed = 1
        self.op_precision = 10 #8
        self.rot_speed = 0.001
        self.update_list = []
        self.block = 0

    def rot_direction_chooser(self, obj):
        if obj.pcollision != False and obj.pcollision != True and obj.rot_check == False:
                cpoint = obj.pcollision
                center = self.mass_center(obj.pos)
                if center[0] > cpoint[0]:
                    return "right"
                if center[0] < cpoint[0]:
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

    def rotation(self, direction, obj, archive): #для левого поворота ументшать угол, а не менять знак, чекать коллизию во время поворота
        if obj.pcollision != False and obj.pcollision != True:
            export = []
            if direction == "right":
                obj.ang = obj.ang + self.rot_speed
            if direction == "left":
                obj.ang = obj.ang - self.rot_speed
            for point in obj.pos:
                r_point = (point[0] - obj.pcollision[0], point[1] - obj.pcollision[1])
                export.append(((r_point[0] * cos(obj.ang) - r_point[1] * sin(obj.ang))+obj.pcollision[0], (r_point[0] * sin(obj.ang) + r_point[1] * cos(obj.ang))+obj.pcollision[1]))
            self.prop(obj, archive)
            obj.pos = export
            #self.rotation(direction, obj)

    def setGravConst(self, g):
        self.g = g

    def setTimeSpeed(self, speed): #without this use QTimer
        self.timespeed = speed
        
    def timeReset(self, obj):
        obj.time = 0
        
    def settime(self, time, obj):
        obj.time = time * self.timespeed

    def gravity(self, obj, archive):
        newpos = []
        collision = False
        coordinate = self.minmax(obj.pos)
        archeck = []
        for point in obj.pos:
            #корректируем перемещение по коллизии
            newpos.append((point[0], point[1] + obj.speed * obj.time * (self.g*obj.time**2)/2))
            archeck = archeck + [(point[0], point[1] + dots) for dots in range(int(obj.speed * obj.time * (self.g*obj.time**2)/2))] 
        if archeck != []:
            testbody = body()
            testbody.pos = archeck
            for ident in archive:
                if ident != obj:
                    if self.prop_check(testbody, ident):
                        if testbody.pcollision != False and testbody.pcollision != True:
                            newpos = []
                            for point in obj.pos:
                                newpos.append((point[0], point[1] + testbody.pcollision[1] - coordinate[3]))
                            obj.pcollision = testbody.pcollision
                            collision = True
                        break              
        if collision:
            newpos = []
            for point in obj.pos:  
                newpos.append((point[0], point[1] + testbody.pcollision[1] - coordinate[3]))
        obj.pos = newpos
        obj.speed = self.g*obj.time
    
    def check_collision(self, f_archive, s_archive):
        self.check = True
        count = 0
        #for x,y in idpoint(f_archive, s_archive):
        for id_a, id_b in self.idpoint(f_archive, s_archive):
            if self.prop_check(id_a, id_b):
                break
        for id_a in f_archive:
            if id_a.pcollision == False:
                self.settime(0.5, id_a)
                self.gravity(id_a, s_archive)

                
    def prop(self, obj_a, obj_b): #rotation, numpy for phis
        def overlap(apoints, bpoints):
            return (apoints[0] <= bpoints[0] + self.op_precision and apoints[0] >= bpoints[0] - self.op_precision) and (apoints[1] <= bpoints[1] + self.op_precision and apoints[1] >= bpoints[1] - self.op_precision)
        hitbox_a = self.minmax(obj_a.pos) # xmin, xmax, ymin, ymax
        hitbox_b = self.minmax(obj_b.pos)
        check = True
        if self.check_hitbox(hitbox_a, hitbox_b):
            for apoint in obj_a.pos:
                for bpoint in obj_b.pos:
                    if overlap(apoint, bpoint):
                        self.add_rotation_object(obj_a, apoint)
                        check = False
        return check

    def add_rotation_object(self, body, cpoint):
        if body.pcollision == False:
            body.pcollision = cpoint
        else:
            if body.pcollision != cpoint and body.pcollision != True:
                if self.norma(body.pcollision, cpoint) < self.norma(cpoint, self.mass_center(body.pos)):
                    body.pcollision = cpoint 
                else:    
                    body.pcollision = True

    def moution(self, car_part, direction):
        newpos = []
        if direction == "up" and self.block < 3:
            for point in car_part.pos:
                newpos.append((point[0], point[1]-15))
            self.block += 1
            car_part.pos = newpos
        elif direction == "up":
            for point in car_part.pos:
                newpos.append((point[0], point[1]-3))
            car_part.pos = newpos
        if direction == "right":
            for point in car_part.pos:
                newpos.append((point[0]+20, point[1]))
            self.block = 0
            car_part.pos = newpos
        return car_part
    
    def minmax(self, pos):
        #print(pos)
        xmin = pos[0][0]
        xmax = 0
        ymin = pos[0][1]
        ymax = 0
        for point in pos:
            if point[0] > xmax:
                xmax = point[0]
            if point[0] < xmin:
                xmin = point[0]
            if point[1] > ymax:
                ymax = point[1]
            if point[1] < ymin:
                ymin = point[1]
        return (xmin, xmax, ymin, ymax)

    def check_hitbox(self, hitbox_a, hitbox_b):
        def check_in(x, a, b):
            if a <= x <= b:
                return x
        return (check_in(hitbox_a[0], hitbox_b[0], hitbox_b[1]) or check_in(hitbox_a[1], hitbox_b[0], hitbox_b[1])) and (check_in(hitbox_a[2], hitbox_b[2], hitbox_b[3]) or check_in(hitbox_a[3], hitbox_b[2], hitbox_b[3]))
    
    def norma(self, apoint, bpoint):
        dx = abs(apoint[0] - bpoint[0])
        dy = abs(apoint[1] - bpoint[1])

        return sqrt(dx**2 + dy**2)
    
    def idpoint(self, f_arh, s_arh):
        for obj_a in f_arh:
            if obj_a.pcollision != True:
                for obj_b in s_arh:
                        yield (obj_a, obj_b)

    def prop_check(self, id_a, id_b):
        if id_a.pos != id_b.pos:
            if self.prop(id_a, id_b):
                return False
            else:
                self.rotation(self.rot_direction_chooser(id_a), id_a, id_b)
                return True

