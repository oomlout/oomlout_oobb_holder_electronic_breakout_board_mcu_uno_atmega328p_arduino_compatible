import copy
import opsc
import oobb
import oobb_base
import yaml
import os

def main(**kwargs):
    make_scad(**kwargs)

def make_scad(**kwargs):
    parts = []

    # save_type variables
    if True:
        filter = ""
        filter = "clamp"

        #kwargs["save_type"] = "none"
        kwargs["save_type"] = "all"
        
        navigation = False
        #navigation = True    

        kwargs["overwrite"] = True
        
        #kwargs["modes"] = ["3dpr", "laser", "true"]
        kwargs["modes"] = ["3dpr"]
        #kwargs["modes"] = ["laser"]

    # default variables
    if True:
        kwargs["size"] = "oobb"
        kwargs["width"] = 1
        kwargs["height"] = 1        
        kwargs["thickness"] = 3

        
        
        
    # project_variables
    if True:
        pass
    
    # declare parts
    if True:

        part_default = {} 
        part_default["project_name"] = "test" ####### neeeds setting
        part_default["full_shift"] = [0, 0, 0]
        part_default["full_rotations"] = [0, 0, 0]
        
        part = copy.deepcopy(part_default)
        p3 = copy.deepcopy(kwargs)
        p3["size"] = "oobb"
        p3["width"] = 4
        p3["height"] = 7
        p3["extra"] = "uno_rev_3_atmega328p_arduino_compatible_with_clamp"
        p3["thickness"] = 3
        part["kwargs"] = p3
        part["name"] = "base"
        parts.append(part)

        
        part = copy.deepcopy(part_default)
        p3 = copy.deepcopy(kwargs)
        p3["size"] = "oobb"
        p3["width"] = 4
        p3["height"] = 7
        p3["extra"] = "uno_rev_3_atmega328p_arduino_compatible"
        p3["thickness"] = 3
        part["kwargs"] = p3
        part["name"] = "base"
        parts.append(part)

        
    #make the parts
    if True:
        for part in parts:
            name = part.get("name", "default")            
            extra = part["kwargs"].get("extra", "")
            if filter in name or filter in extra:
                print(f"making {part['name']}")
                make_scad_generic(part)            
                print(f"done {part['name']}")
            else:
                print(f"skipping {part['name']}")


    #generate navigation
    if navigation:
        sort = []
        #sort.append("extra")
        sort.append("name")
        sort.append("width")
        sort.append("height")
        sort.append("thickness")
        
        generate_navigation(sort = sort)


def get_base(thing, **kwargs):
    prepare_print = kwargs.get("prepare_print", False)
    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    depth = kwargs.get("thickness", 3)                    
    rot = kwargs.get("rot", [0, 0, 0])
    pos = kwargs.get("pos", [0, 0, 0])
    extra = kwargs.get("extra", "")
    #pos = copy.deepcopy(pos)
    #pos[2] += -20

    #add plate
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "p"
    p3["shape"] = f"oobb_plate"    
    p3["depth"] = depth
    #p3["holes"] = True         uncomment to include default holes
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos)         
    p3["pos"] = pos1
    oobb_base.append_full(thing,**p3)
    
    #add holes seperate
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "p"
    p3["shape"] = f"oobb_holes"
    p3["both_holes"] = True  
    p3["depth"] = depth
    if width == 4:
        p3["holes"] = ["left", "right"]
    else:
        p3["holes"] = "perimeter"
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos)         
    p3["pos"] = pos1
    oobb_base.append_full(thing,**p3)




    if extra == "uno_rev_3_atmega328p_arduino_compatible":
        thing = add_uno_rev_3_atmega328p_arduino_compatible(thing, **kwargs)
    elif extra == "uno_rev_3_atmega328p_arduino_compatible_with_clamp":
        thing = add_uno_rev_3_atmega328p_arduino_compatible_with_clamp(thing, **kwargs)
    



    if prepare_print:
        #put into a rotation object
        components_second = copy.deepcopy(thing["components"])
        return_value_2 = {}
        return_value_2["type"]  = "rotation"
        return_value_2["typetype"]  = "p"
        pos1 = copy.deepcopy(pos)
        pos1[0] += 50
        return_value_2["pos"] = pos1
        return_value_2["rot"] = [180,0,0]
        return_value_2["objects"] = components_second
        
        thing["components"].append(return_value_2)

    
        #add slice # top
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"oobb_slice"
        #p3["m"] = "#"
        oobb_base.append_full(thing,**p3)
    
###### utilities

def add_uno_rev_3_atmega328p_arduino_compatible(thing, **kwargs):
    depth = kwargs.get("thickness", 3)
    pos = kwargs.get("pos", [0, 0, 0])
    extra_lift = 3
    #add mounting holes
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "negative"
    p3["shape"] = f"oobb_screw_countersunk"
    p3["radius_name"] = "m3"
    p3["depth"] = depth + extra_lift
    p3["holes"] = "mounting"
    #p3["m"] = "#"
    positions = []
    positions.append([-24.185,20.363])
    positions.append([24.181,19.091])
    positions.append([-19.093,-31.822])
    positions.append([8.909,-31.822])
    poss = []
    for position in positions:
        pos1 = copy.deepcopy(pos)
        pos1[0] += position[0]
        pos1[1] += position[1]
        pos1[2] += 0
        poss.append(pos1)        
    p3["pos"] = poss
    rot1 =  [0,180,0]
    p3["rot"] = rot1
    p3["zz"] = "top"
    oobb_base.append_full(thing,**p3)

    #add hoels as negative negative
    dep = depth + 3#+ 29 #from with clamp section
    p4 = copy.deepcopy(p3)
    p4["type"] = "negative_negative"
    p4["shape"] = f"oobb_hole"
    p4["radius_name"] = "m3"
    p4["depth"] = dep
    p4["m"] = "#"
    poss2 = copy.deepcopy(poss)
    for pos1 in poss2:
        pos1[2] += dep
    p4["pos"] = poss2
    oobb_base.append_full(thing,**p4)





    #add cylinder lifters
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "positive_positive"
    p3["shape"] = f"oobb_cylinder"
    p3["radius"] = 6/2
    p3["depth"] = extra_lift
    #p3["m"] = "#"
    
    poss = []
    for position in positions:
        pos1 = copy.deepcopy(pos)
        pos1[0] += position[0]
        pos1[1] += position[1]
        pos1[2] += extra_lift + depth/2
        poss.append(pos1)
    p3["pos"] = poss        
    oobb_base.append_full(thing,**p3)


    return thing

def add_uno_rev_3_atmega328p_arduino_compatible_with_clamp(thing, **kwargs):

    thing = add_uno_rev_3_atmega328p_arduino_compatible(thing, **kwargs)

    depth = kwargs.get("thickness", 3)
    pos = kwargs.get("pos", [0, 0, 0])
    height = kwargs.get("height", 3)
    width = kwargs.get("width", 3)
    extra_lift = 3
    rot = kwargs.get("rot", [0, 0, 0])    

    depth_board = .75
    depth_lift = 20
    #add top clamp plate
    depth_clamp = 9
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "p"
    p3["height"] = 2
    p3["width"] = (18+1)/15
    p3["shape"] = f"oobb_plate"
    p3["depth"] = depth_clamp
    #p3["holes"] = True
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos)
    pos1[0] += -4.5
    pos1[1] += (height/2) * 15 - 15
    pos1[2] += depth + depth_lift
    poss = []
    poss.append(pos1)
    p3["pos"] = poss
    oobb_base.append_full(thing,**p3)

    #bottom clamp plate
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "p"
    p3["height"] = 2
    p3["width"] = 3
    p3["shape"] = f"oobb_plate"
    p3["depth"] = depth_clamp
    #p3["holes"] = True
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos)
    pos1[0] += -7.5
    pos1[1] += -(height/2) * 15 + 15
    pos1[2] += depth + depth_lift
    poss = []
    poss.append(pos1)
    p3["pos"] = poss
    oobb_base.append_full(thing,**p3)



    #cube cutout for pcb
    depth_pcb_cutout = 3 + depth_board
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "n"
    p3["shape"] = f"oobb_cube"
    ex = 3
    w = 54 + ex
    h = 69 + ex
    d = depth_pcb_cutout
    size = [w,h,d]
    p3["size"] = size
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos)
    pos1[1] += 0
    pos1[2] += depth + depth_lift 
    p3["pos"] = pos1
    oobb_base.append_full(thing,**p3)

    #add cutouts for clearance
    cubes = []

    #ldo clearance 7,8 at 11.5,26
    w = 7; h = 8; d = depth_clamp
    x_shift = -11.5; y_shift = 26; z_shift = 0
    cubes.append([[x_shift, y_shift, z_shift], [w,h,d]])

    #fuse clearance 5,8 at 0,28.5
    w = 5+1; h = 8; d = depth_clamp
    x_shift = 0; y_shift = 28.5; z_shift = 0
    cubes.append([[x_shift, y_shift, z_shift], [w,h,d]])

    #extra capacitor clearnce 1,2 at 3,22.5
    w = 1; h = 2; d = depth_clamp
    x_shift = 3; y_shift = 22.5; z_shift = 0

    #bottom clearance
    #icsp 8,6 at 1.5,-30.5
    w = 8; h = 6; d = depth_clamp
    x_shift = 1.5; y_shift = -30.5; z_shift = 0
    cubes.append([[x_shift, y_shift, z_shift], [w,h,d]])

    #chip 10,36 at -10.5,-13.5
    w = 10; h = 36; d = depth_clamp
    x_shift = -10.5; y_shift = -13.5; z_shift = 0
    cubes.append([[x_shift, y_shift, z_shift], [w,h,d]])

    #left uno header 2.54,2.54*6 at -24,-23
    w = 2.54; h = 2.54*6; d = depth_clamp
    x_shift = -24; y_shift = -23; z_shift = 0
    cubes.append([[x_shift, y_shift, z_shift], [w,h,d]])

    #misc component clearance 14'6 at 6.5,-22.5
    w = 14; h = 6; d = depth_clamp
    x_shift = 6.5; y_shift = -22.5; z_shift = 0
    cubes.append([[x_shift, y_shift, z_shift], [w,h,d]])

    for cube in cubes:
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"oobb_cube"
        ex = 3
        w = cube[1][0] + ex
        h = cube[1][1] + ex
        d = cube[1][2]
        size = [w,h,d]
        p3["size"] = size
        p3["m"] = "#"
        pos1 = copy.deepcopy(pos)
        pos1[0] += cube[0][0]
        pos1[1] += cube[0][1]
        pos1[2] += cube[0][2]+depth_lift+depth
        p3["pos"] = pos1
        oobb_base.append_full(thing,**p3)

    #add countersunk linkers
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "n"
    p3["shape"] = f"oobb_screw_countersunk"
    p3["radius_name"] = "m3"
    p3["depth"] = depth_clamp + depth + depth_lift
    p3["nut"] = True
    p3["overhang"] = True
    p3["m"] = "#"
    pos1 = copy.deepcopy(pos)    
    pos1[2] += 0
    pos11 = copy.deepcopy(pos1)
    y_top = 37.5
    y_bottom = -37.5
    pos11[0] += -11.25
    pos11[1] += y_top
    pos12 = copy.deepcopy(pos1)
    pos12[0] += 0
    pos12[1] += 45
    pos13 = copy.deepcopy(pos1)
    pos13[0] += 0
    pos13[1] += y_bottom
    pos14 = copy.deepcopy(pos1)
    pos14[0] += -15
    pos14[1] += y_bottom
    poss = []
    poss = []
    poss.append(pos11)
    poss.append(pos12)
    poss.append(pos13)
    poss.append(pos14)
    p3["pos"] = poss
    rot1 = copy.deepcopy(rot)    
    rot1[1] = 180 
    rot1[2] += 360/12
    p3["rot"] = rot1
    oobb_base.append_full(thing,**p3)

    #locating spheres
    positions = []
    #positions.append([-23.96,26.46])
    positions.append([24,24])
    positions.append([-19.5,-26.5])
    positions.append([8.5,-26.5])
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "positive_positive"
    p3["shape"] = f"sphere"
    p3["radius"] = 2.75/2
    #p3["m"] = "#"
    poss = []
    for shift in positions:
        pos1 = copy.deepcopy(pos)
        pos1[0] += shift[0]
        pos1[1] += shift[1]
        pos1[2] += depth + depth_lift + 3 + depth_board
        poss.append(pos1)
    p3["pos"] = poss
    #oobb_base.append_full(thing,**p3)



    return thing




def make_scad_generic(part):
    
    # fetching variables
    name = part.get("name", "default")
    project_name = part.get("project_name", "default")
    
    kwargs = part.get("kwargs", {})    
    
    modes = kwargs.get("modes", ["3dpr", "laser", "true"])
    save_type = kwargs.get("save_type", "all")
    overwrite = kwargs.get("overwrite", True)

    kwargs["type"] = f"{project_name}_{name}"

    thing = oobb_base.get_default_thing(**kwargs)
    kwargs.pop("size","")

    #get the part from the function get_{name}"
    func = globals()[f"get_{name}"]    
    # test if func exists
    if callable(func):            
        func(thing, **kwargs)        
    else:            
        get_base(thing, **kwargs)   
    
    folder = f"scad_output/{thing['id']}"

    for mode in modes:
        depth = thing.get(
            "depth_mm", thing.get("thickness_mm", 3))
        height = thing.get("height_mm", 100)
        layers = depth / 3
        tilediff = height + 10
        start = 1.5
        if layers != 1:
            start = 1.5 - (layers / 2)*3
        if "bunting" in thing:
            start = 0.5
        

        opsc.opsc_make_object(f'{folder}/{mode}.scad', thing["components"], mode=mode, save_type=save_type, overwrite=overwrite, layers=layers, tilediff=tilediff, start=start)  

    yaml_file = f"{folder}/working.yaml"
    with open(yaml_file, 'w') as file:
        part_new = copy.deepcopy(part)
        kwargs_new = part_new.get("kwargs", {})
        kwargs_new.pop("save_type","")
        part_new["kwargs"] = kwargs_new
        import os
        cwd = os.getcwd()
        part_new["project_name"] = cwd
        part_new["id"] = thing["id"]
        part_new["thing"] = thing
        yaml.dump(part_new, file)

def generate_navigation(folder="scad_output", sort=["width", "height", "thickness"]):
    #crawl though all directories in scad_output and load all the working.yaml files
    parts = {}
    for root, dirs, files in os.walk(folder):
        if 'working.yaml' in files:
            yaml_file = os.path.join(root, 'working.yaml')
            #if working.yaml isn't in the root directory, then do it
            if root != folder:
                with open(yaml_file, 'r') as file:
                    part = yaml.safe_load(file)
                    # Process the loaded YAML content as needed
                    part["folder"] = root
                    part_name = root.replace(f"{folder}","")
                    
                    #remove all slashes
                    part_name = part_name.replace("/","").replace("\\","")
                    parts[part_name] = part

                    print(f"Loaded {yaml_file}: {part}")

    pass
    for part_id in parts:
        part = parts[part_id]
        kwarg_copy = copy.deepcopy(part["kwargs"])
        folder_navigation = "navigation_oobb"
        folder_source = part["folder"]
        folder_extra = ""
        for s in sort:
            if s == "name":
                ex = part.get("name", "default")
            else:
                ex = kwarg_copy.get(s, "default")
            folder_extra += f"{s}_{ex}/"

        #replace "." with d
        folder_extra = folder_extra.replace(".","d")            
        folder_destination = f"{folder_navigation}/{folder_extra}"
        if not os.path.exists(folder_destination):
            os.makedirs(folder_destination)
        if os.name == 'nt':
            #copy a full directory auto overwrite
            command = f'xcopy "{folder_source}" "{folder_destination}" /E /I /Y'
            print(command)
            os.system(command)
        else:
            os.system(f"cp {folder_source} {folder_destination}")

if __name__ == '__main__':
    kwargs = {}
    main(**kwargs)